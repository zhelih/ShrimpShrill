#!/usr/bin/python
CONSUMER_KEY    = "tmNlNUFqmZ0d3si0G5XrguslC"
CONSUMER_SECRET = "2RhhRIrrjMuM3CgoWlSWJua62XibxTlTnhUcPjo25jY3uG5IpM"
API_KEY         = "2267716710-JmsGNXgFoo31IyuFublyWLsMTRTYXoKOZCJOOlZ"
API_SECRET      = "FVuM4WBjosEkDp89mCE30sODqSjEgahk2PoBhOBcVDmST"
URL             = "http://localhost:5000/ers/post_new"

import oauth2
import json
import sys
import signal
import time
import calendar
import urllib2
import requests
from dateutil import parser

def signal_handler(signal, frame):
    print "Got Ctrl+C, bye\n"
    sys.exit(0)

def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content

def getSearchQuery(string, count, since_id = 0):
    return "https://api.twitter.com/1.1/search/tweets.json?q={}&result_type=recent&count={}&since_id={}".format(string, count, since_id)

def getSearch(string, count):
    def _():
        since_id = 0
        while True:
            result = oauth_req(getSearchQuery(string, count, since_id), API_KEY, API_SECRET)
            result = json.loads(result)['statuses']
            if result:
                since_id = result[0]['id']
            yield result
    return _()

def sendTweet(tweet):
    user = tweet['user']['screen_name']
    text = tweet['text']
    link = "https://twitter.com/{}/status/{}".format(user, tweet['id'])
    time = calendar.timegm(parser.parse(tweet['created_at']).timetuple())
    location = {}
    if tweet.get('place', None):
        if tweet['place'].get('country'):
            location["state"] = tweet['place']['country']
        if tweet['place'].get('name'):
            location["city"] = tweet['place']['name']
        if tweet['place'].get('bounding_box'):
            n = len(tweet['place']['bounding_box']['coordinates'][0])
            location['longitude'] = sum([i[0] for i in tweet['place']['bounding_box']['coordinates'][0]])/n
            location['latitude']   = sum([i[1] for i in tweet['place']['bounding_box']['coordinates'][0]])/n
    query = {"user": user, "text": text, "link": link, "date": time, "source": 0};
    if location:
        query["location"] = location
    
    header = {'content-type': 'application/json'}
    response = requests.post(URL, data = json.dumps(query), headers = header);

def sendTweets(tweets):
    try:
        for tweet in tweets:
            sendTweet(tweet)
    except requests.exceptions.ConnectionError:
        print "Looks like FishingboatBloat is down"

def run(keyword, count, timeout = 10):
    generator = getSearch(keyword, count)
    while True:
        tweets = generator.next()
        print "Got {} new tweets".format(len(tweets))
        sendTweets(tweets)
        time.sleep(timeout)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    run(sys.argv[1], int(sys.argv[2]), timeout = int(sys.argv[3]))
