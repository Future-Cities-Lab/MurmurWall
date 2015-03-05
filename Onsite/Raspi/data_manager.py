import time
import pprint
import requests
import json
import threading
import platform

def get_latest_buckets():
    """ Input: JSON file of trending words and related terms and conversation
        Does: Manages network of teensies, LEDs, runs animation 
    """

    #Uncomment to run every 10 min.
    #threading.Timer(900.0, main).start()

    #print '\nLoading backup data file.....\n'
    if platform.system() == "Darwin":
        backup_file = 'Backup/backup.json'
    else:
        backup_file = '/home/pi/FutureCities/MurmurWall/Onsite/Raspi/Backup/backup.json'  
    with open(backup_file) as backup_json_file:    
        current_json = json.load(backup_json_file)

    #print 'Backup data: \n'
    #pprint.PrettyPrinter(indent=4).pprint(current_json)

    #print '\nRequesting new data.....\n'
    response = requests.get("https://api.myjson.com/bins/2csub")
    
    if response.status_code is 200:
        #print 'Success (200) in downloading data\n'
        current_json = response.json()
        #print 'Backing up data\n'

        if platform.system() == "Darwin":
            backup_location = 'Backup/backup.json'
        else:
            backup_location = '/home/pi/FutureCities/MurmurWall/Onsite/Raspi/Backup/backup.json'
        with open(backup_location, 'w') as backup_json:
            json.dump(current_json, backup_json)
    else: 
        print 'Error (' + response.status_code + ')\n'
        print 'Using backup.json'

    #print 'Current data: \n'
    #pprint.PrettyPrinter(indent=4).pprint(current_json)
    #print '\n'

    return current_json

def main():
    """ Input: JSON file of trending words and related terms and conversation
        Does: Manages network of teensies, LEDs, runs animation 
    """
    get_latest_words()


if __name__ == "__main__":
    print 'Starting raspberry thread'
    main()
