# TweetMap
## General Description

* The TweetMap web application collects tweets from a live stream and processes them to display certain tweets, that contain keywords, on GoogleMaps. 

* Created a web application to process and display real-time tweets on Google Maps using Python Flask.
* Fetched tweets using Twitter Streaming APIs, and indexed tweets for searching on AWS ElasticSearch.
* Deployed the application on AWS Elastic Beanstalk in an auto-scaling environment at http://tweetmapp.us-east-1.elasticbeanstalk.com/. 
* Used ElasticSearch’s geospatial feature to shows tweets that are within a 500km radius from the point the user clicks on the map. 

## Run it on your local
* First, clone the app to your local and install the dependencies of the application.
* Then, run the application and visit the application on http://127.0.0.1:5000/
```
$ sudo pip install -r requirement.txt 
$ python application.py
```
