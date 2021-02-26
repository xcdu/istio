from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsOneClassifier
from sklearn.svm import LinearSVC

from manual import IstioManual

from docs_helper import load_pages_from_dir
from input_adapter import IstioManualInputAdaptor
from preprocessor import PipelinePreprocessor


def train_model(classifier, feature_vector_train, label, feature_vector_valid,
                valid_y):
  classifier.fit(feature_vector_train, label)
  predictions = classifier.predict(feature_vector_valid)
  print(predictions)
  return accuracy_score(predictions, valid_y)


in_path = "../../.data"

raw_pages = load_pages_from_dir(in_path)

manual = IstioManual()
manual.build(pages=raw_pages)

input_adapter = IstioManualInputAdaptor()
data = input_adapter.multilevel_format(manual.manual)

input_data = data[3]

preprocessor = PipelinePreprocessor()
data = preprocessor.process(in_data=input_data)

texts = list()
labels = list()
for indexer, contents in data.items():
  for content in contents:
    texts.append(content)
    labels.append(indexer)

label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(labels)

train_x, valid_x, train_y, valid_y = train_test_split(texts, labels)

tfidf_vector_ngram = TfidfVectorizer(analyzer="word", token_pattern=r"\w{1,}",
                                     max_features=5000,
                                     ngram_range=(2, 3))
tfidf_vector_ngram.fit(texts)
train_x_tfidf_ngram = tfidf_vector_ngram.transform(train_x)
valid_x_tfidf_ngram = tfidf_vector_ngram.transform(valid_x)

accuracy = train_model(OneVsOneClassifier(LinearSVC(random_state=0)),
                       train_x_tfidf_ngram,
                       train_y,
                       valid_x_tfidf_ngram, valid_y)
print(accuracy)
