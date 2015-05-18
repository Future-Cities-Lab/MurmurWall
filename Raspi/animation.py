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

'''

LEDs always slightly lit ~10%? Maybe a color like cyan?
      
    In LedConstructor - set background color.

# of Ants (maximum and minimum)

Buzz words/ Curated Words

Lighten the color of the text on screen to increase legibility

Smooth Ant movement

Fix color issue of Buzz ant

Pod LED behavior while displaying text (fill up then dissipate)

Limit amount of text sent to a pod at once

Secondary Fail safe that reboots Pi if process isn't running

Ant variable speed and Length

Disperse Ants to cover more of wall at one time

End behaviors pulsing or beacon that generates and absorbs ants lights fade up then release ant, lights fade out after ant reaches end

Trigger sensor that causes an ant to be released

Port system to Pi 2





'''

import sys
import RPi.GPIO as GPIO
from os import execv
from itertools import repeat
from threading import Thread, Timer
from Queue import Queue
from time import time, sleep
from random import uniform, shuffle, randint
import time as date
import subprocess

from Packet import Packet
from LedMatrix import LedMatrix
from LedStrand import LedStrand

from port_manager import get_ports
from data_manager import get_latest_data, get_buzz_word, get_currated_words

from color_functions import map_values, color_strand_for_packet
from color_functions import color_pod_for_packet

# How often to restart MurmurWall (seconds)
RESTART_LENGTH = 3600

# How often to add in a priority word (seconds)
PRIORITY_LENGTH = 200

# How many frames/second will MurmurWall run at
FRAMES_PER_SECOND = 30.0
SKIP_TICKS = 1000.0 / FRAMES_PER_SECOND

# How many pixels are in MurmurWall
NUM_PIXELS_LEFT = 2933
NUM_PIXELS_RIGHT = 776

TOTAL_PIXELS = NUM_PIXELS_LEFT + NUM_PIXELS_RIGHT

# L
START_PIX = 0

END_PIX = TOTAL_PIXELS - 1
OUT_OF_BOUNDS = END_PIX + 500


# Where the LED matrices are located on the pixel strip
# First LED entering pod....
MATRIX_POSITIONS = [912, 1157, 1373, 1644, 1853, 2092]

# Maximum speed packets will run on the LED strand
MAX_SPEED = 4.0
MIN_SPEED = 1.0

# Maximum speed packets will move on the LED matrices
MAX_SPEED_LED = 40
MIN_SPEED_LED = 50

# Maximum number of packets in MurmurWall
NUM_PACKETS = 12

BACKGROUND_R = chr(0)
BACKGROUND_G = chr(25)
BACKGROUND_B = chr(25)

RELAY_PIN_1 = 18
RELAY_PIN_2 = 23
RELAY_PIN_3 = 24
RELAY_PIN_4 = 25

def test_leds(led_strand_left, led_strand_right, current_pos):
    """
    Runs a single color through the entire LED strand to test the system

    Args: 
        led_strand = List: LED strand state to run the color through

    """
    led_strand_left.clear_state()
    #led_strand_right.clear_state()
    
    for pos in MATRIX_POSITIONS:
        led_strand_left.color_state[3*pos] = chr(255)
        
    led_strand_left.color_state[3*1853] = chr(255)


    '''
    if current_pos >= NUM_PIXELS_LEFT:
        new_current = current_pos-NUM_PIXELS_LEFT
        for i in range(new_current-15, new_current+16):
            if i >= 0 and i < NUM_PIXELS_RIGHT:
                print "writing to right at pos %i" % (i,)
                led_strand_right.color_state[3*i] = chr(255)
    else:
        for i in range(current_pos-15, current_pos+16):
            if i >= 0 and i < NUM_PIXELS_LEFT:
                print "writing to left at pos %i" % (i,)
                led_strand_left.color_state[3*i] = chr(255)
    '''

    led_strand_left.update_hardware()
    #led_strand_right.update_hardware()

