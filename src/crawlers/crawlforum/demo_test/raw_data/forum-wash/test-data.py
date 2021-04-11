import time
import numpy as np 
import pandas as pd 
#import matplotlib.pyplot as plt
#from matplotlib.pyplot import figure
import seaborn as sns
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from pandas import read_csv
df = read_csv('text-wash6.csv', sep='delimiter', header=None)
print(df)
#print(df.text)#

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer()
## apply the TfidfVectorizer to transform the text into vectors
X = tfidf.fit_transform(df)
feature_names = tfidf.get_feature_names()
from sklearn.decomposition import NMF
n = 5
## assign variable "nmf" to the function NMF with 10 components
nmf = NMF(n_components=n)
## apply nmf to the texts transformed into TFIDF vectors
comp = nmf.fit(X)
for topic_number, topic in enumerate(comp.components_):
    print( "Topic {}:".format(topic_number))
            # gets the top words that scored the highest from TFIDF
    print( " ".join([feature_names[i] for i in topic.argsort()[:-n - 1:-1]]))
'''
X = df.drop(['class'], axis = 1)
Y = df['class']
X = pd.get_dummies(X, prefix_sep='_')
Y = LabelEncoder().fit_transform(Y)
X = StandardScaler().fit_transform(X)
'''