from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import pymongo
from pymongo import Connection 
import credentials
import json
import jsonpickle
import re

#credentials for Twitter OAuth 
CONSUMER_KEY = credentials.CONSUMER_KEY
CONSUMER_SECRET = credentials.CONSUMER_SECRET
ACCESS_TOKEN = credentials.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = credentials.ACCESS_TOKEN_SECRET

#Mongo connection
conn = pymongo.Connection('localhost', 27017)
db = conn['tweetDB']


class StdOutListener(StreamListener):
  
    #tweets and Mongo
    def on_status(self, status):
       
       #readable date for tweets
       date = status.created_at.date().strftime("20%y/%m/%d") 
       
       #print text of tweets
       print status.text       
       
       #store the whole tweet object by emoticon
       if re.search('(:\))', status.text):
          data = json.loads(jsonpickle.encode(status))
          db.tweets.save({"smiley": ":)", "Date": date, "tweet": data})
       elif re.search('(:\()', status.text):
          data = json.loads(jsonpickle.encode(status))
          db.tweets.save({"sad": ":(", "Date": date, "tweet": data})
       else:
          data = json.loads(jsonpickle.encode(status))
          db.tweets.save({"neutral": ":|", "Date": date, "tweet": data})      

    #count the number of tweets in database and print it
    smiley_count = db.tweets.find({"smiley": ":)"}).count()
    sad_count = db.tweets.find({"sad": ":("}).count()
    neutral_count = db.tweets.find({"neutral": ":|"}).count()
    total_count = db.tweets.count()
    print "Total number of tweets: ", total_count
    print "Smiley ", smiley_count
    print "Sad ", sad_count
    print "Neutral ", neutral_count

    #error handling
    def on_error(self, error):
        print error 
    
     


if __name__ == '__main__':
    listener = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET )
    stream = Stream(auth, listener)    
    stream.filter(track=[':)', ':(', ':|'])
      