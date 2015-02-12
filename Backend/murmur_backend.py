from pyGTrends import pyGTrends
import time
from random import randint

import requests
import json
from collections import defaultdict

from requests_oauthlib import OAuth1Session

import re

CONSUMER_KEY = "fJuMgEGE2JOopxUqZWrCJMKK4"
CONSUMER_SECRET = "BsLB6rbnCVXHYPMQ5StI740K2yYO2nBliZXiyWId4cspMVjzAh"
ACCESS_TOKEN = "2375964139-76Bx8t2z3ZcZBIrKF7ubq6QOXt0D6gYWGcF4ZYn"
ACCESS_SECRET = "yhbYtNonmq5aBeqanmraKed4Je9lhH2jLASWuwZpHdybv"

PATH = "CSV/"

def get_current_trends():
    """Returns the current trends from Google Search"""

    print("Updating Trends.......\n")
    google_request = requests.get('http://hawttrends.appspot.com/api/terms/')
    return {x: [] for x in google_request.json()["1"]}

def get_twitter_responses(trends):
    """Updates each trend with responses from Twitter"""

    print('Getting Twitter Information:\n')
    twitter_session = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    for trend, related_terms in trends.items():
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

def get_google_trends_responses(trends):
    """Updates each trend with related searches from Google"""

    print('\nGetting Google Trends Information:\n')
    for trend, relates_terms in trends.items():
        connector = pyGTrends("collinschupman@gmail.com", "b33fC0mm@nd0")
        connector.request_report(trend)
        time.sleep(randint(10, 20))
        connector.save_csv(PATH, trend)
        current_csv_file = open(PATH + trend + '.csv')
        result = defaultdict(dict)
        current_key = ""
        db_key = ""
        ignore_next = False
        for line in current_csv_file:
            line = line.strip()
            if line == "":
                current_key = ""
                continue
            if current_key == "":
                current_key = line
                ignore_next = True
                continue
            if ignore_next:
                ignore_next = False
                continue
            data = line.split(",")
            result[current_key][data[0]] = data[1]
            if "Top searches for" in current_key:
                db_key = current_key
        current_csv_file.close()
        if db_key is not '':
            for name in result[db_key].keys():
                new_name = name
                if trend in name:
                    new_name = name.replace(trend, '').lstrip()
                elif trend.lower() in name: 
                    new_name = name.replace(trend.lower(), '').lstrip()
                relates_terms.append(new_name)

def main():
    """Ouputs: JSON file of trending words and related terms and conversation"""

    print("\nStarting backend thread.........\n")

    #Un-comment to run this script every 10 minutes......
    #threading.Timer(900.0, main).start()
    
    # UPDATE TRENDS
    # trends = get_current_trends()

    # # TWITTER
    # #get_twitter_responses(trends)

    # # GOOGLE TRENDS
    # get_google_trends_responses(trends)

    # # WRITE TO FILE
    # print("Writing to 'data.json'\n")

    # print(trends)

    # with open('../Frontend/Processing/sketch_four/data/data.json', 'w') as outfile:
    #     json.dump(trends, outfile)

    r = requests.get("https://api.myjson.com/bins/2csub")
    to_go = r.json()
    print(type(str(to_go)))

    headers = {'Content-type': 'application/json'}
    s = requests.put("https://api.myjson.com/bins/2csub", data = json.dumps(to_go), headers = headers)
    print(s)

    # json_data = open('../Frontend/Processing/sketch_four/data/data.json')
    # data = json.load(json_data)
    # r = requests.post("https://api.myjson.com/bins/2csub", data=json.dumps(data))
    # json_data.close()
    # print(r)

    print("\nFinished!!!!!!!\n")

if __name__ == "__main__":
    main()