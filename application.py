from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from elasticsearch import Elasticsearch
import json
import requests

application = Flask(__name__)

socketio = SocketIO(application)

@application.route('/')
def hello_world():
    return render_template('TwitterMap.html')


@socketio.on('message')
def handleConnected(message):
    # use localhosted elasticsearch
    es = Elasticsearch(['https://search-tweetmap-6c2ha6a5qww6zywmv7kxhj3gx4.us-east-1.es.amazonaws.com',])
    #es = Elasticsearch();
    data = {}
    
    if message == 'Init':
        results = es.search(index="twitters", size=2000, body={ "query": { "match_all": {} } })
        print("INIT MAP")

    elif message in ['glad', 'lucky', 'happy', 'excited', 'wonderful', 'upset', 'bad', 'terrible', 'unhappy', 'sad']:
        data['key'] = message
        results = es.search(index="twitters", size=2000, body={"query": {'bool': {'must': {'match': {'keyword': message}}}}})
        print("SEARCH: " + message)

    else:
        dic = json.loads(message)
        loc = dic['location']
        if 'key' in dic:
            data['key'] = dic['key']
            results = es.search(index="twitters", size=2000, body={"query": {'bool': {
                'must': {'match': {'keyword': dic['key']}},
                'filter': {"geo_distance": {"distance":"500km",  "location": {"lat":  loc[0], "lon":loc[1] }}}}}})
            print("LOCAL SEARCH: " + dic['key'])
        else:
            results = es.search(index="twitters", size=2000, body={"query": {'bool': {
                'filter': {"geo_distance": {"distance":"500km",  "location": {"lat":  loc[0], "lon":loc[1] }}}}}})
            print("LOCAL SEARCH")
    

    # Find locations of each tweet
    data['tweets'] = []

    for result in results['hits']['hits']:
        data['tweets'].append(result['_source'])

    #print(data)

    send(json.dumps(data))


if __name__ == '__main__':
    socketio.run(application, debug=True)
