import time
import glob
import serial
import pprint
import requests
import json
import threading

BAUD_RATE = 9600

def get_available_ports():
    print '\nHere are the available ports : \n'
    pprint.PrettyPrinter(indent=4).pprint(glob.glob('/dev/tty[A-Za-z]*'))
    return glob.glob('/dev/tty[A-Za-z]*')

def main():
    """ Input: JSON file of trending words and related terms and conversation
        Does: Manages network of teensies, LEDs, runs animation 
    """

    #Uncomment to run every 10 min.
    #threading.Timer(900.0, main).start()

    print '\nGetting Teensy Ports......\n'

    teensy_ports = [get_available_ports()[x] for x in range(0, 6)]

    print '\nHere are the teensy ports : \n'
    pretty_printer.pprint(teensy_ports)

    print '\nOpening ports.......\n'

    serial_ports = [serial.Serial(port_name, BAUD_RATE, timeout=1) for port_name in teensy_ports]

    print 'Serial ports succesfully opened!\n'

    print '\nLoading backup data file.....\n'
    with open('Backup/backup.json') as backup_json_file:    
        current_json = json.load(backup_json_file)

    print 'Backup data: \n'
    pprint.PrettyPrinter(indent=4).pprint(current_json)

    print '\nRequesting new data.....\n'
    response = requests.get("https://api.myjson.com/bins/2csub")
    
    if response.status_code is 200:
        print 'Success (200) in downloading data\n'
        current_json = response.json()
        print 'Backing up data\n'
        with open('Backup/backup.json', 'w') as backup_json:
            json.dump(current_json, backup_json)
    else: 
        print 'Error (' + response.status_code + ') was a problem getting the data\n'
        print 'Using backup.json'

    print 'Current data: \n'
    pprint.PrettyPrinter(indent=4).pprint(current_json)
    print '\n'

    # print 'Starting main loop....\n'

    # user_input = 'Y'
    # while user_input is 'Y':
    #     for port in serial_ports:
    #         print "Writing 'a' to " + port.port + '.........\n'
    #         port.write('a')
    #         time.sleep(2)
    #         out = ''
    #         print 'Recieving from ' + port.port + '...'
    #         while port.inWaiting() > 0:
    #             out += port.read(1)
    #         if out is not '':
    #             print '>> ' + out
    #             print ''
    #         time.sleep(5)
    #     print 'Again?'
    #     user_input = raw_input(">> ")
    #     print ''

    # print 'Closing serial ports....\n'

    # for serial_port in serial_ports:
    #     serial_port.close()

    # print 'Serial ports successfully closed!\n'

    # print 'Goodbye, have a nice day!\n'

if __name__ == "__main__":
    print 'Starting raspberry thread'
    main()
