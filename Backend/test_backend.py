from __future__ import absolute_import, print_function

from pyGTrends import pyGTrends
import time
from random import randint
import csv
import sys

import requests
import json
from collections import defaultdict
import sqlite3


        #TODO: setup google account for project
        #setup 
        google_username = "collinschupman@gmail.com"
        google_password = "b33fC0mm@nd0"
        path = "CSV/"

        # connect to Google
        connector = pyGTrends(google_username, google_password)


        # get today's trends
        r = requests.get('http://hawttrends.appspot.com/api/terms/')

        # need to do some error testing here......
        trends = r.json()["1"]
        
        conn = sqlite3.connect('searches.db')
        c = conn.cursor()
        # get trending information for each trend trends
        for trend in trends :
                'GET Google Trend Information'

                #make request
                connector.request_report(trend)

                #wait a random amount of time between requests to avoid bot detection
                time.sleep(randint(5,10))

                #download file
                connector.save_csv(path, trend)
                print ('Saving file ' + trend + '.csv\n')

                fh = open(path + trend + '.csv')
                result = defaultdict(dict)
                current_key = ""
                db_key = ""
                ignore_next = False

                for line in fh:
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
                    (a,b) = line.split(",")
                    result[current_key][a] = b
                    if "Top searches for" in current_key:
                        db_key = current_key
                fh.close()
                if db_key is not '':
                        lis = trend.lower().split(" ")
                        newTrend = "".join(lis)
                        command = "CREATE TABLE " + newTrend + " (name text, count integer)"
                        print (command)
                        c.execute(command)
                        for name, num in result[db_key].items():
                            c.execute("INSERT INTO " + newTrend + " VALUES ('" + name + "','" + num +"')")
                            conn.commit()
        conn.close()
