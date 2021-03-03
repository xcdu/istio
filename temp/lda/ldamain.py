#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gensim.models import ldamodel
from gensim import corpora

from docs_helper import load_raw_from_dir
from parse_docs.graph import IstioGraph
from nltk.corpus import stopwords

from temp.lda.temp import clean_text

from pprint import pprint as print

in_path = "../../.data"

raw_pages = load_raw_from_dir(in_path)

graph = IstioGraph()
graph.build(page_dicts=raw_pages)

docs_dict = dict()
templates_dict = dict()

for page in graph.pages:
  docs_dict[page.page_indexer] = "\n".join(page.content_list)
  templates_dict[page.page_indexer] = page.templates_hierarchy

docs = docs_dict.values()

stopwords = stopwords.words("english")

docs = [clean_text(doc) for doc in docs]

texts = [[word for word in doc.lower().split() if word not in stopwords] for doc
         in docs]

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

lda = ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=10)
print(lda.show_topics(num_topics=10, num_words=100))

lda.save('lda.model')

lda = ldamodel.LdaModel.load('lda.model')

for k, v in docs_dict.items():
  text = v
  text = clean_text(text)
  texts = [word for word in text.lower().split() if word not in stopwords]
  bow = dictionary.doc2bow(texts)
  print("==========")
  print(k)
  print(lda.get_document_topics(bow))
