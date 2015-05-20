"""
Copyright (c) 2015, Collin Schupman (Future Citites Lab)

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

from requests import get, ConnectionError, put 
from json import load, dump, dumps
from platform import system

def set_backup_data(current_json):
    """
    Takes latests JSON data loaded from the Server and saves it to disk
    """
    print '\nBacking up data\n'
    if system() == "Darwin":
        backup_location = 'Backup/backup.json'
    else:
        backup_location = '/home/pi/MurmurWall/Raspi/Backup/backup.json'
    with open(backup_location, 'w') as backup_json:
        dump(current_json, backup_json)


def get_backup_data():
    """
    Loads the backup JSON file to be used in this iteration of MURMURWALL 
    """
    print '\nConnection Error, Using Backup JSON File\n'
    if system() == "Darwin":
        backup_file = 'Backup/backup.json'
    else:
        backup_file = '/home/pi/MurmurWall/Raspi/Backup/backup.json'  
    with open(backup_file) as backup_json_file:    
        current_json = load(backup_json_file)
    return current_json

def get_latest_data():
    """ 
    Makes request to get latest JSON from the Server
    If there is any problem in getting the data, the script
    resorts to using the last backup JSON file for this turn.
    """
    try:
        print '\nRequesting new data.....\n'
        response = get("https://api.myjson.com/bins/2csub")
        if response.status_code is 200:
            print '\nSuccess (200) in downloading data\n'
            current_json = response.json()
            set_backup_data(current_json)
        else: 
            current_json = get_backup_data()
    except ConnectionError:
        current_json = get_backup_data()
    return current_json

def get_buzz_word():
    """ 
    Get BUZZ_WORDS
    """
    try:
        response = get("https://api.myjson.com/bins/46ec7")
        if response.status_code is 200:
            word = response.json()[0].encode('ascii', 'ignore')
            if word is '':
                word = 'fail'
            else:
                headers = {'Content-type': 'application/json'}
                put("https://api.myjson.com/bins/46ec7", data=dumps([""]), headers=headers)
            return word
        else: 
            return 'fail'
    except ConnectionError:
        return 'fail'

def get_currated_words():
    """ 
    Get currated words
    """
    try:
        response = get("https://api.myjson.com/bins/3ddib")
        if response.status_code is 200:
            words = [word.encode('ascii', 'ignore') for word in response.json()]
            return words
        else: 
            return []
    except ConnectionError:
        return []

def main():
    """ 
    Used to test this module

    """
    print get_latest_data()


if __name__ == "__main__":
    main()
