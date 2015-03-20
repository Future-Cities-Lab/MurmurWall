"""
Module for Running the MurmurWall
"""

from sys import executable, argv, exit
from os import execv
from itertools import repeat
from threading import Thread
from Queue import Queue
from time import time, sleep
from random import randrange, uniform, shuffle

from Packet import Packet
from LedMatrix import LedMatrix
from LedStrand import LedStrand

from helper_functions import get_ports
from data_manager import get_latest_data

from color_functions import map_values, color_strand_for_packet, color_pod_for_packet


RESTART_LENGTH = 1800

PRIORITY_LENGTH = 200

FRAMES_PER_SECOND = 30.0
SKIP_TICKS = 1000.0 / FRAMES_PER_SECOND

NUM_PIXELS = 360
TOTAL_PIXELS = NUM_PIXELS

START_PIX = 0
END_PIX = 299

OUT_OF_BOUNDS = 400 

MATRIX_POSITIONS = [29, 69, 109, 149, 189, 229]

MAX_SPEED = 0.3
MIN_SPEED = 0.05

MAX_SPEED_LED = 40
MIN_SPEED_LED = 50

NUM_PACKETS = 8

BUZZ_WORDS = ['YBCA', 'YERBA BUENA', 'SF MOMA', 
              'MARKET ST. PROTOTYPING FESTIVAL', 
              'MISSION ST.', 'MURMURWALL']

def get_new_packet(text, speed, color, is_special=False):
    """
    Creates a new data packet to be used in MurmurWall
    """
    if color is None:    
        red = chr(randrange(0, 255))
        green = chr(0)
        blue = chr(255)
        color = (red, green, blue)
    length = len(text)
    if length % 2 == 0:
        length += 1
    cur_pos = START_PIX
    tar_pos = MATRIX_POSITIONS[0]
    prev_tar_pos = START_PIX
    displaying = False
    return Packet(length, speed, color, 
                  text, cur_pos, tar_pos, prev_tar_pos,
                  displaying, is_special)

def test_leds(led_strand):
    """
    Input: LED Strand to test
    Runs: Sends a single data ant through system. 
    """
    for i in range(0, TOTAL_PIXELS):
        led_strand.clear_state()
        led_strand.color_state[3*i] = chr(255)
        led_strand.update_hardware()

def send_packet_to_matrix(packet, led_matrices):
    """
    Send packet to matrix to be displayed
    """
    packet.text_being_displayed = True
    packet.current_position = packet.target_position
    #led_matrices[packet.target_position].packets.append(packet)
    text_speed = int(map_values(packet.speed, MAX_SPEED, MIN_SPEED, MIN_SPEED_LED, MAX_SPEED_LED))
    color = (packet.red, packet.green, packet.blue)
    led_matrices[packet.target_position].update_hardware(color, text_speed, packet)

def remove_packets(packets_to_remove, packets):
    """
    removes all packets marked to removal
    """
    for packet in packets_to_remove:
        packets.remove(packet)  

def add_new_packets(num_of_packets_to_append, packets, related_terms_queue):
    """
    adds a number of new packets into system
    """
    for _ in repeat(None, num_of_packets_to_append):
        text = related_terms_queue.get()
        packets.append(get_new_packet(text, uniform(MIN_SPEED, MAX_SPEED), None))

def update_matrices(led_matrices):
    """
    checks if matrices are finished displaying a word
    if so, they send the packet along
    """
    #print "Matrices :"
    for led_matrix in led_matrices.values():
        #print led_matrix.position
        #print len(led_matrix.packets)
        #for packet in led_matrix.packets:
            #print packet.current_position
        #print ""
        word = led_matrix.check_status()
        if word is not '' and 'messed up':
            #print word
            for packet in led_matrix.packets:
                if packet.text == word:
                    packet_to_update = packet
            led_matrix.packets.remove(packet_to_update)
            packet_to_update.text_being_displayed = False
            packet_to_update.current_position = led_matrix.position + 1.000002
            packet_to_update.prev_target_position = packet_to_update.target_position 
            packet_to_update.target_position = led_matrix.next_position 

