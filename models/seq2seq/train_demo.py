from tensorflow import keras
from tensorflow.keras import backend as K
import numpy as np

# TODO(xcdu) TO BE REFINED

from seq2seq.seq2seq import Seq2Seq, encoder_infer, decoder_infer




mask_words = ["<VALUE>", "<BOL>", "<IND>", "<PAD>", "<UNK>", "<GO>", "<EOS>"]

context_path = "pdata/context"
template_path = "pdata/template"

context_file = open(context_path, "r", encoding="utf-8")
context_content = context_file.readlines()
context_file.close()

template_file = open(template_path, "r", encoding="utf-8")
template_content = template_file.readlines()
template_file.close()

all_content = list(context_content) + list(template_content)

vocab_word = set([word for line in all_content for word in line.split()])

for word in mask_words:
    if word in vocab_word:
        vocab_word.remove(word)

vocab = list(mask_words) + list(vocab_word)
vocab2id = {word: i for i, word in enumerate(vocab)}
id2vocab = {i: word for i, word in enumerate(vocab)}

context_ids = [[vocab2id[word] for word in context.split()] for context in context_content]
template_ids = [[vocab2id[word] for word in template.split()] for template in template_content]

# unnecessary multiple when amount of data increasing
for i in range(10):
    context_ids = context_ids + context_ids
    template_ids = template_ids + template_ids

source_inputs = []
target_inputs = []
target_outputs = []

for (source, target) in zip(context_ids, template_ids):
    source_inputs.append([vocab2id["<GO>"]] + source + [vocab2id["<EOS>"]])
    target_inputs.append([vocab2id["<GO>"]] + target)
    target_outputs.append(target + [vocab2id["<EOS>"]])


# maxlen should be consider
maxlen = 10

source_input_ids = keras.preprocessing.sequence.pad_sequences(source_inputs, padding='post', maxlen=maxlen)
target_input_ids = keras.preprocessing.sequence.pad_sequences(target_inputs, padding='post', maxlen=maxlen)
target_output_ids = keras.preprocessing.sequence.pad_sequences(target_outputs, padding='post', maxlen=maxlen)

K.clear_session()

embedding_dim = 50
hidden_units = 128
vocab_size = len(vocab2id)


# Starts here
# encoder_inputs = Input(shape=(None, maxlen))
# encoder = LSTM(latent_dim, return_state=True)
# encoder_outpus, state_h, state_c = encoder(encoder_inputs)
# encoder_state = [state_h, state_c]
#
# decoder_inputs = Input(shape=(None, num_decoder_tokens))
# decoder_lstm = LSTM(latent_dim, return_sequences=True, return_state=True)
# decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_state)
# decoder_dense = Dense(num_decoder_tokens, activation='softmax')
# decoder_outputs = decoder_dense(decoder_output




model = Seq2Seq(maxlen, embedding_dim, hidden_units, vocab_size)
print(model.summary())


epochs = 3
batch_size = 32
val_rate = 0.2

loss_fn = keras.losses.SparseCategoricalCrossentropy()
model.compile(loss=loss_fn, optimizer='adam')
model.fit([source_input_ids, target_input_ids], target_output_ids,
          batch_size=batch_size, epochs=epochs, validation_split=val_rate)

encoder_model = encoder_infer(model)
print(encoder_model.summary())

decoder_model = decoder_infer(model, encoder_model)
print(decoder_model.summary())


maxlen = 10
def infer_predict(input_text, encoder_model, decoder_model):
    text_words = input_text.split()[:maxlen]
    input_id = [vocab2id[w] if w in vocab2id else vocab2id["<UNK>"] for w in text_words]
    # input_id = [vocab2id["<START>"]] + input_id + [vocab2id["<END>"]]
    if len(input_id) < maxlen:
        input_id = input_id + [vocab2id["<PAD>"]] * (maxlen - len(input_id))

    input_source = np.array([input_id])
    input_target = np.array([vocab2id["<GO>"]])

    # 编码器encoder预测输出
    enc_outputs, enc_state_h, enc_state_c = encoder_model.predict([input_source])
    dec_inputs = input_target
    dec_states_inputs = [enc_state_h, enc_state_c]

    result_id = []
    result_text = []
    for i in range(maxlen):
        dense_outputs, dec_state_h, dec_state_c = decoder_model.predict([enc_outputs, dec_inputs] + dec_states_inputs)
        pred_id = np.argmax(dense_outputs[0][0])
        result_id.append(pred_id)
        result_text.append(id2vocab[pred_id])
        if id2vocab[pred_id] == "<EOS>":
            break
        dec_inputs = np.array([[pred_id]])
        dec_states_inputs = [dec_state_h, dec_state_c]
    return result_id, result_text

input_text = "MeshConfig"
result_id, result_text = infer_predict(input_text, encoder_model, decoder_model)

print("Input: ", input_text)
print("Output: ", result_text, result_id)


