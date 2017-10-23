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
    es = Elasticsearch()
    
    if message == 'Init':
        results = es.search(index="twitter", size=2000, body={ "query": { "match_all": {} } })
        print("INIT MAP")

    else:
        results = es.search(index="twitter", size=2000, body={"query": {"match": {'text':{'query': message}}}})
        print("SEARCH: " + message)
    

    # Find locations of each tweet
    data = {'location': [], 'user': [], 'time': [], 'text': []}

    for result in results['hits']['hits']:
        for key in data:
            data[key].append(result['_source'][key])

    send(json.dumps(data))


if __name__ == '__main__':
    socketio.run(application, debug=True)
