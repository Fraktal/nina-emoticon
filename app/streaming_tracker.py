from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import pymongo
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
        # Prints the text of the tweet
       date = status.created_at.date().strftime("20%y/%m/%d") 
       print(date + ' Tweet: ' + status.text)


    def on_error(self, error):
        print error 


    def handle_data(self, status):
        try:
            string_buffer = StringIO(status)
            tweets = json.load(string_buffer) 
        except Exception as ex:
            print "Exception occurred: %s" % str(ex)
        try:
            self.raw_tweets.insert(tweets)
        except Exception as ex:
            print "Exception occurred: %s" % str(ex)  




if __name__ == '__main__':
    listener = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET )
    stream = Stream(auth, listener)    
    stream.filter(track=[':)', ':(', ':|'])
      