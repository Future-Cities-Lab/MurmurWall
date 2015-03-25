#!/usr/bin/python

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

#TODO: Clean stuff when starting?

import sys

from os import execv
from itertools import repeat
from threading import Thread
from Queue import Queue
from time import time, sleep
from random import uniform, shuffle

from Packet import Packet
from LedMatrix import LedMatrix
from LedStrand import LedStrand

from port_manager import get_ports
from data_manager import get_latest_data

from color_functions import map_values, color_strand_for_packet
from color_functions import color_pod_for_packet

# How often to restart MurmurWall (seconds)
RESTART_LENGTH = 1800

# How often to add in a priority word (seconds)
PRIORITY_LENGTH = 200

# How many frames/second will MurmurWall run at
FRAMES_PER_SECOND = 30.0
SKIP_TICKS = 1000.0 / FRAMES_PER_SECOND

# How many pixels are in MurmurWall
NUM_PIXELS = 360
TOTAL_PIXELS = NUM_PIXELS

# L
START_PIX = 0
END_PIX = 299
OUT_OF_BOUNDS = 400 

# Where the LED matrices are located on the pixel strip
MATRIX_POSITIONS = [29, 69, 109, 149, 189, 229]

# Maximum speed packets will run on the LED strand
MAX_SPEED = 0.3
MIN_SPEED = 0.05

# Maximum speed packets will move on the LED matrices
MAX_SPEED_LED = 40
MIN_SPEED_LED = 50

# Maximum number of packets in MurmurWall
NUM_PACKETS = 8

BUZZ_WORDS = ['YBCA', 'YERBA BUENA', 'SF MOMA', 
              'MARKET ST. PROTOTYPING FESTIVAL', 
              'MISSION ST.', 'MURMURWALL']

def test_leds(led_strand):
    """
    Runs a single color through the entire LED strand to test the system

    Args: 
        led_strand = LED strand state to run the color through

    """
    for i in range(0, TOTAL_PIXELS):
        led_strand.clear_state()
        led_strand.color_state[3*i] = chr(255)
        led_strand.update_hardware()

def send_packet_to_matrix(packet, led_matrix):
    """
    Sends the packet to an LED matrix to be displayed

    Args:
        packet - The packet to send to the LED matrix
        led_matrix - The LEDMatrix this packet is displaying on

    """
    packet.text_being_displayed = True
    packet.current_position = packet.target_position
    text_speed = int(map_values(packet.speed, MAX_SPEED,
                                MIN_SPEED, MIN_SPEED_LED, MAX_SPEED_LED))
    color = (packet.red, packet.green, packet.blue)
    led_matrix.update_hardware(color, text_speed, packet)

def remove_packets(packets_to_remove, packets):
    """
    Removes all marked packets from MurmurWall

    Args:
        packets_to_remove - A list of packets to remove
        packets - List of all packets in MurmurWall
    """
    for packet in packets_to_remove:
        packets.remove(packet)  

def add_new_packets(num_of_packets_to_append, packets, related_terms_queue):
    """
    Adds a given number of new packets into MurmurWall

    Args:
        num_of_packets_to_append - Number of new packets to add into MurmurWall
        packets - MurmurWall's list of packets currently in the system
        related_terms_queue - Queue of words to pull from
    """
    for _ in repeat(None, num_of_packets_to_append):
        text = related_terms_queue.get()
        new_packet = Packet(uniform(MIN_SPEED, MAX_SPEED), None, text,
                            START_PIX, MATRIX_POSITIONS[0],
                            START_PIX, False, True)
        packets.append(new_packet)

# TODO: Make this safer, divide functionality up
def update_matrices(led_matrices):
    """
    Checks each LED matrix in MurmurWall to see if they're finished
    displaying a packet. If so, puts the given packet backing into MurmurWall

    Args:
        led_matrices - A dictionary of all the LED Matrices in the system
    """
    for led_matrix in led_matrices.values():
        word = led_matrix.check_status()
        if word is not '' and 'messed up':
            for packet in led_matrix.packets:
                if packet.text == word:
                    packet_to_update = packet
            led_matrix.packets.remove(packet_to_update)
            packet_to_update.text_being_displayed = False
            packet_to_update.current_position = led_matrix.position + 1.000002
            packet_to_update.prev_target_position = packet_to_update.target_position 
            packet_to_update.target_position = led_matrix.next_position 

