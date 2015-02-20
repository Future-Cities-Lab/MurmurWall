from pyGTrends import pyGTrends
import time
from random import randint
import pprint

import threading

import requests
import json
from collections import defaultdict

from requests_oauthlib import OAuth1Session

import re

import os
import glob

CONSUMER_KEY = "fJuMgEGE2JOopxUqZWrCJMKK4"
CONSUMER_SECRET = "BsLB6rbnCVXHYPMQ5StI740K2yYO2nBliZXiyWId4cspMVjzAh"
ACCESS_TOKEN = "2375964139-76Bx8t2z3ZcZBIrKF7ubq6QOXt0D6gYWGcF4ZYn"
ACCESS_SECRET = "yhbYtNonmq5aBeqanmraKed4Je9lhH2jLASWuwZpHdybv"

PATH = "CSV/"

JSON_URL = "https://api.myjson.com/bins/2csub"

def get_current_trends():
    """Returns the current trends from Google Search"""
    google_request = requests.get('http://hawttrends.appspot.com/api/terms/')
    return [x for x in google_request.json()["1"]]

def get_twitter_responses(trends):
    """Updates each trend with responses from Twitter"""
    twitter_session = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    for trend in trends:
        print('Getting responses for trend - ' + trend)
        url = "https://api.twitter.com/1.1/search/tweets.json?q="
        url += trend
        url += "&lang=en&geocode=37.781157,-122.398720,2000mi&count=20"
        twitter_responses = twitter_session.get(url).json()["statuses"]
        for twitter_response in twitter_responses:
            edited_twitter_response = twitter_response["text"]
            hash_tags = re.findall(r'#\w*', edited_twitter_response)
            for tag in hash_tags:
                edited_twitter_response = edited_twitter_response.replace(tag, "").strip()
            at_symbols = re.findall(r'@\w*', edited_twitter_response)
            for at_symbol in at_symbols:
                edited_twitter_response = edited_twitter_response.replace(at_symbol, "").strip()
            webs = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',edited_twitter_response)
            for web in webs:
                edited_twitter_response = edited_twitter_response.replace(web, "").strip()
            related_terms.append(edited_twitter_response)

def get_google_trends_responses(trends,new_trends):
    """Updates each trend with related searches from Google"""

    to_remove = []

    files = glob.glob(PATH + '*')
    for fil in files:
        os.remove(fil)

    for trend in trends:
        connector = pyGTrends("collinschupman@gmail.com", "b33fC0mm@nd0")

        try:
            connector.request_report(trend)
        except URLError:
            print 'Bummer'

        time.sleep(randint(10, 20))
        connector.save_csv(PATH, trend)

        cvs_file = open(PATH + trend + '.csv')
        result = defaultdict(dict) #dictionary holding the data
        current_key = "" #current category
        ignore_next = False #flag to skip header
       
        for line in cvs_file:
            line = line.strip() #throw away newline
            if line == "": #line is empty
                current_key = ""
                continue
            if current_key == "": #current_key is empty
                current_key = line #so the current line is the header for the following data
                ignore_next = True
                continue
            if ignore_next: #we're in a line that can be ignored
                ignore_next = False
                continue
            data = line.split(",")
            if "Top searches for" in current_key:
                name = data[0]
                if trend in data[0]:
                    name = data[0].replace(trend, '').lstrip()
                elif trend.lower() in data[0]: 
                    name = data[0].replace(trend.lower(), '').lstrip()
                result["Top searches for"][name] = data[1]
       
        cvs_file.close()
       
        if not bool(result):
            to_remove.append(trend)
        else:
            new_trends[trend] = result

    for trend in to_remove:
        new_trends.pop(trend, None)

    with open('Backup/backup.json', 'w') as backup_json_file:    
        json.dump(new_trends, backup_json_file) 

def main():
    """Ouputs: JSON file of trending words and related terms and conversation"""

    #Un-comment to run this script every 10 minutes......
    #threading.Timer(900.0, main).start()

    print('\nLoading backup data.....\n')
    with open('Backup/backup.json') as backup_json_file:    
        to_go_json = json.load(backup_json_file)

    
    # UPDATE TRENDS * HOW TO ERROR CHECK?
    print("Updating current trends.......\n")
    trends = get_current_trends()

    twitter_session = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    twitter_url = "https://api.twitter.com/1.1/trends/place.json?id=2487956"
    twitter_responses = twitter_session.get(twitter_url).json()
    for trend in twitter_responses[0]['trends']:
        word = trend['name']
        if word[0] is '#':
            word = word[1:]
        trends.append(word)

    # TWITTER * HOW TO ERROR CHECK?
    # print('Getting Twitter Information:\n')
    # get_twitter_responses(trends)

    # GOOGLE TRENDS * HOW TO ERROR CHECK?
    print('Getting trending information......\n')
    new_trends = {}
    get_google_trends_responses(trends, new_trends)

    to_go_json = new_trends

    print('\nNew JSON is ready : \n')
    pretty_printer = pprint.PrettyPrinter(indent=4)
    pretty_printer.pprint(to_go_json)

    # WRITE TO WEB * HOW TO ERROR CHECK? *** MAYBE TRY 10X or so?
    print('\nUploading to https://api.myjson.com/bins/2csub.....\n')

    headers = {'Content-type': 'application/json'}
    response = requests.put(JSON_URL, data=json.dumps(to_go_json), headers=headers)
    
    if response.status_code is 200: 
        print("200 Success!\n")
    else:  
        print('Failure ' + response.status_code + '\n')

    print("Finished!!!!!!!\n")

if __name__ == "__main__":
    print("\nStarting backend thread.........\n")
    main()
