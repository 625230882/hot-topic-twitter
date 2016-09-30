import random
import json
import nltk
import re
from collections import defaultdict
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords as sw
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import os
import time

class WordProcessor(object):
    def __init__(self):
        self.lemma = WordNetLemmatizer()
        self.noun_tags = ["NN", "NNS", "NNP", "NNPS"]
        self.stopwords = sw.words('english')
        self.none_words = ["https", "http", "b", "ka", "mo", "ang", "u", "sa", "na", "amp", "aku", "e", "l", "ji", "people", \
             "life", "time", "weather", "update", "today", "day", "fuck", "shit", "nigga", "channel", "follow", "twitter"] # manually added blacklist word list

    # Remove all the stopwords and those are not actual words from the tweets
    def cleanTweet(self, tweet):
        resultwords = [word.lower() for word in tweet.split()
                       if word.lower() not in self.stopwords and wn.synsets(word)] # removes non-word
        # resultwords = [stemmer.stem(word) for word in resultwords] # stem words
        resultwords = [self.lemma.lemmatize(word) for word in resultwords] # lemmatize words
        if resultwords != []: 
            return ' '.join(resultwords)
        return ''
    
    # Extract all nouns from tweets
    def extractNouns(self, tweet):
        nouns = []
        tagged = nltk.pos_tag(word_tokenize(tweet)) # find pos tags for each word
        propernouns = [word for word, pos in tagged if pos in self.noun_tags and word not in self.none_words]
        return ' '.join(propernouns)