# TODO: Could this be cleaner?
def update_packets(packets, packets_to_remove, led_strand, led_matrices):
    """
    Updates the state of each packet in the MurmurWall system.
    
    First, does some error checking to make sure a packet hasn't been caught in
    the system, if so, it marks it for removal. 
    
    If the packet is not currently being displayed on an LED Matrix,
    it updates its postion in the color state and checks if it's reached its
    destination, updating accordingingly.
    Either removing from MurmurWall or adding it back into the system.

    If the packet is being displayed on an LED matrix, it checks if it
    has finished and adds in back into the system. If not, it colors the
    associated pod and updates it's position on the pod. 

    Args:
        packets - The list of all packets currently in MurmurWall
        packets_to_remove - A list of all packets marked for removal
        led_strand - The LED Strand state
        led_matrices - A dictionary of all the LED Matrices in MurmurWall

    Returns:
        num_of_packets_to_append - Number of new packets to add into MurmurWall
    """
    num_of_packets_to_append = 0
    for packet in packets:
        if packet.is_out_of_bounds(OUT_OF_BOUNDS):
            packets_to_remove.append(packet)
            if not packet.is_special:
                num_of_packets_to_append += 1
        else:
            if not packet.text_being_displayed:
                color_strand_for_packet(led_strand.color_state, 
                                        packet.current_position,
                                        packet.red, 
                                        packet.green,
                                        packet.blue, 
                                        packet.prev_target_position,
                                        packet.target_position)
                packet.update_postion_strand()
                if packet.has_reached_target():
                    if packet.target_is_end(END_PIX):
                        packets_to_remove.append(packet)
                        if not packet.is_special:
                            num_of_packets_to_append += 1
                    else:
                        send_packet_to_matrix(packet, led_matrices[packet.target_position])
            else:
                if packet.current_position >= packet.target_position + 100.0:
                    led_matrices[packet.target_position].packets.remove(packet)
                    packet.text_being_displayed = False
                    packet.current_position = packet.target_position + 1.000002
                    packet.prev_target_position = packet.target_position 
                    packet.target_position = led_matrices[packet.target_position].next_position 
                else:
                    # color_pod_for_packet(led_strand.color_state, packet.current_position,
                    #                      packet.red, packet.green, packet.blue)
                    packet.update_postion_pod()
    return num_of_packets_to_append

def animate_mumurwall(packets, led_strand, related_terms_queue, led_matrices, emptying):
    """
    Clears previous LED state, updates all packets, checks each LED matrix
    for a response, removes and adds new packets into the system.

    Args:
       packets - A list of all active packets in MurmurWall
       led_strand - A list describing the next LED color state
       related_terms_queue - A queue of all words to add to MurmurWall
       led_matrices - A dictionary of all the LED matrices in MurmurWall
       emptying - a boolean describing if the system is emptying itself 

    """        
    led_strand.clear_state()

    packets_to_remove = []

    num_of_packets_to_append = update_packets(packets, packets_to_remove,
                                              led_strand, led_matrices)

    led_strand.update_hardware()        

    update_matrices(led_matrices)
    
    remove_packets(packets_to_remove, packets)

    if not emptying:
        add_new_packets(num_of_packets_to_append, packets, related_terms_queue)

# TODO: get rid of global variables, rethink DSs
def update_queue():
    """
    Gets latest words from the database, creates and returns a queue of
    words to be added to MurmurWall

    Returns:
        related_terms_queue - A queue of all the words to add to MurmurWall

    """
    related_terms_queue = Queue()
    trend_buckets = get_latest_data()
    related_terms_list = []
    for trend in trend_buckets:
        for related_term in trend_buckets[trend]["Top searches for"]:
            term = related_term.upper().encode('ascii', 'ignore')
            if term not in related_terms_list:
                related_terms_list.append(term)
    shuffle(related_terms_list)
    for i in range(0, len(related_terms_list)):
        related_terms_queue.put(related_terms_list[i])
    global updating
    updating = True
    print '\nRelated_Terms size = %i\n' % (related_terms_queue.qsize(),)
    return related_terms_queue

def restart_murmurwall(led_matrices, led_strand):
    """
    Restarts the MurmurWall system

    Args:
        led_matrices - A dictionary of all LED Matrices to shut off
        led_strand - the LED strand state to shut off
    """
    print '\nRestarting MurmurWall\n'    
    for led_matrix in led_matrices.values():
        led_matrix.shut_off()
    led_strand.shut_off()
    sleep(2)
    execv(sys.executable, [sys.executable] + sys.argv)

