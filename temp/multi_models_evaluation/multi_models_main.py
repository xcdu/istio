#!/usr/bin/env python
# -*- coding: utf-8 -*-
import string

import pandas as pd
import textblob
# import xgboost
from sklearn import ensemble
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from modules.nlp_preprocess.feature import SpacyFeature
from manual import IstioManual
from modules.nlp_preprocess.input_adapter import IstioManualInputAdaptor
from modules.nlp_preprocess.preprocessor import PipelinePreprocessor
from docs_helper import load_pages_from_dir

in_path = "../../.data"

raw_pages = load_pages_from_dir(in_path)

manual = IstioManual()
manual.build(pages=raw_pages)

input_adapter = IstioManualInputAdaptor()
data = input_adapter.multilevel_format(manual.manual)

import json

with open("data.pickle", "w", encoding="utf-8") as out_pickle:
  json.dump(data, out_pickle)

in_pickle = open("data.pickle", "r", encoding="utf-8")
data = json.load(in_pickle)
in_pickle.close()

for key, data in data.items():
  print("CURRENT LEVEL: {}".format(key))
  preprocessor = PipelinePreprocessor()
  preprocessor.set_features([SpacyFeature])
  data = preprocessor.process(in_data=data)

  texts = list()
  labels = list()
  for indexer, contents in data.items():
    for content in contents:
      texts.append(content)
      labels.append(indexer)

  print("NUMBER OF LABELS: {}".format(len(set(labels))))
  print("NUMBER OF SLICED CONTENTS: {}".format(len(set(texts))))

  df = pd.DataFrame()
  df["text"] = texts
  df["label"] = labels

  label_encoder = LabelEncoder()
  df["label"] = label_encoder.fit_transform(df["label"])

  train_x, valid_x, train_y, valid_y = train_test_split(df["text"], df["label"])


  def train_model(classifier, feature_vector_train, label, feature_vector_valid,
                  is_neural_net=False):

    # fit the training dataset on the classifier
    classifier.fit(feature_vector_train, label)

    # predict the labels on validation dataset
    predictions = classifier.predict(feature_vector_valid)

    if is_neural_net:
      predictions = predictions.argmax(axis=-1)

    return metrics.accuracy_score(predictions, valid_y)


  # count
  count_vector = CountVectorizer(analyzer="word", token_pattern=r"\w{1,}")
  count_vector.fit(texts)

  # 创建一个向量计数器对象
  count_vect = CountVectorizer(analyzer='word', token_pattern=r'\w{1,}')
  count_vect.fit(df['text'])

  # 使用向量计数器对象转换训练集和验证集
  xtrain_count = count_vect.transform(train_x)
  xvalid_count = count_vect.transform(valid_x)

  # 词语级tf-idf
  tfidf_vect = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}',
                               max_features=5000)
  tfidf_vect.fit(df['text'])
  xtrain_tfidf = tfidf_vect.transform(train_x)
  xvalid_tfidf = tfidf_vect.transform(valid_x)

  # ngram 级tf-idf
  tfidf_vect_ngram = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}',
                                     ngram_range=(2, 3), max_features=5000)
  tfidf_vect_ngram.fit(df['text'])
  xtrain_tfidf_ngram = tfidf_vect_ngram.transform(train_x)
  xvalid_tfidf_ngram = tfidf_vect_ngram.transform(valid_x)

  # 词性级tf-idf
  tfidf_vect_ngram_chars = TfidfVectorizer(analyzer='char',
                                           ngram_range=(2, 3),
                                           max_features=5000)
  tfidf_vect_ngram_chars.fit(df['text'])
  xtrain_tfidf_ngram_chars = tfidf_vect_ngram_chars.transform(train_x)
  xvalid_tfidf_ngram_chars = tfidf_vect_ngram_chars.transform(valid_x)

  df['char_count'] = df['text'].apply(len)
  df['word_count'] = df['text'].apply(lambda x: len(x.split()))
  df['word_density'] = df['char_count'] / (df['word_count'] + 1)
  df['punctuation_count'] = df['text'].apply(
    lambda x: len("".join(_ for _ in x if _ in string.punctuation)))
  df['title_word_count'] = df['text'].apply(
    lambda x: len([wrd for wrd in x.split() if wrd.istitle()]))
  df['upper_case_word_count'] = df['text'].apply(
    lambda x: len([wrd for wrd in x.split() if wrd.isupper()]))
  pos_family = {
    'noun': ['NN', 'NNS', 'NNP', 'NNPS'],
    'pron': ['PRP', 'PRP$', 'WP', 'WP$'],
    'verb': ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'],
    'adj': ['JJ', 'JJR', 'JJS'],
    'adv': ['RB', 'RBR', 'RBS', 'WRB']
  }


  # 检查和获得特定句子中的单词的词性标签数量
  def check_pos_tag(x, flag):
    cnt = 0
    try:
      wiki = textblob.TextBlob(x)
      for tup in wiki.tags:
        ppo = list(tup)[1]
      if ppo in pos_family[flag]:
        cnt += 1
    except:
      pass


  # # Linear Classifier on Count Vectors
  # accuracy = train_model(linear_model.LogisticRegression(), xtrain_count,
  #                        train_y, xvalid_count)
  # print("LR, Count Vectors: ", accuracy)
  #
  # # 特征为词语级别TF-IDF向量的线性分类器
  # accuracy = train_model(linear_model.LogisticRegression(), xtrain_tfidf,
  #                        train_y, xvalid_tfidf)
  # print("LR, WordLevel TF-IDF: ", accuracy)
  #
  # # 特征为多个词语级别TF-IDF向量的线性分类器
  # accuracy = train_model(linear_model.LogisticRegression(), xtrain_tfidf_ngram,
  #                        train_y, xvalid_tfidf_ngram)
  # print("LR, N-Gram Vectors: ", accuracy)
  #
  # # 特征为词性级别TF-IDF向量的线性分类器
  # accuracy = train_model(linear_model.LogisticRegression(),
  #                        xtrain_tfidf_ngram_chars, train_y,
  #                        xvalid_tfidf_ngram_chars)
  # print("LR, CharLevel Vectors: ", accuracy)

  # 特征为计数向量的RF
  accuracy = train_model(ensemble.RandomForestClassifier(), xtrain_count,
                         train_y, xvalid_count)
  print("RF, Count Vectors: ", accuracy)

  # 特征为词语级别TF-IDF向量的RF
  accuracy = train_model(ensemble.RandomForestClassifier(), xtrain_tfidf,
                         train_y, xvalid_tfidf)
  print("RF, WordLevel TF-IDF: ", accuracy)

  # # 特征为计数向量的Xgboost
  # accuracy = train_model(xgboost.XGBClassifier(), xtrain_count.tocsc(), train_y,
  #                        xvalid_count.tocsc())
  # print("Xgb, Count Vectors: ", accuracy)
  #
  # # 特征为词语级别TF-IDF向量的Xgboost
  # accuracy = train_model(xgboost.XGBClassifier(), xtrain_tfidf.tocsc(), train_y,
  #                        xvalid_tfidf.tocsc())
  # print("Xgb, WordLevel TF-IDF: ", accuracy)
  #
  # # 特征为词性级别TF-IDF向量的Xgboost
  # accuracy = train_model(xgboost.XGBClassifier(),
  #                        xtrain_tfidf_ngram_chars.tocsc(), train_y,
  #                        xvalid_tfidf_ngram_chars.tocsc())
  # print("Xgb, CharLevel Vectors: ", accuracy)
