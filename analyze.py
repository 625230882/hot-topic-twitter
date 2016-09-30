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
import word_processor
from nb import NB

alpha = 0.1
beta = 0.1
K = 5
iter_num = 10
top_words = 5

class Document(object):
    def __init__(self):
        self.words = []
        
class Dataset(object):
    def __init__(self):
        self.M = 0 # number of documents
        self.V = 0 # number of words
        self.docs = []
        self.wordId = {} # "word": "id" dictionary
        self.idWord = {} # "id": "word" dicttionary
        
    def dumpToDisk(self, filename):
        with open(filename, "w") as file:
            for word, id in self.wordId.items():
                file.write(word + "," + str(id) + "\n")

class LdaModel(object):
    def __init__(self, dataset,file_time):
        self.dset = dataset
        self.topicfile = open("lda_topics.txt","a")
        self.file_time = file_time
        self.topicfile.write(file_time+'\n')
        self.p = [] # store the temporary sample value
        self.Z = [] # distribution of the topic
        self.nw = [] # distribution of word i on topic j
        self.nwsum = [] # num of words belong to topic i
        self.nd = []
        self.ndsum = []
        self.theta = []
        self.phi = []
        
        self.K = K 
        self.alpha = alpha # by defaut
        self.beta = beta
        self.iterates = iter_num
        self.top_words = top_words # number of words for one topics

    def init_est(self):
        self.p = [0.0 for x in xrange(self.K)]
        self.nw = [ [0 for y in xrange(self.K)] for x in xrange(self.dset.V) ]
        self.nwsum = [ 0 for x in xrange(self.K)]
        self.nd = [ [ 0 for y in xrange(self.K)] for x in xrange(self.dset.M)]
        self.ndsum = [ 0 for x in xrange(self.dset.M)]
        self.Z = [ [] for x in xrange(self.dset.M)]
        for x in xrange(self.dset.M):
            self.Z[x] = [0 for y in xrange(self.dset.docs[x].length)]
            self.ndsum[x] = self.dset.docs[x].length
            for y in xrange(self.dset.docs[x].length):
                topic = random.randint(0, self.K - 1)
                self.Z[x][y] = topic
                self.nw[self.dset.docs[x].words[y]][topic] += 1
                self.nd[x][topic] += 1
                self.nwsum[topic] += 1
        self.theta = [ [0.0 for y in xrange(self.K)] for x in xrange(self.dset.M) ]
        self.phi = [ [ 0.0 for y in xrange(self.dset.V) ] for x in xrange(self.K)]

    def init_data(self):
        i=0
        for x in xrange(self.dset.M):
            for y in xrange(self.dset.doc[x].length):
                self.z.append([])
                self.nw.append([])
                self.nd.append([])
                for z in xrange(self.K):
                        self.nwsum.append(0)
                        self.nd[x].append([])
                        self.nw[i].append([])
                topic = random.randint(0 , self.K-1)
                self.z[x].append(topic)
                self.nw[i][topic] +=1
                self.nd[x][topic] +=1
                self.nwsum[topic] +=1 
                i +=1      
        self.theta = [[0.0 for y in xrange(self.K)] for x in xrange(self.dset.M)]
        self.phi = [[0.0 for y in xrange(self.dset.V)] for x in xrange(self.K)]

    def estimate(self):
        print 'Sampling %d iterations!' % self.iterates
        for x in xrange(self.iterates):
            # print 'Iteration %d ...' % (x+1)
            for i in xrange(len(self.dset.docs)):
                for j in xrange(self.dset.docs[i].length):
                    topic = self.sampling(i, j)
                    self.Z[i][j] = topic
        print 'End sampling.'
        print 'Compute theta...'
        self.compute_theta()
        print 'Compute phi...'
        self.compute_phi()
        print 'Saving model...'
        self.save_model()

    # Gibbs LDA
    def sampling(self, i, j):
        topic = self.Z[i][j]
        wid = self.dset.docs[i].words[j]
        self.nw[wid][topic] -= 1
        self.nd[i][topic] -= 1
        self.nwsum[topic] -= 1
        self.ndsum[i] -= 1

        Vbeta = self.dset.V * self.beta
        Kalpha = self.K * self.alpha

        for k in xrange(self.K):
            self.p[k] = (self.nw[wid][k] + self.beta)/(self.nwsum[k] + Vbeta) * \
                        (self.nd[i][k] + alpha)/(self.ndsum[i] + Kalpha)
        for k in range(1, self.K):
            self.p[k] += self.p[k-1]
        u = random.uniform(0, self.p[self.K-1])
        for topic in xrange(self.K):
            if self.p[topic]>u:
                break
        self.nw[wid][topic] += 1
        self.nwsum[topic] += 1
        self.nd[i][topic] += 1
        self.ndsum[i] += 1
        return topic

    def compute_theta(self):
        for x in xrange(self.dset.M):
            for y in xrange(self.K):
                self.theta[x][y] = (self.nd[x][y] + self.alpha) \
                                   /(self.ndsum[x] + self.K * self.alpha)

    def compute_phi(self):
        for x in xrange(self.K):
            for y in xrange(self.dset.V):
                self.phi[x][y] = (self.nw[y][x] + self.beta)\
                                 /(self.nwsum[x] + self.dset.V * self.beta)

    def save_model(self):
        result = []
        if self.top_words > self.dset.V:
            self.top_words = self.dset.V
        for x in xrange(self.K):
            topics = []
            # ftwords.write('Topic '+str(x)+'th:\n')
            topic_words = []
            for y in xrange(self.dset.V):
                topic_words.append((y, self.phi[x][y]))
            #quick-sort
            topic_words.sort(key=lambda x:x[1], reverse=True)
            for y in xrange(self.top_words):
                word = self.dset.idWord[topic_words[y][0]]
                self.topicfile.write(word+",")
                topics.append(word)
            result.append(topics)
            self.topicfile.write('\n')
        return result
        