# TODO: can't always clean up?
def shutdown_murmurwall(led_matrices, led_strand):
    """
    Shutsdown the MurmurWall system

    Args:
        led_matrices - A dictionary of all LED Matrices to shut off
        led_strand - the LED strand state to shut off
    """
    for led_matrix in led_matrices.values():
        led_matrix.shut_off()
    led_strand.shut_off()
    sleep(2)
    sys.exit('\nShutting Down\n')

# TODO: Clean up
def main():
    """
    Initializes and begins the MurmurWall system

    Begins by getting the latest words to populate the system with, and subsequently
    creating packets to add into the system.

    Initializes all the ports, the LED Matrices and the LED Strand state.

    Runs main animation, begins emptying system ever RESTART_LENGTH seconds,
    restarts system when packets run out, adds a buzz word in every PRIORITY_LENGTH seconds,
    rests to maintain FRAMES_PER_SECOND.

    Raises:
        KeyboardInterrupt: detects when user manual exits system. Shutsdown the system
        SystemExit: detects when python shuts the program down. Shuts down the system
        IOError: an error in the serial communication. Restarts the system.

    """
    related_terms_queue = update_queue()
    packets = []
    add_new_packets(NUM_PACKETS, packets, related_terms_queue)
    led_port, matrix_port_1, matrix_port_2, matrix_port_3, matrix_port_4, matrix_port_5, matrix_port_6 = get_ports()
    led_matrices = {MATRIX_POSITIONS[0]: 
                    LedMatrix(matrix_port_1, MATRIX_POSITIONS[0], MATRIX_POSITIONS[1]),
                    MATRIX_POSITIONS[1]: 
                    LedMatrix(matrix_port_2, MATRIX_POSITIONS[1], MATRIX_POSITIONS[2]),
                    MATRIX_POSITIONS[2]: 
                    LedMatrix(matrix_port_3, MATRIX_POSITIONS[2], MATRIX_POSITIONS[3]),
                    MATRIX_POSITIONS[3]: 
                    LedMatrix(matrix_port_4, MATRIX_POSITIONS[3], MATRIX_POSITIONS[4]),
                    MATRIX_POSITIONS[4]: 
                    LedMatrix(matrix_port_5, MATRIX_POSITIONS[4], MATRIX_POSITIONS[5]),
                    MATRIX_POSITIONS[5]: 
                    LedMatrix(matrix_port_6, MATRIX_POSITIONS[5], END_PIX)}
                    
    led_strand = LedStrand(led_port, TOTAL_PIXELS)
    sleep_time = 0
    updating = False
    emptying = False
    last_time = time()
    priority_time = time()
    buzz_pos = 0
    restart_time = time()

    while True:
        try:
            if len(packets) == 0:
                restart_murmurwall(led_matrices, led_strand)
            if related_terms_queue.qsize() <= 300 and not updating:
                print '\nUpdating Words\n'
                updating = True
                thread = Thread(target=update_queue)
                thread.start()
            if time() - priority_time >= PRIORITY_LENGTH and not emptying:
                print '\nAdding Buzz Word\n'
                priority_time = time()
                color = (chr(255), chr(255), chr(255))
                buzz_packet = Packet(0.5, color, BUZZ_WORDS[buzz_pos],
                                     START_PIX, MATRIX_POSITIONS[0],
                                     START_PIX, False, True)
                packets.append(buzz_packet)
                buzz_pos += 1
                buzz_pos %= len(BUZZ_WORDS)

            if time() -  restart_time >= RESTART_LENGTH:
                emptying = True

            animate_mumurwall(packets, led_strand, related_terms_queue,
                              led_matrices, emptying)

            current_time = time()
            sleep_time = 1./FRAMES_PER_SECOND - (current_time - last_time)
            last_time = current_time
            if sleep_time >= 0:
                sleep(sleep_time)

        except (KeyboardInterrupt, SystemExit):
            shutdown_murmurwall(led_matrices, led_strand)
        except IOError:
            print '\nIOError, Restarting MurmurWall\n'
            sleep(30)
            restart_murmurwall(led_matrices, led_strand)

if __name__ == "__main__":
    print '\nStarting MurmurWall\n'
    main()