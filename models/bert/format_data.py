import os
import shutil
import csv

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
from official.nlp import bert
import official.nlp.bert.tokenization

from model_mapping import name_to_handle

def main():
    data_path_dataset = "Istio_data"
    data_folders = ["train", "test"]
    data_labels = ["General", "Configuration", "Telemetry", "Networking", "Security"]

    #Remove previous files
    for folder in data_folders:
        for subfolder in data_labels:
            for root, dirs, files in os.walk(data_path_dataset + "/" + folder + "/" + subfolder):
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))

    bert_model_name = 'small_bert/bert_en_uncased_L-12_H-768_A-12'
    tfhub_handle_encoder = name_to_handle(bert_model_name)
    bert_layer = hub.KerasLayer(tfhub_handle_encoder, trainable = False)
    vocab_file = bert_layer.resolved_object.vocab_file.asset_path.numpy()
    tokenizer = bert.tokenization.FullTokenizer(vocab_file=vocab_file, do_lower_case=True)

    data_path_data = "post_fixed.csv"
    with open(data_path_data, encoding="utf8") as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        first_line = True
        train = True #(if false then test)
        for row in data:
            if first_line:
                first_line = False
            else:
                if row[1] == '0' and row[7] in data_labels:
                    if train: #part of the training data
                        #print(row[6])
                        f = open(data_path_dataset + "/train/" + row[7] + "/" + row[0] + ".txt", "w", encoding="utf-8")
                        f.write(preprocess(row[6], tokenizer))
                        f.close()
                        train = not train
                    else: #part of the testing data
                        #print(row[6])
                        f = open(data_path_dataset + "/test/" + row[7] + "/" + row[0] + ".txt", "w", encoding="utf-8")
                        f.write(preprocess(row[6], tokenizer))
                        f.close()
                        train = not train

def preprocess(text, tokenizer):
    token_id = tokenizer.convert_tokens_to_ids(tokenizer.tokenize(text))
    return list_to_string(token_id)

def list_to_string(some_list):
    return_string = ""
    for value in some_list:
        return_string += (str(value) + ' ')
    return return_string[:-1]

if __name__ == '__main__':
        main()
