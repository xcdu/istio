#!/usr/bin/env python
# -*- coding: utf-8 -*-
from preprocess_corpus.preprocess_forum import load_forum_dataframe
import re
import numpy as np


def load_texts_templates_dataset():
    df = load_forum_dataframe()
    df = df.loc[:, ["processed_text", "processed_template"]]
    df = df.loc[df["processed_text"].notnull() & df["processed_template"].notnull()]

    texts = df["processed_text"]
    templates = df["processed_template"]
    return texts, templates


def format_input_text(texts):
    text_chars = set()
    input_texts = []
    for text in texts:
        input_text = " ".join(text)
        input_text = input_text.replace("\t", " ")
        input_text = input_text.replace("\n", " ")
        input_texts.append(input_text)
        for text_c in input_text:
            text_chars.add(text_c)
    text_token_index = dict([(c, i) for i, c in enumerate(text_chars)])
    return input_texts, text_chars, text_token_index


def format_input_template(templates):
    template_chars = set()
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
    template_token_index = dict([c, i] for i, c in enumerate(template_chars))
    return input_templates, template_chars, template_token_index


def calculate_parameters(input_texts, text_chars, input_templates, template_chars):
    print(f"len text chars: {len(text_chars)} len template chars: {len(template_chars)}")
    # num_encoder_tokens
    num_text_tokens = len(text_chars)
    # num_decoder_tokens
    num_template_tokens = len(template_chars)

    # max encoder sequence length
    max_text_seq_len = max([len(t) for t in input_texts])
    # max decoder sequence length
    max_template_seq_len = max([len(t) for t in input_templates])
    print(f"len max text: {max_text_seq_len} len max temp: {max_template_seq_len}")

    num_samples = len(input_texts)
    print(f"num samples: {num_samples}")
    return num_samples, num_text_tokens, num_template_tokens, max_text_seq_len, max_template_seq_len


def prepare_encoder_decoder_data(
        input_texts, target_texts,
        input_token_index, target_token_index,
        num_encoder_tokens, max_encoder_seq_length,
        num_decoder_tokens, max_decoder_seq_length):
    # init encoder/decoder input arrays
    encoder_input_data = np.zeros((len(input_texts), max_encoder_seq_length, num_encoder_tokens), dtype="float32")
    decoder_input_data = np.zeros((len(input_texts), max_decoder_seq_length, num_decoder_tokens), dtype="float32")
    decoder_target_data = np.zeros((len(input_texts), max_decoder_seq_length, num_decoder_tokens), dtype="float32")

    for i, (input_text, target_text) in enumerate(zip(input_texts, target_texts)):
        for t, char in enumerate(input_text):
            encoder_input_data[i, t, input_token_index[char]] = 1.
        for t, char in enumerate(target_text):
            # decoder_target_data is ahead of decoder_input_data by one timestep
            decoder_input_data[i, t, target_token_index[char]] = 1.
            if t > 0:
                # decoder_target_data will be ahead by one timestep
                # and will not include the start character.
                decoder_target_data[i, t - 1, target_token_index[char]] = 1.

    return encoder_input_data, decoder_input_data, decoder_target_data


# def prepare_train_input():
#     texts, templates = load_texts_templates_dataset()
#     input_texts, text_chars, input_token_index = format_input_text(texts)
#     input_templates, template_chars, target_token_index = format_input_template(templates)
#     num_sample, num_encoder_tokens, num_decoder_tokens, max_encoder_seq_length, max_decoder_seq_length = \
#         calculate_parameters(input_texts, text_chars, input_templates, template_chars)
#     encoder_input_data, decoder_input_data, decoder_target_data = prepare_encoder_decoder_data(
#         input_texts, input_templates, input_token_index, target_token_index, num_encoder_tokens, max_encoder_seq_length,
#         num_decoder_tokens, max_decoder_seq_length)
#     return input_texts, input_templates, text_chars, template_chars, input_token_index, target_token_index, num_sample,\
#            num_encoder_tokens, num_decoder_tokens, max_encoder_seq_length, max_decoder_seq_length, encoder_input_data,\
#            decoder_input_data, decoder_target_data
