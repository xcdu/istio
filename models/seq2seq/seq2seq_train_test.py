#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

from keras.models import Model
from keras.layers import Input, LSTM, Dense
from models.seq2seq.data_preparation import prepare_input
import numpy as np
import re

df = prepare_input()
texts = df["processed_text"]
templates = df["processed_template"]

text_chars = set()
template_chars = set()

input_texts = []
for text in texts:
    input_text = " ".join(text)
    input_text = input_text.replace("\t", " ")
    input_text = input_text.replace("\n", " ")
    input_texts.append(input_text)
    for text_c in input_text:
        text_chars.add(text_c)

input_templates = []
for template in templates:
    input_template = " ".join(template)
    input_template = re.sub(r"<NUM_\d+>", "<NUM>", input_template)
    input_template = input_template.replace('\t', ' ')
    input_template = input_template.replace('\n', ' ')
    input_template = '\t' + input_template + '\n'
    input_templates.append(input_template)
    for template_c in input_template:
        template_chars.add(template_c)

print(f"len text chars: {len(text_chars)} len template chars: {len(template_chars)}")
num_encoder_tokens = len(text_chars)
num_decoder_tokens = len(template_chars)

max_text_seq_len = max([len(t) for t in input_texts])
max_encoder_seq_length = max_text_seq_len
max_temp_seq_len = max([len(t) for t in input_templates])
max_decoder_seq_length = max_temp_seq_len
print(f"len max text: {max_text_seq_len} len max temp: {max_temp_seq_len}")

num_samples = len(input_texts)
print(f"num samples: {num_samples}")

input_token_index = dict([(c, i) for i, c in enumerate(text_chars)])
target_token_index = dict([c, i] for i, c in enumerate(template_chars))

encoder_input_data = np.zeros((len(input_texts), max_encoder_seq_length, num_encoder_tokens), dtype="float32")
decoder_input_data = np.zeros((len(input_texts), max_decoder_seq_length, num_decoder_tokens), dtype="float32")
decoder_target_data = np.zeros((len(input_texts), max_decoder_seq_length, num_decoder_tokens), dtype="float32")

for i, (input_text, target_text) in enumerate(zip(input_texts, input_templates)):
    for t, c in enumerate(input_text):
        encoder_input_data[i, t, input_token_index[c]] = 1.
        encoder_input_data[i, t + 1:, input_token_index[' ']] = 1.
    for t, c in enumerate(target_text):
        decoder_target_data[i, t - 1, target_token_index[c]] = 1.
        decoder_input_data[i, t + 1:, target_token_index[' ']] = 1.
        decoder_target_data[i, t:, target_token_index[' ']] = 1.

print(encoder_input_data.shape)
print(decoder_input_data.shape)
print(decoder_target_data.shape)

latent_dim = 64
batch_size = 10
epochs = 2

# Define an input sequence and process it.
encoder_inputs = Input(shape=(None, num_encoder_tokens))
encoder = LSTM(latent_dim, return_state=True)
encoder_outputs, state_h, state_c = encoder(encoder_inputs)
# We discard `encoder_outputs` and only keep the states.
encoder_states = [state_h, state_c]

# Set up the decoder, using `encoder_states` as initial state.
decoder_inputs = Input(shape=(None, num_decoder_tokens))
# We set up our decoder to return full output sequences,
# and to return internal states as well. We don't use the
# return states in the training model, but we will use them in inference.
decoder_lstm = LSTM(latent_dim, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(decoder_inputs,
                                     initial_state=encoder_states)
decoder_dense = Dense(num_decoder_tokens, activation='softmax')
decoder_outputs = decoder_dense(decoder_outputs)

# Define the model that will turn
# `encoder_input_data` & `decoder_input_data` into `decoder_target_data`
model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

# Run training
model.compile(optimizer='rmsprop', loss='categorical_crossentropy')
model.fit([encoder_input_data, decoder_input_data], decoder_target_data,
          batch_size=batch_size,
          epochs=epochs,
          validation_split=0.2)
# Save model
model.save("seq2seq.model.2")

# Next: inference mode (sampling).
# Here's the drill:
# 1) encode input and retrieve initial decoder state
# 2) run one step of decoder with this initial state
# and a "start of sequence" token as target.
# Output will be the next target token
# 3) Repeat with the current target token and current states

# Define sampling models
encoder_model = Model(encoder_inputs, encoder_states)

decoder_state_input_h = Input(shape=(latent_dim,))
decoder_state_input_c = Input(shape=(latent_dim,))
decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
decoder_outputs, state_h, state_c = decoder_lstm(
    decoder_inputs, initial_state=decoder_states_inputs)
decoder_states = [state_h, state_c]
decoder_outputs = decoder_dense(decoder_outputs)
decoder_model = Model(
    [decoder_inputs] + decoder_states_inputs,
    [decoder_outputs] + decoder_states)

# Reverse-lookup token index to decode sequences back to
# something readable.
reverse_input_char_index = dict(
    (i, char) for char, i in input_token_index.items())
reverse_target_char_index = dict(
    (i, char) for char, i in target_token_index.items())


def decode_sequence(input_seq):
    # Encode the input as state vectors.
    states_value = encoder_model.predict(input_seq)

    # Generate empty target sequence of length 1.
    target_seq = np.zeros((1, 1, num_decoder_tokens))
    # Populate the first character of target sequence with the start character.
    target_seq[0, 0, target_token_index['\t']] = 1.

    # Sampling loop for a batch of sequences
    # (to simplify, here we assume a batch of size 1).
    stop_condition = False
    decoded_sentence = ''
    while not stop_condition:
        output_tokens, h, c = decoder_model.predict(
            [target_seq] + states_value)

        # Sample a token
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_char = reverse_target_char_index[sampled_token_index]
        decoded_sentence += sampled_char

        # Exit condition: either hit max length
        # or find stop character.
        if (sampled_char == '\n' or
                len(decoded_sentence) > max_decoder_seq_length):
            stop_condition = True

        # Update the target sequence (of length 1).
        target_seq = np.zeros((1, 1, num_decoder_tokens))
        target_seq[0, 0, sampled_token_index] = 1.

        # Update states
        states_value = [h, c]

    return decoded_sentence


for seq_index in range(100):
    # Take one sequence (part of the training test)
    # for trying out decoding.
    input_seq = encoder_input_data[seq_index: seq_index + 1]
    decoded_sentence = decode_sequence(input_seq)
    print('-')
    print('Input sentence:', input_texts[seq_index])
    print('Decoded sentence:', decoded_sentence)