def update_packets(packets, packets_to_remove, led_strand, led_matrices):
    """
    does a bunch of complicated shit to update the packets
    """
    num_of_packets_to_append = 0
    for packet in packets:
        if packet.is_out_of_bounds(OUT_OF_BOUNDS):
            packets_to_remove.append(packet)
            if not packet.is_special:
                num_of_packets_to_append += 1
        else:
            if not packet.text_being_displayed:
                color_strand_for_packet(led_strand.color_state, packet.current_position,
                                        packet.red, packet.green, packet.blue, 
                                        packet.prev_target_position, packet.target_position)
                packet.update_postion_strand()
                if packet.has_reached_target():
                    if packet.target_is_end(END_PIX):
                        packets_to_remove.append(packet)
                        if not packet.is_special:
                            num_of_packets_to_append += 1
                    else:
                        send_packet_to_matrix(packet, led_matrices)
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
    The animation begins by drawing the previous state, and then updating.
    i.e, it draws each packet at the position determined by the previous iteration
    and then procedes to determine its next position
    """        
    led_strand.clear_state()

    packets_to_remove = []

    num_of_packets_to_append = update_packets(packets, packets_to_remove, led_strand, led_matrices)

    led_strand.update_hardware()        

    #print "Length of packets : %i" % (len(packets),)
    update_matrices(led_matrices)
    
    remove_packets(packets_to_remove, packets)

    if not emptying:
        add_new_packets(num_of_packets_to_append, packets, related_terms_queue)

def update_queue():
    """
    updates the words being displayed in the queue
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
    restarts the system
    """
    print '\nRestarting MurmurWall\n'    
    for led_matrix in led_matrices.values():
        led_matrix.shut_off()
    led_strand.shut_off()
    sleep(2)
    execv(executable, [executable] + argv)

def shutdown_murmurwall(led_matrices, led_strand):
    """
    shutsdown the system
    """
    for led_matrix in led_matrices.values():
        led_matrix.shut_off()
    led_strand.shut_off()
    sleep(2)
    exit('\nShutting Down\n')


def main():
    """
    main thread for MurmurWall
    """
    related_terms_queue = update_queue()
    packets = []
    for _ in repeat(None, NUM_PACKETS):    
        text = related_terms_queue.get()
        packets.append(get_new_packet(text, uniform(MIN_SPEED, MAX_SPEED), None))
    
    led_port, matrix_port_1, matrix_port_2, matrix_port_3, matrix_port_4, matrix_port_5, matrix_port_6 = get_ports()
    
    led_matrices = {MATRIX_POSITIONS[0]: LedMatrix(matrix_port_1, MATRIX_POSITIONS[0], MATRIX_POSITIONS[1]),
                    MATRIX_POSITIONS[1]: LedMatrix(matrix_port_2, MATRIX_POSITIONS[1], MATRIX_POSITIONS[2]),
                    MATRIX_POSITIONS[2]: LedMatrix(matrix_port_3, MATRIX_POSITIONS[2], MATRIX_POSITIONS[3]),
                    MATRIX_POSITIONS[3]: LedMatrix(matrix_port_4, MATRIX_POSITIONS[3], MATRIX_POSITIONS[4]),
                    MATRIX_POSITIONS[4]: LedMatrix(matrix_port_5, MATRIX_POSITIONS[4], MATRIX_POSITIONS[5]),
                    MATRIX_POSITIONS[5]: LedMatrix(matrix_port_6, MATRIX_POSITIONS[5], END_PIX)}
                    
    led_strand = LedStrand(led_port, TOTAL_PIXELS)
    sleep_time = 0
    updating = False
    emptying = False
    last_time = time()
    priority_time = time()
    buzz_pos = 0
    restart_time = time()

    print '\nStarting MurmurWall\n'
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
                print '\nAdding Priority Word\n'
                priority_time = time()
                color = (chr(255), chr(255), chr(255))
                packets.append(get_new_packet(BUZZ_WORDS[buzz_pos], 0.5, color, True))
                buzz_pos += 1
                buzz_pos %= len(BUZZ_WORDS)

            if time() -  restart_time >= RESTART_LENGTH:
                emptying = True

            animate_mumurwall(packets, led_strand, related_terms_queue, led_matrices, emptying)

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
            related_terms_queue = update_queue()
            packets = []
            for _ in repeat(None, NUM_PACKETS):     
                text = related_terms_queue.get()
                packets.append(get_new_packet(text, uniform(MIN_SPEED, MAX_SPEED), None))
            led_port, matrix_port_1, matrix_port_2, matrix_port_3, matrix_port_4, matrix_port_5, matrix_port_6 = get_ports()
    
            led_matrices = {MATRIX_POSITIONS[0]: LedMatrix(matrix_port_1, MATRIX_POSITIONS[0], MATRIX_POSITIONS[1]),
                            MATRIX_POSITIONS[1]: LedMatrix(matrix_port_2, MATRIX_POSITIONS[1], MATRIX_POSITIONS[2]),
                            MATRIX_POSITIONS[2]: LedMatrix(matrix_port_3, MATRIX_POSITIONS[2], MATRIX_POSITIONS[3]),
                            MATRIX_POSITIONS[3]: LedMatrix(matrix_port_4, MATRIX_POSITIONS[3], MATRIX_POSITIONS[4]),
                            MATRIX_POSITIONS[4]: LedMatrix(matrix_port_5, MATRIX_POSITIONS[4], MATRIX_POSITIONS[5]),
                            MATRIX_POSITIONS[5]: LedMatrix(matrix_port_6, MATRIX_POSITIONS[5], END_PIX)}

            led_strand = LedStrand(led_port, TOTAL_PIXELS)
            sleep_time = 0
            last_time = time()
            updating = False
            priority_time = time()
            buzz_pos = 0

if __name__ == "__main__":
    print '\nStarting Script\n'
    main()
