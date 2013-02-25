from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import credentials 

CONSUMER_KEY = credentials.CONSUMER_KEY
CONSUMER_SECRET = credentials.CONSUMER_SECRET
ACCESS_TOKEN = credentials.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = credentials.ACCESS_TOKEN_SECRET

class StdOutListener(StreamListener):
  
  
    def on_status(self, status):
        # Prints the text of the tweet
        print('Tweet: ' + status.text)      

    def on_error(self, error):
        print error 


if __name__ == '__main__':
    listener = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET )

    stream = Stream(auth, listener)    
    stream.filter(track=[':)', ':(', ':|'])  