from analyze import run
from twisted.internet import task
from twisted.internet import reactor
import datetime
import json
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import word_processor
import threading


consumer_key = 'dFJEu9JBEMzrgLxblEJ0yM8K1'
consumer_secret = 'CazfEDXyRx2WUlCti5zXPcWyZBYlrNAis3H2b6WHvRZ5wYzbyU'
token_key = '705923076144435200-42yGCuGLSSIZd3wB4R6Y6xSVOoZy4Te'
token_secret = 'Z9T3xq9rOaoPTdIV7E5zoeiJskEZ1TEIeLpwBNCX94hYt'

oauth = OAuth(token_key, token_secret, consumer_key, consumer_secret)

timeout = 5.0 # Sixty seconds
news = 0
ongoing = 0
memes = 0
comm = 0

def crawler(filename):
   count = 0
   try:
     print filename
     file = open("./textData/"+filename+".txt","a")
     twitter_stream = TwitterStream(auth=oauth)
     iterator = twitter_stream.statuses.sample()
     try:
         for tweet in iterator:
             if count == 100 :
                 file.close()
                 break
             file.write(json.dumps(tweet)+'\n')
             count += 1
         Analyze= threading.Thread(target=run, args=("./textData/"+filename+".txt",filename))
         Analyze.start()
     except:
          pass
   except:
     print "stop"
     pass
   return


def doWork():
    now = datetime.datetime.now()
    if now.month < 10:
        month = "0"+str(now.month)
    else:
        month = str(now.month)
    if now.minute < 10:
        minute = "0"+str(now.minute)
    else:
        minute = str(now.minute)
    if now.hour < 10:
        hour = "0"+str(now.hour)
    else:
        hour = str(now.hour)
    if now.day < 10:
        day = "0"+str(now.day)
    else:
        day = str(now.day)
    filename = str(now.year)+month+day+hour+minute   
    crawler(filename)
    pass

l = task.LoopingCall(doWork)
l.start(timeout) # call every sixty seconds

reactor.run()