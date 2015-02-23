import time
import pprint
import requests
import json
import threading

def get_latest_data():
    """ Input: JSON file of trending words and related terms and conversation
        Does: Manages network of teensies, LEDs, runs animation 
    """

    #Uncomment to run every 10 min.
    #threading.Timer(900.0, main).start()
    print '\nLoading backup data file.....\n'

    with open('/home/pi/FutureCities/MurmurWall/Onsite/Raspi/Backup/backup.json') as backup_json_file:    
        current_json = json.load(backup_json_file)

    print 'Backup data: \n'
    pprint.PrettyPrinter(indent=4).pprint(current_json)

    print '\nRequesting new data.....\n'
    response = requests.get("https://api.myjson.com/bins/2csub")
    
    if response.status_code is 200:
        print 'Success (200) in downloading data\n'
        current_json = response.json()
        print 'Backing up data\n'
        with open('/home/pi/FutureCities/MurmurWall/Onsite/Raspi/Backup/backup.json', 'w') as backup_json:
            json.dump(current_json, backup_json)
    else: 
        print 'Error (' + response.status_code + ') was a problem getting the data\n'
        print 'Using backup.json'

    print 'Current data: \n'
    pprint.PrettyPrinter(indent=4).pprint(current_json)
    print '\n'

    return current_json

def main():
    """ Input: JSON file of trending words and related terms and conversation
        Does: Manages network of teensies, LEDs, runs animation 
    """
    get_latest_data()


if __name__ == "__main__":
    print 'Starting raspberry thread'
    main()
