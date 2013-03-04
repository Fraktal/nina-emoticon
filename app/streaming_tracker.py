from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import pymongo
import re
from pymongo import MongoClient
from pymongo import Connection 
from pymongo.errors import ConnectionFailure
connection = MongoClient()
import credentials

 
CONSUMER_KEY = credentials.CONSUMER_KEY
CONSUMER_SECRET = credentials.CONSUMER_SECRET
ACCESS_TOKEN = credentials.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = credentials.ACCESS_TOKEN_SECRET

connection = MongoClient('localhost', 27017)
db = connection['tweet_test']
collection = db['tweet_test']

class StdOutListener(StreamListener):
  
    
    def on_status(self, status):
       date = status.created_at.date().strftime("20%y/%m/%d") 
       """
       Trying to figure out regex syntax for python. Semmy wants Mongo to store and index 
       the tweets by each Emoticon (the three below). Group the tweets by emoticon in the db.   
       """
       #smiley = re.finditer("'^:\))+$'", status.text)
       #sad = 
       #neutral = 
       
       # Prints the text of the tweet
       print(date + ' Tweet: ' + status.text)


    def on_error(self, error):
        print error 

    """
    This is my attempt at trying to handle the tweets. Basically, trying to get Mongo to save the 
    tweet stream. The whole JSON object.  
    """
    def handle_data(self, status):
        try:
            string_buffer = StringIO(status)
            tweets = json.load(string_buffer)
            i = 0
            while True:
              i = i + 1
              for tweet in tweets:
                try:
                  print ' SAVING: "%s"' % tweet['text']
                  collection.insert(tweet)
                except Exception as e:
                  print 'ERROR: %s' % e 
        except Exception as e:
           print "Exception occurred: %s" % str(e)
   


if __name__ == '__main__':
    listener = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET )
    stream = Stream(auth, listener)    
    stream.filter(track=[':)', ':(', ':|'])
      