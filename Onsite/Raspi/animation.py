import serial
import time
import platform

from random import randrange, choice

from Packet import Packet
from LedMatrix import LedMatrix
from LedStrand import LedStrand

from helper_functions import get_available_ports
from data_manager import get_latest_data

NUM_PIXELS = 57

BAUD_RATE = 115200
TIMEOUT = 1

def map_values(value, i_start, i_stop, o_start, o_stop): 
    return o_start + (o_stop - o_start) * ((value - i_start) / (i_stop - i_start))

def get_new_packet(word_list):
    """
    Creates a new data packet to be used in MurmurWall
    """
    red = chr(randrange(0, 255))
    green = chr(randrange(0, 255))
    blue = chr(randrange(0, 255))
    bright = 255
    text = choice(word_list).upper().encode('ascii', 'ignore') + '\n'
    length = len(text)
    speed = int(map_values(float(ord(red)), 0.0, 255.0, 1.0, 6.0))
    cur_pos = 56
    tar_pos = 1
    displaying = False
    return Packet(length, speed, red, green, blue, bright, text, cur_pos, tar_pos, displaying)

def get_next_available_matrix():
    """
    Returns the next available matrix in MurmurWall
    """
    return 0

def get_latest_words():
    """
    Returns a list of latetest cool guy words
    """
    data = get_latest_data()

    for topic in data:
        word_list = [word for word in data[topic]["Top searches for"]]

    return word_list

def get_ports():
    """
    Returns the correct ports to be used by the hardware
    """
    current_ports = get_available_ports()
    print '\nCurrent Ports are : \n'
    print current_ports
    print ''
    
    for i in range(0, 2):
        if platform.system() == "Darwin":
            pos = 2+i
        else:
            pos = i
        port = serial.Serial(current_ports[pos], BAUD_RATE, timeout=TIMEOUT)
        time.sleep(0.116)
        port.flushInput()
        port.flushOutput()
        port.write('#')
        time.sleep(0.216)
        out = ''
        while port.inWaiting() > 0:
            out += port.read(1)
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

    return led_port, matrix_port

def animate(packets, led_strand, word_list, led_matrices):
    """
    The animation begins by drawing the previous state, and then updating.
    i.e, it draws each atom at the position determined by the previous iteration
    and then procedes to determine its next position
    """
    while True:
        
        to_remove = []
        
        for packet in packets:

            led_strand.clear_state()
            
            if not packet.text_being_displayed:
                
                strands = packet.length/2
                
                for i in range(1, strands):
                    
                    if 3 * (packet.current_position - i) >= 0:
                        led_strand.color_state[3 * (packet.current_position - i)] = chr(int(float(ord(packet.red))/i*2))
                        led_strand.color_state[3 * (packet.current_position - i) + 1] = chr(int(float(ord(packet.green))/i*2))
                        led_strand.color_state[3 * (packet.current_position - i) + 2] = chr(int(float(ord(packet.blue))/i*2))

                    if 3 * (packet.current_position + i) < (3*(NUM_PIXELS - 1)) - 2:
                        led_strand.color_state[3 * (packet.current_position + i)] = chr(int(float(ord(packet.red))/i*2))
                        led_strand.color_state[3 * (packet.current_position + i) + 1] = chr(int(float(ord(packet.green))/i*2))
                        led_strand.color_state[3 * (packet.current_position + i) + 2] = chr(int(float(ord(packet.blue))/i*2))          

                led_strand.color_state[3*packet.current_position] = packet.red
                led_strand.color_state[3*packet.current_position + 1] = packet.green
                led_strand.color_state[3*packet.current_position + 2] = packet.blue



                packet.current_position -= packet.speed
                
                if packet.current_position <= packet.target_position:
                    
                    if packet.target_position is 0:
                        #print 'toRemove'
                        to_remove.append(packet)
                        new_packet = get_new_packet(word_list)
                        packets.append(new_packet)
                        led_matrices[new_packet.target_position].packet = new_packet
                    else:
                        packet.text_being_displayed = True
                        led_matrices[packet.target_position].is_showing_packet = True
                        led_matrices[packet.target_position].update_hardware()
            else:
                led_strand.color_state[3*packet.current_position] = chr(0)
                led_strand.color_state[3*packet.current_position + 1] = chr(0)
                led_strand.color_state[3*packet.current_position + 2] = chr(0)
                # need to make this array to include the pod.......

        # send the new state to the the LED teensy
        led_strand.update_hardware()        
        
        # listen for responses from the matrices
        for led_matrix in led_matrices.values():
            if led_matrix.is_showing_packet:
                if led_matrix.is_finished():
                    led_matrix.is_showing_packet = False
                    led_matrix.packet.text_being_displayed = False
                    led_matrix.packet.target_position = get_next_available_matrix() 
                    led_matrix.packet = None
        
        for packet in to_remove:
            packets.remove(packet)
            print 'removed'

        time.sleep(0.116)


def main():
    """
    main thread for MurmurWall
    """
    word_list = get_latest_words()

    packets = [get_new_packet(word_list) for i in range(1)]

    led_port, matrix_port = get_ports()

    led_matrices = {1: LedMatrix(False, matrix_port, packets[0], 1)}

    led_strand = LedStrand(led_port)

    animate(packets, led_strand, word_list, led_matrices)


if __name__ == "__main__":
    print 'running main animation...'
    main()