class Analysis(object):
    def __init__(self, filename, threshold = 10000):
        processor = WordProcessor()
        file = open(filename)
        i = 0
        frequency = defaultdict(int)
        self.status_texts = []
        self.threshold = threshold
        for line in file:
            if i < self.threshold:
                line = json.loads(line)
                # ignore tweets that have the "delete" key
                # "delete" key indicates that the tweet is deleted
                if "delete" not in line:
                    cleaned = processor.cleanTweet(processor.extractNouns(line["text"]))
                    if cleaned != '':
                        self.status_texts.append(cleaned)
                        i += 1
                    else:
                        continue
            # When i reach the threshold (which is maximum_item)
            else:
                for text in self.status_texts:
                    for token in text.split():
                        frequency[token] += 1
                
                self.status_texts = [[token for token in text.split() if frequency[token] > 1] 
                                for text in self.status_texts]
                self.status_texts = [text for text in self.status_texts if text != []]
                
                i = 0
                # self.status_texts
                # status_texts = []
                break

class run(object):
    def __init__(self,file_name,file_time):
        filename = str(file_name) # local data file
        start_time = time.time()
        print("--- start at: %s ---" % (start_time))
        print 'Reading train data...'
        dset = Dataset()
        nbdata = []
        with open(filename,'r') as f:
            docs = f.readlines()
        items_idx = 0
        processor = word_processor.WordProcessor()
        for line in docs :
            temp = json.loads(line)
            if "delete" in temp: continue
            if "lang" in temp:
                if temp["lang"] != "en": continue
            if "text" not in line: continue
            tmp = processor.cleanTweet(processor.extractNouns(temp["text"]))
            if tmp != "":
                nbdata.append(tmp)
                doc = Document()
                tmp = tmp.split()
                for item in tmp:
                    if dset.wordId.has_key(item):
                        doc.words.append(dset.wordId[item])
                    else:
                        dset.wordId[item] = items_idx
                        dset.idWord[items_idx] = item
                        doc.words.append(items_idx)
                        items_idx += 1
                doc.length = len(tmp)
                dset.docs.append(doc)
            else:
                pass
        dset.M = len(dset.docs)
        dset.V = len(dset.wordId)
        print 'There are %d documents' % dset.M
        print 'There are %d items' % dset.V
        model = LdaModel(dset,file_time)
        model.init_est()
        model.estimate()
        nb = NB()
        categories =nb.ana(nbdata)
        aafile = open("./nbData/categories.txt","a")
        news = 0
        comm = 0
        memes = 0
        ongoing = 0
        for item in categories:
            if item == "news" :
                news +=1
            if item == "comm" :
                comm +=1
            if item == "memes" :
                memes +=1
            if item == "ongoing" :
                ongoing +=1
        aafile.write("time=" + file_time+'\n'+"news="+str(news)+";"+"comm="+str(comm)+";"+"memes="+str(memes)+";"+"ongoing="+str(ongoing)+'\n')
        aafile.close()
        # print categories
        print("--- %s seconds ---" % (time.time() - start_time))
