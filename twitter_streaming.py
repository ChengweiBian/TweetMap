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

keywords = ['love', 'great', 'happy', 'excited', 'wonderful', 'good', 'bad', 'no', 'work', 'sad']


# This is a basic listener that just prints received tweets to stdout
class StdOutListener(StreamListener):

	def on_error(self, status):
		#print status
		if status_code == 420:
		#returning False in on_data disconnects the stream
			return False
	
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
				for key in keywords:
					if key in tweet['text']:
						es.index(index = 'twitter', doc_type = 'tweet', body = {
							'keyword': key,
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
	#es = Elasticsearch()
	#es.indices.delete(index='twitter', ignore=[400, 404])
	es = Elasticsearch(['https://search-tweetmap-6c2ha6a5qww6zywmv7kxhj3gx4.us-east-1.es.amazonaws.com',])
	if not es.indices.exists(index='twitter'):
		es.indices.create(index='twitter', body={
        	'mappings': {
            	'tweet': {
                	'properties': {
                		"keyword": {
                    		"type": "string",
                		},
                    	"location": {
                        	"type": "geo_point"
                    	},
                    	"user": {
                        	"type": "string"
                    	},
                    	"time": {
                    		"type": "string"
                    	},
                    	"text": {
                    		"type": "string"
                		}
                	}
            	}
        	}
        })

	# This handles Twitter authetification and the connection to Twitter Streaming API
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)
	stream.filter(track = keywords)