def test_leds_right(led_strand_right, current_pos):
    """
    Runs a single color through the entire LED strand to test the system

    Args: 
        led_strand = List: LED strand state to run the color through

    """
    led_strand_right.clear_state()

    print "Data ant at pos %i" % (current_pos,)

    for i in range(current_pos-15, current_pos+16):
        if i >= 0 and i < NUM_PIXELS_LEFT:
            print i
            led_strand_right.color_state[3*i] = chr(255)

    #led_strand_right.color_state[3*current_pos] = chr(255)


    current_pos += 1
    current_pos %= NUM_PIXELS_RIGHT

    led_strand_right.update_hardware()

def send_packet_to_matrix(packet, led_matrix):
    """
    Sends the packet to an LED matrix to be displayed

    Args:
        packet - Packet: packet to send to the matrix
        led_matrix - LedMatrix: the matrix to send this packet to

    """
    packet.text_being_displayed = True
    packet.current_position = packet.target_position
    '''
    text_speed = int(map_values(packet.speed, MAX_SPEED,
                                MIN_SPEED, MIN_SPEED_LED, MAX_SPEED_LED))
    '''
    text_speed = 40
    color = (packet.red, packet.green, packet.blue)
    led_matrix.update_hardware(color, text_speed, packet)

def remove_packets(packets_to_remove, packets):
    """
    Removes all marked packets from MurmurWall

    Args:
        packets_to_remove - List: all packets to remove
        packets - List: all packets in MurmurWall
    """
    for packet in packets_to_remove:
        packets.remove(packet)  

def add_new_packets(num_of_packets_to_append, packets, related_terms_queue):
    """
    Adds a given number of new packets into MurmurWall

    Args:
        num_of_packets_to_append - Integer: how many new packets to add into MurmurWall
        packets - List: all active packets in the MurmurWall
        related_terms_queue - Queue: words to make packets from
    """
    for _ in repeat(None, num_of_packets_to_append):
        text = related_terms_queue.get()
        color = (chr(randint(0, 155)), chr(0), chr(255))
        new_packet = Packet(uniform(MIN_SPEED, MAX_SPEED), color, text,
                            START_PIX, MATRIX_POSITIONS[0],
                            START_PIX, False)
        packets.append(new_packet)

def update_matrices(led_matrices):
    """
    Checks each LED matrix in MurmurWall to see if they're finished
    displaying a packet. If so, puts the given packet backing into MurmurWall

    Args:
        led_matrices - Dictionary: all matrices in MurmurWall
    """
    for led_matrix in led_matrices.values():
        word = led_matrix.check_status()
        if word is not '' and 'messed up':
            print word
            for packet in led_matrix.packets:
                print "Packet text is : " + packet.text
                # TODO: Temp fix
                if packet.text.rstrip() == word.rstrip():
                    packet_to_update = packet
            led_matrix.packets.remove(packet_to_update)
            packet_to_update.text_being_displayed = False
            packet_to_update.current_position = led_matrix.position + 1.000002
            packet_to_update.prev_target_position = packet_to_update.target_position 
            packet_to_update.target_position = led_matrix.next_position 

