# -*- coding: utf-8 -*-
"""hw1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rUI5sbAt-d1Hn9cQb7YZ1sP6x_6DwxJJ
"""



import nltk
nltk.download('stopwords')
import numpy as np
import pandas as pd
import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

def ngrams(n,text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    tokens = [token for token in text.split(" ") if token !=""]
    ngramArr = zip(*[tokens[i:] for i in range(n)])
    return ["".join(ngram) for ngram in ngramArr]
    pass

def myTokenizeFunc(text):
    text = text.lower()
    tokenizer = RegexpTokenizer('\w+')
    tokens = tokenizer.tokenize(text)
    words = []
    for word in tokens:
      words.append(word.lower)
    
    stopWord = nltk.corpus.stop_words.words('english')
    words_nonStop = []
    for word in words:
      if word not in stopWord:
        words_nonStop.append(word)

    return words_nonStop


data=pd.read_csv('/content/drive/MyDrive/nlp-trainingdata-csv.csv', sep=',', encoding="ISO-8859-1")
data.head()

wpt = nltk.WordPunctTokenizer()
stop_words = nltk.corpus.stopwords.words('english')

def normalize_document(doc):
    doc = re.sub(r'[^a-zA-Z\s,]', '', doc, re.I|re.A)
    doc = doc.lower()
    doc = doc.strip()
    tokens = wpt.tokenize(doc)
    filtered_tokens = [token for token in tokens if token not in stop_words]
    doc = ' '.join(filtered_tokens)
    return doc

normalize_corpus = np.vectorize(normalize_document)
norm_corpus = normalize_corpus(data['City'])

#print (norm_corpus)

tv = TfidfVectorizer(min_df=0., max_df=1., norm='l2', use_idf=True, smooth_idf=True)
tv_matrix = tv.fit_transform(norm_corpus)
tv_matrix_2 = tv_matrix.toarray()
vocab = tv.get_feature_names()
pd.DataFrame(np.round(tv_matrix_2, 2), columns=vocab)
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(tv_matrix_2, data['Country'], test_size=0.3, random_state=41)


import random
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.ensemble import RandomForestClassifier
#from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
# Model Generation Using Multinomial Naive Bayes
#clf = MultinomialNB().fit(X_train, y_train)
#predicted= clf.predict(X_test)
'''
classifier = RandomForestClassifier(n_estimators=1000, random_state=0)
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

print(confusion_matrix(y_test,y_pred))
print(classification_report(y_test,y_pred))
print(accuracy_score(y_test, y_pred))

#print("Accuracy: {0}".format(accuracy_score(y_test, predicted)))
'''

from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.model_selection import KFold
from sklearn.metrics import f1_score
X = df_new.values
y = df.target.values
kfold = KFold(n_splits=10)
# Define the model
nb_multinomial = MultinomialNB()
nb_bernoulli = BernoulliNB()
# As a storage of the model's performance
def calculate_f1(model):
 metrics = []
 
 for train_idx, test_idx in kfold.split(X):
   X_train, X_test = X[train_idx], X[test_idx]
   y_train, y_test = y[train_idx], y[test_idx]
   model.fit(X_train, y_train)
   y_pred = model.predict(X_test)
   metrics.append(f1_score(y_test, y_pred))
 
 # Retrieve the mean of the result
 print("%.3f" % np.array(metrics).mean())