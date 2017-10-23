# Important the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream 
from elasticsearch import Elasticsearch
import requests
import json


# Variables that contains the user credentials to access Twitter API
access_token = "920108859007684608-UyNMjzKK1WL67bSkbI9nx7xLX4286nV"
access_token_secret = "nvwDEdY7a6MccvKFuQQvUmwcjadVKB4B7tc6aNwxRG7aw"
consumer_key = "RKlq1R5ug0JeQooH3VgwYglXa"
consumer_secret = "xwy29DNnp8SeoUwBdivi5KvW0UWGFctqZwqTZYr9k2ak25giO6"


# This is a basic listener that just prints received tweets to stdout
class StdOutListener(StreamListener):

	def on_error(self, status):
		#print status
		pass
	
	def on_status(self, status):
		try:
			if status.coordinates:
				#print status
				tweet = {}
				tweet['user'] = status.user.screen_name
				tweet['text'] = status.text
				tweet['location'] = status.coordinates['coordinates']
				tweet['time'] = str(status.created_at)

				#Store twitter data into elasticsearch
				es.index(index = 'twitter', doc_type = 'tweet', body = {
					'user': tweet['user'],
					'text': tweet['text'],
					'location': tweet['location'],
					'time': tweet['time']
					})

				print(tweet)

		except Exception as e:
			print('Error! {0}: {1}'.format(type(e), str(e)))

if __name__ == '__main__':
	# Create elasticsearch instance
	es = Elasticsearch(['https://search-tweetmap-6c2ha6a5qww6zywmv7kxhj3gx4.us-east-1.es.amazonaws.com',])

	# This handles Twitter authetification and the connection to Twitter Streaming API
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)

	stream.filter(track = ['hungry', 'awkward', 'boring', 'sleepy', 'tired',
                             'angry', 'depressed', 'excited', 'happy', 'sad'])