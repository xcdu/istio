import os
import shutil
import csv
import re
import math

import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
from official.nlp import bert
import official.nlp.bert.tokenization

from model_mapping import name_to_handle

def get_data(path_to_file, model_name, batch_size, train_count, validate_count, test_count):
    all_texts = []
    all_labels = []
    data_labels = ["General", "Configuration", "Telemetry", "Networking", "Security"]

    label_to_int = {"General": 0, "Configuration": 1, "Telemetry": 2, "Networking": 3, "Security": 4}

    with open(path_to_file, encoding="utf8") as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        first_line = True
        for row in data:
            if first_line:
                first_line = False
            else:
                if row[1] == '0' and row[7] in data_labels:  # Valid data
                    all_texts.append(row[6])
                    all_labels.append(label_to_int[row[7]])
    np_all_labels = np.array(all_labels)

    # print('\n\n\n', all_texts[0])
    # print('\n\n\n', all_texts[1])

    # Remove punctuation and other special characters
    edited_texts = []
    for text in all_texts:
        text = re.sub(r'http\S+', '', text)
        text = re.sub('[^a-zA-Z0-9]', ' ', text)
        text = re.sub(r"\s+[a-zA-Z0-9]\s+", ' ', text)
        text = re.sub(r'\s+', ' ', text)
        edited_texts.append(text)

    # print('\n\n\n', edited_texts[0])
    # print('\n\n\n', edited_texts[1], '\n\n\n')

    # Tokenize
    tfhub_handle_encoder = name_to_handle(model_name)
    bert_layer = hub.KerasLayer(tfhub_handle_encoder, trainable=False)
    vocab_file = bert_layer.resolved_object.vocab_file.asset_path.numpy()
    tokenizer = bert.tokenization.FullTokenizer(vocab_file=vocab_file, do_lower_case=True)
    tokenized_texts = []
    for comment in edited_texts:
        tokenized_texts.append(tokenizer.convert_tokens_to_ids(tokenizer.tokenize(comment)))

    dataset = [[text, np_all_labels[i], len(text)] for i, text in enumerate(tokenized_texts)]
    dataset.sort(key=lambda x: x[2])
    final_dataset = [(data_instance[0], data_instance[1]) for data_instance in dataset]

    processed_dataset = tf.data.Dataset.from_generator(lambda: final_dataset, output_types=(tf.int32, tf.int32))
    print(processed_dataset)
    batched_dataset = processed_dataset.padded_batch(batch_size, padded_shapes=((None,), ()))

    # Split into training, validation, and testing
    total_batches = math.ceil(len(final_dataset) / batch_size)
    training_amount = total_batches * train_count // 100
    validation_amount = total_batches * validate_count // 100
    testing_amount = total_batches * test_count // 100

    batched_dataset.shuffle(total_batches)
    testing_ds = batched_dataset.take(testing_amount)
    other_ds = batched_dataset.skip(testing_amount)
    training_ds = other_ds.take(training_amount)
    validation_ds = other_ds.skip(training_amount)

    # print(next(iter(training_ds)))
    # print(next(iter(validation_ds)))
    # print(next(iter(testing_ds)))

    return training_ds, validation_ds, testing_ds, len(tokenizer.vocab)

# get_data("post_fixed.csv", 'small_bert/bert_en_uncased_L-12_H-768_A-12', 32, 70, 10, 20)