from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.datasets import load_files
import json as simplejson
import argparse
import cmd




class NB(object):
  def ana(self,message):
    data =load_files('./train')
    #print len(data.filenames)

    categories = data.target_names

    #for t in data.target[:10]:
    #print(data.target_names[t])

    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(data.data)
    #print X_train_counts.shape


    tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
    X_train_tf = tf_transformer.transform(X_train_counts)
    X_train_tf.shape

    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    X_train_tfidf.shape

    clf = MultinomialNB().fit(X_train_tfidf, data.target)

    docs_new = message
    res = []
    X_new_counts = count_vect.transform(docs_new)
    X_new_tfidf = tfidf_transformer.transform(X_new_counts)
    predicted = clf.predict(X_new_tfidf)

    for doc, category in zip(docs_new, predicted):
        res.append(data.target_names[category])
    return res