def update_packets(packets, packets_to_remove, led_strand_left, led_strand_right, led_matrices):
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
        packets - List: all active packets in MurmurWall
        packets_to_remove - List: all packets marked for removal
        led_strand - LedStrand: the led strand
        led_matrices - Dictionary: all matrices in MurmurWall
    Returns:
        num_of_packets_to_append - Integer: the number of new packets to add into MurmurWall
    """
    num_of_packets_to_append = 0
    for packet in packets:
        if packet.is_out_of_bounds(OUT_OF_BOUNDS):
            packets_to_remove.append(packet)
            if not packet.is_special:
                num_of_packets_to_append += 1
        else:
            if not packet.text_being_displayed:
                print packet.current_position
                for i in range(int(packet.current_position)-2, int(packet.current_position)+3):
                    if i >= START_PIX and i <= END_PIX:
                        if i >= NUM_PIXELS_LEFT:
                            j = i - NUM_PIXELS_LEFT
                            led_strand_right.color_state[3*j] = packet.red
                            led_strand_right.color_state[(3*j) + 1] = packet.green
                            led_strand_right.color_state[(3*j) + 2] = packet.blue
                        else:
                            led_strand_left.color_state[3*i] = packet.red
                            led_strand_left.color_state[(3*i) + 1] = packet.green
                            led_strand_left.color_state[(3*i) + 2] = packet.blue   
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

def animate_mumurwall(packets, led_strand_left, led_strand_right, related_terms_queue, led_matrices, emptying):
    """
    Clears previous LED state, updates all packets, checks each LED matrix
    for a response, removes and adds new packets into the system.

    Args:
       packets - List: all active packets in MurmurWall
       led_strand - List: the current color state
       related_terms_queue - Queue: all words to add to MurmurWall
       led_matrices - Dictionary: all the LED matrices in MurmurWall
       emptying - Boolean: is the system is emptying itself?

    """
    led_strand_left.clear_state()
    led_strand_right.clear_state()

    packets_to_remove = []

    num_of_packets_to_append = update_packets(packets, packets_to_remove, led_strand_left, led_strand_right, led_matrices)
    led_strand_left.update_hardware()        
    led_strand_right.update_hardware()
    
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
        related_terms_queue - Queue: all the words to add to MurmurWall

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

def restart_murmurwall(led_matrices, led_strand_left, led_strand_right):
    """
    Restarts MurmurWall

    Args:
        led_matrices - Dictionary: all the LED matrices in MurmurWall
        led_strand - LedStrand: the led strand
    """
    print '\nRestarting MurmurWall\n'
    #t.cancel()
    sleep(2)
    GPIO.output(RELAY_PIN_1, GPIO.HIGH)
    GPIO.output(RELAY_PIN_2, GPIO.HIGH)
    GPIO.output(RELAY_PIN_3, GPIO.HIGH)
    GPIO.output(RELAY_PIN_4, GPIO.HIGH)
    sleep(10)
    subprocess.call("sudo reboot", shell=True)
    #execv(sys.executable, [sys.executable] + sys.argv)

# TODO: can't always clean up?
def shutdown_murmurwall(led_matrices, led_strand_left, led_strand_right):
    """
    Shutsdown MurmurWall 

    Args:
        led_matrices - Dictionary: all the LED matrices in MurmurWall
        led_strand - LedStrand: the led strand
    """
    #t.cancel()
    sleep(2)
    GPIO.output(RELAY_PIN_1, GPIO.HIGH)
    GPIO.output(RELAY_PIN_2, GPIO.HIGH)
    GPIO.output(RELAY_PIN_3, GPIO.HIGH)
    GPIO.output(RELAY_PIN_4, GPIO.HIGH)
    sleep(10)
    subprocess.call("sudo reboot", shell=True)
    #sys.exit('\nShutting Down\n')

def check_buzz(super_buzz_words):
    print 'Checking buzz'
    t = Timer(5.0, check_buzz, args=(super_buzz_words,))
    t.dameon = True
    t.start()
    buzz_word = get_buzz_word()
    if buzz_word is not 'fail':
        super_buzz_words.put(buzz_word)
    return t
    

# TODO: Clean up
def main():
    """
    Initializes and starts MurmurWall 

    Downloads the latest words to make Packets with, 

    Initializes all the ports, the LED Matrices and the LED Strand state.

    Runs main animation
    
    Empties MurmurWall every RESTART_LENGTH

    Restarts when packets run out

    Adds in a buzz word in every PRIORITY_LENGTH

    Rests to maintain FRAMES_PER_SECOND

    Raises:
        KeyboardInterrupt: detects when user manual exits system. Shutsdown the system
        SystemExit: detects when python shuts the program down. Shuts down the system
        IOError: an error in the serial communication. Restarts the system.

    """
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(RELAY_PIN_1, GPIO.OUT)
    GPIO.setup(RELAY_PIN_2, GPIO.OUT)
    GPIO.setup(RELAY_PIN_3, GPIO.OUT)
    GPIO.setup(RELAY_PIN_4, GPIO.OUT)
    
    GPIO.output(RELAY_PIN_1, GPIO.LOW)
    GPIO.output(RELAY_PIN_2, GPIO.LOW)
    GPIO.output(RELAY_PIN_3, GPIO.LOW)
    GPIO.output(RELAY_PIN_4, GPIO.LOW)
    sleep(2)
    try:

        sleep(2)
        print date.strftime("%d/%m/%Y")
        print date.strftime("%H:%M:%S")
    
        related_terms_queue = update_queue()
    
        packets = []
    
        add_new_packets(1, packets, related_terms_queue)

        led_port_1 = None
        led_port_2 = None
        matrix_port_1 = None
        matrix_port_2 = None
        matrix_port_3 = None
        matrix_port_4 = None
        matrix_port_5 = None
        matrix_port_6 = None
        led_matrices = None
        led_strand_left = None
        led_strand_right = None
        
        led_port_1, led_port_2, matrix_port_1, matrix_port_2, matrix_port_3, matrix_port_4, matrix_port_5, matrix_port_6 = get_ports()            
        
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

    
        led_strand_left = LedStrand(led_port_1, NUM_PIXELS_LEFT, (BACKGROUND_R, BACKGROUND_G, BACKGROUND_B))
        led_strand_right = LedStrand(led_port_2, NUM_PIXELS_RIGHT, (BACKGROUND_R, BACKGROUND_G, BACKGROUND_B))

        if led_port_1 is None or led_port_2 is None or matrix_port_1 is None or matrix_port_2 is None or matrix_port_3 is None or matrix_port_4 is None or matrix_port_5 is None or matrix_port_6 is None:
            restart_murmurwall(led_matrices, led_strand_left, led_strand_right)
            
        sleep_time = 0
        updating = False
        emptying = False
        starting = True
        last_time = time()
        priority_time = time()
        buzz_pos = 0
        restart_time = time()
        starting_time = time()
        buzz_time = time()

        while True:
            """
            if not super_buzz_word.empty():
                 color = (chr(255), chr(255), chr(255))
                 buzz_packet = Packet(0.5, color, super_buzz_word.get(),
                                     START_PIX, MATRIX_POSITIONS[0],
                                      START_PIX, False, True)
                 packets.append(buzz_packet)
            """
            if starting and time() - starting_time >= 5:
                starting_time = time()
                add_new_packets(1, packets, related_terms_queue)
                if len(packets) == NUM_PACKETS:
                    starting = False
            if len(packets) == 0:
                print "Done emptying, restarting"
                #shutdown_murmurwall(led_matrices, led_strand_left, led_strand_right)
                restart_murmurwall(led_matrices, led_strand_left, led_strand_right)
            """
            if related_terms_queue.qsize() <= 300 and not updating:
                 print '\nUpdating Words\n'
                 updating = True
                 thread = Thread(target=update_queue)
                 thread.start()
            """
            
            """
            if time() - priority_time >= PRIORITY_LENGTH and not emptying:
                 print '\nAdding Buzz Word\n'
                 priority_time = time()
                 color = (chr(255), chr(255), chr(255))
                 buzz_packet = Packet(0.5, color, buzz_words[buzz_pos],
                                     START_PIX, MATRIX_POSITIONS[0],
                                      START_PIX, False, True)
                 packets.append(buzz_packet)
                 buzz_pos += 1
                 buzz_pos %= len(buzz_words)
            """
            if time() -  restart_time >= RESTART_LENGTH:
                 emptying = True

            animate_mumurwall(packets, led_strand_left, led_strand_right, related_terms_queue, led_matrices, emptying)

            current_time = time()
            sleep_time = 1./FRAMES_PER_SECOND - (current_time - last_time)
            last_time = current_time
            if sleep_time >= 0:
                sleep(sleep_time)

    except (KeyboardInterrupt, SystemExit):
        shutdown_murmurwall(led_matrices, led_strand_left, led_strand_right)
    except IOError:
        print '\nIOError, Shutting down  MurmurWall\n'
        #shutdown_murmurwall(led_matrices, led_strand_left, led_strand_right)
        restart_murmurwall(led_matrices, led_strand_left, led_strand_right)
            
    
if __name__ == "__main__":
    print '\nStarting MurmurWall\n'
    main()
