import serial
import time
import platform

from random import randrange, choice

from Packet import Packet
from LedMatrix import LedMatrix
from LedStrand import LedStrand

from helper_functions import get_available_ports, my_range
from data_manager import get_latest_data

NUM_PIXELS = 57

BAUD_RATE = 115200
TIMEOUT = 1

def get_new_packet(word_list):
    """
    Creates a new data packet to be used in MurmurWall
    """
    length = 5
    speed = 1
    red = chr(randrange(0, 255))
    green = chr(randrange(0, 255))
    blue = chr(randrange(0, 255))
    bright = 255
    text = choice(word_list).upper().encode('ascii','ignore') + '\n'
    cur_pos = 0
    tar_pos = 28
    displaying = False
    return Packet(length, speed, red, green, blue, bright, text, cur_pos, tar_pos, displaying)

def get_next_available_matrix():
    """
    Returns the next available matrix in MurmurWall
    """
    return 56

def main():
    """
    Runs the main thread for MurmurWall
    """
    data = get_latest_data()

    for topic in data:
        word_list = [word for word in data[topic]["Top searches for"]]

    packets = []
    packets.append(get_new_packet(word_list))

    current_ports = get_available_ports()
    print '\nCurrent Ports are : \n'
    print current_ports
    print ''

    # if platform.system() == "Darwin":
    #     led_port = serial.Serial(current_ports[2], BAUD_RATE, timeout=TIMEOUT)
    #     matrix_port = serial.Serial(current_ports[3], BAUD_RATE, timeout=TIMEOUT)
    # else:
    #     led_port = serial.Serial(current_ports[0], BAUD_RATE, timeout=TIMEOUT)
    
    if platform.system() == "Darwin":
        for i in range(0, 2):
            port = serial.Serial(current_ports[2+i], BAUD_RATE, timeout=TIMEOUT)
            port.write('#')
            time.sleep(0.116)
            out = ''
            while port.inWaiting() > 0:
                out += port.read(1)
            if out == '04:E9:E5:01:0C:F5':
                led_port = port
            elif out == '04:E9:E5:01:0C:E0':
                matrix_port = port
    else:
        for i in range(0, 2):
            port = serial.Serial(current_ports[i], BAUD_RATE, timeout=TIMEOUT)
            port.write('#')
            time.sleep(0.116)
            out = ''
            while port.inWaiting() > 0:
                out += port.read(1)
                print out
            print out
            if out == '04:E9:E5:01:0C:F5':
                led_port = port
            elif out == '04:E9:E5:01:0C:E0':
                matrix_port = port        
    
    print '\nLED Port is : \n'
    print led_port
    print ''

    print '\nMatrix Port is : \n'
    print matrix_port
    print ''

    led_matrices = {28: LedMatrix(False, matrix_port, packets[0], 28)}

    led_strand = LedStrand(led_port)

    #Manager Algorithm-1

    while True:

         to_remove = []

         for packet in packets:
             if not packet.text_being_displayed:

                 led_strand.clear_state()

                 led_strand.color_state[3*packet.current_position] = packet.red
                 led_strand.color_state[3*packet.current_position + 1] = packet.green
                 led_strand.color_state[3*packet.current_position + 2] = packet.blue
                
                 packet.current_position += packet.speed

                 if packet.current_position is packet.target_position:
                     if packet.target_position is (NUM_PIXELS - 1):
                         to_remove.append(packet)
                         new_packet = get_new_packet(word_list)
                         packets.append(new_packet)
                         led_matrices[new_packet.target_position].packet = new_packet
                     else:
                         packet.text_being_displayed = True
                         led_matrices[packet.target_position].is_showing_packet = True
                         led_matrices[packet.target_position].update_hardware()


         # need to test method......
         led_strand.update_hardware()
        
         for led_matrix in led_matrices.values():
             if led_matrix.is_showing_packet:
                 if led_matrix.is_finished():
                     led_matrix.is_showing_packet = False
                     led_matrix.packet.text_being_displayed = False
                     led_matrix.packet.target_position = get_next_available_matrix() 
                     led_matrix.packet = None

         for packet in to_remove:
             packets.remove(packet)

         time.sleep(0.116)

if __name__ == "__main__":
    print 'running main animation...'
    main()
