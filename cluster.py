################################################
### To classify emails
################################################

import email.parser
from email.parser import Parser
from os import listdir
from os.path import isfile, join
from csv import DictReader, DictWriter
import copy
import argparse
import numpy as np
from numpy import array
import random
import gensim
import lda

from sklearn.cluster import KMeans


from sklearn.metrics import accuracy_score
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline
import sklearn.multiclass as sk
import sklearn.feature_extraction.text as sktxt
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import NMF, LatentDirichletAllocation

kTARGET_FIELD = "Head_X_Folder"
kHEAD_FROM_FIELD = "Head_From"
kHEAD_TO_FIELD = "Head_To"
kHEAD_SUBJECT = "Head_Subject"
kBODY = "Body"
# Code to extract a particular section from raw emails.


# Custom transformer for column data extraction
class columnExtractor(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key

    def fit(self, examples, y=None):
        # return self and nothing else
        return self

    def transform(self, examples):
        # Loop over examples and return list for the key
        column = [values for d in examples for col, values in d.items() if col == self.key]
        return column


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Feature Engineering options')
    parser.add_argument('--limit', type=int, default=0.85,
                        help="Restrict training to this many examples")
    args = parser.parse_args()

    # Cast to list to keep it all in memory
    x_train = list(DictReader(open("./EmailData.csv", 'r')))
    random.shuffle(x_train)
    # Get the train data and hold out set
    train_lim = int(args.limit * len(x_train))
    print "Limit: ", train_lim

    # Get labels
    labels = []
    for line in x_train:
        if not line[kTARGET_FIELD] in labels:
            labels.append(line[kTARGET_FIELD])
    #print "13: ", labels[13]
    #print "39: ", labels[39]
    # Get y values
    y_train = array(list(labels.index(x[kTARGET_FIELD])
                         for x in x_train))

    # Get HO y values
    y_ho = array(list(labels.index(x[kTARGET_FIELD])
                         for x in x_train[train_lim:]))

    print labels
    print len(labels)

    pipeline = Pipeline([
        ('feature-union', FeatureUnion([
             ('head-from', Pipeline([('extract-column', columnExtractor(kHEAD_FROM_FIELD)),
                                       ('tf-idf', sktxt.CountVectorizer(ngram_range=(4,4), max_features=1)),
                                      ])),
             ('head-to', Pipeline([('extract-column', columnExtractor(kHEAD_TO_FIELD)),
                                        ('tf-idf', sktxt.CountVectorizer(ngram_range=(2,2), max_features=10)),
                                        ])),
            ('head-subject', Pipeline([('extract-column', columnExtractor(kHEAD_SUBJECT)),
                                 ('tokens', sktxt.CountVectorizer()),
                                  ])),
            ('body', Pipeline([('extract-column', columnExtractor(kBODY)),
                                       ('tokens', sktxt.TfidfVectorizer(smooth_idf = True, max_df=0.85,min_df=2,ngram_range=(1,2),binary = True,stop_words= "english")),
                                       ])),
        ])),
        #('Multinomial-classification', SVC(kernel='linear')) 
    ])
    
    

    # Fit the data
    matrix= pipeline.fit_transform(x_train, y_train)

    """
    # HO test
    predictions = pipeline.predict(x_train[train_lim:])
    print predictions[:10]
    print y_ho[:10]
    accuracy = accuracy_score(predictions, y_ho)
    print "Final accuracy: ", accuracy
    """


    """
    model = lda.LDA(n_topics=20, n_iter=500, random_state=1)
    model.fit(matrix)
    topic_word = model.topic_word_
    n_top_words = 20
 
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))
    """
    
    num_clusters = 5

    km = KMeans(n_clusters=num_clusters)

    km.fit(matrix)

    clusters = km.labels_.tolist()
    print(clusters)

    
