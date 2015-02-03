from __future__ import absolute_import, print_function

from pyGTrends import pyGTrends
import time
from random import randint
import csv
import sys

import os

import requests
import json
from collections import defaultdict
import sqlite3
import threading

from pandas import read_csv
import tweepy
from requests_oauthlib import OAuth1Session
import json
import praw

import re

CONSUMER_KEY = "fJuMgEGE2JOopxUqZWrCJMKK4"
CONSUMER_SECRET = "BsLB6rbnCVXHYPMQ5StI740K2yYO2nBliZXiyWId4cspMVjzAh"

def create_clean_db(db_name):
    print("\nClearing " + db_name + "..........\n")

    try:
        os.remove(db_name)
    except OSError:
        pass

def get_google_connector(name, password):

    #TODO: setup google account for project
    return pyGTrends(name, password)

# def oauth_req(url, key, secret, http_method="GET", post_body = None, http_headers = None):
#     consumer = oauth.Consumer(key = CONSUMER_KEY, secret = CONSUMER_SECRET)
#     token = oauth.Token(key = key, secret = secret)
#     client = oauth.Client(consumer, token)
#     resp, content = client.request(url, "GET")
#     print resp
#     print content


# Format nicely for command line
# format names to be broken apart
def main():
    
    #Un-comment to run this script every 10 minutes......
    # threading.Timer(900.0, main).start()

    # path = "CSV/"
    # # connect to Google
    # connector = get_google_connector("collinschupman@gmail.com", "b33fC0mm@nd0")

    # # get today's trends
    # google_request = requests.get('http://hawttrends.appspot.com/api/terms/')

    # # need to do some error testing here......
    # trends = google_request.json()["1"]

    # db_name = 'searches.db'

    # create_clean_db(db_name)

    # conn = sqlite3.connect(db_name)

    # c = conn.cursor()

    # red = praw.Reddit(user_agent='murmur')
    # submissions = red.search('sanfrancisco')
    # print([str(x) for x in submissions])
    # san_fran = [str(x) for x in submissions]
    # for post in san_fran:
    #     print(post)

    #twitter shit
    access_token = "2375964139-76Bx8t2z3ZcZBIrKF7ubq6QOXt0D6gYWGcF4ZYn"
    access_secret = "yhbYtNonmq5aBeqanmraKed4Je9lhH2jLASWuwZpHdybv"
    twitter_session = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_SECRET, resource_owner_key=access_token, resource_owner_secret=access_secret)
    
    url = "https://api.twitter.com/1.1/search/tweets.json?q=Zooey Deschanel&lang=en&geocode=37.781157,-122.398720,2000mi&count=100"

    trends = twitter_session.get(url).json()["statuses"]
    for trend in trends:
        x = trend["text"]
        #print(x)
        #print(trend["text"])
        hash_tags = re.findall(r'#\w*', x)
        for tag in hash_tags:
            x = x.replace(tag,"").strip()
        ats = re.findall(r'@\w*', x)
        for at in ats:
            x = x.replace(at,"").strip()
        webs = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',x)
        for web in webs:
            x = x.replace(web,"").strip()
        print(x)
        #print(re.findall(r'#\w*', x))
        #print(' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",x).split()))
        print('')
    #print(json.dumps(trends, indent=4, sort_keys=True))

    # for trend in trends:
    #     trends_list.append(trend['name'])
    # print(trends_list)

    #get trending information for each trend trends
    # for trend in trends :
                    
    #                 print('Working with ' + trend)

    #                 'GET Google Trend Information'

    #                 #make requ`est
    #                 connector.request_report(trend)

    #                 #wait a random amount of time between requests to avoid bot detection
    #                 time.sleep(randint(5,10))

    #                 #download file
    #                 connector.save_csv(path, trend)

    #                 print ('Saving file ' + trend + '.csv\n')

    #                 fh = open(path + trend + '.csv')
    #                 result = defaultdict(dict)
    #                 current_key = ""
    #                 db_key = ""
    #                 ignore_next = False

    #                 for line in fh:
    #                         if 'Top regions for' in line:
    #                             print(line)
    #                         line = line.strip()
    #                         if line == "":
    #                                 current_key = ""
    #                                 continue
    #                         if current_key == "":
    #                                 current_key = line
    #                                 ignore_next = True
    #                                 continue
    #                         if ignore_next:
    #                                 ignore_next = False
    #                                 continue
    #                         data = line.split(",")
    #                         #(a,b) = line.split(",")
    #                         result[current_key][data[0]] = data[1]
    #                         if "Top searches for" in current_key:
    #                                 db_key = current_key
    #                 fh.close()
    #                 if db_key is not '':
    #                                 lis = trend.lower().split(" ")
    #                                 newTrend = "".join(lis)
    #                                 command = "CREATE TABLE " + newTrend + " (name text, count integer)"
    #                                 print (command)
    #                                 c.execute(command)
    #                                 print('')
    #                                 print('\nRelated Search Terms: ' + trend)
    #                                 for name, num in result[db_key].items():
    #                                         newName = name
    #                                         if trend in name:
    #                                             newName = name.replace(trend,'').lstrip()
    #                                         elif trend.lower() in name:
    #                                             newName = name.replace(trend.lower(),'').lstrip()
    #                                         print(newName)
    #                                         #c.execute("INSERT INTO " + newTrend + " VALUES ('" + name + "','" + num +"')")
    #                                         #conn.commit()
    #                                 print('\nEnd of related terms\n')
    # conn.close()

if __name__ == "__main__":
    main()