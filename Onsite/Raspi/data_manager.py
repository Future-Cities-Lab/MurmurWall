"""
Module provides functions for managing MURMURWALL data
"""

from requests import get, ConnectionError 
from json import load, dump
from platform import system

def set_backup_data(current_json):
    """
    Takes latests JSON data loaded from the Server and saves it to disk
    """
    print '\nBacking up data\n'
    if system() == "Darwin":
        backup_location = 'Backup/backup.json'
    else:
        backup_location = '/home/pi/FutureCities/MurmurWall/Onsite/Raspi/Backup/backup.json'
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
        backup_file = '/home/pi/FutureCities/MurmurWall/Onsite/Raspi/Backup/backup.json'  
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

def main():
    """ 
    Used to test this module

    """
    print get_latest_data()


if __name__ == "__main__":
    main()
