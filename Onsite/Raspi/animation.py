import time
import math
import pprint

from random import randrange, choice, randint

from Packet import Packet
from LedMatrix import LedMatrix
from LedStrand import LedStrand

from helper_functions import map_values, get_ports, lerp
from data_manager import get_latest_words

FADE_COLOR = 0.0

NUM_PIXELS = 360
TOTAL_PIXELS = NUM_PIXELS

START_PIX = 0
END_PIX = 299 

MATRIX_POS = 149

MAX_SPEED = 2.0
MIN_SPEED = 1.0

MAX_SPEED_LED = 40
MIN_SPEED_LED = 50

NUM_PACKETS = 3

WAIT_TIME = 0.076

POD_AMT = 0.4

def get_new_packet(word_list, speed):
    """
    Creates a new data packet to be used in MurmurWall
    """
    red = chr(randrange(0, 255))
    green = chr(0)
    blue = chr(255)
    bright = 255
    text = choice(word_list).upper().encode('ascii', 'ignore') + '\n'
    length = len(text)
    if length % 2 == 0:
        length += 1
    cur_pos = START_PIX
    tar_pos = MATRIX_POS
    prev_tar_pos = START_PIX
    displaying = False
    is_passsing = False
    passing_pos = 0
    return Packet(length, speed, red, green, blue, bright, text, cur_pos, tar_pos, prev_tar_pos, displaying, 0.0, is_passsing, passing_pos)

def get_next_available_matrix(led_matrices):
    """
    Returns the next available matrix in MurmurWall
    """
    # if led_matrices[MATRIX_POS].is_showing_packet:
    #     return END_PIX
    # else:
    return END_PIX


def test_leds(led_strand):
    """
    Input: LED Strand to test
    Runs: Sends a single data ant through system. 
    """
    for i in range(0, TOTAL_PIXELS):
        led_strand.clear_state()
        led_strand.color_state[3*i] = chr(255)
        led_strand.update_hardware()
        time.sleep(WAIT_TIME)

def color_pod(led_strand, packet):
    for i in range(0, 5):
        for j in range(0, 12):
            pos = 300 + (i*12) + j
            amt = map_values(math.sin(packet.theta), -1, 1, 0, POD_AMT)
            led_strand.color_state[3*pos] = chr(int(lerp(float(ord(packet.red)), FADE_COLOR, POD_AMT-amt)))
            led_strand.color_state[3*pos + 1] = chr(int(lerp(float(ord(packet.green)), FADE_COLOR, POD_AMT-amt)))
            led_strand.color_state[3*pos + 2] = chr(int(lerp(float(ord(packet.blue)), FADE_COLOR, POD_AMT-amt)))
    packet.theta += 0.2

def send_packet_to_end(packet):
    packet.prev_target_position = MATRIX_POS
    packet.target_position = END_PIX
    packet.current_position = MATRIX_POS + 1

def color_strand_for_packet(led_strand, packet):
    strands = packet.length/2
    led_strand.color_state[3*packet.current_position] = packet.red
    led_strand.color_state[3*packet.current_position + 1] = packet.green
    led_strand.color_state[3*packet.current_position + 2] = packet.blue

    # for i in range(1, strands):
    #     if packet.current_position - i > packet.prev_target_position:
    #         led_strand.color_state[3 * (packet.current_position - i)] = chr(int(lerp(float(ord(packet.red)), FADE_COLOR, 1.0-float(i)/float(strands))))
    #         led_strand.color_state[3 * (packet.current_position - i) + 1] = chr(int(lerp(float(ord(packet.green)), FADE_COLOR, 1.0-float(i)/float(strands))))
    #         led_strand.color_state[3 * (packet.current_position - i) + 2] = chr(int(lerp(float(ord(packet.blue)), FADE_COLOR, 1.0-float(i)/float(strands))))

    #     if packet.current_position + i < packet.target_position:
    #         led_strand.color_state[3 * (packet.current_position + i)] = chr(int(lerp(float(ord(packet.red)), FADE_COLOR, 1.0-float(i)/float(strands))))
    #         led_strand.color_state[3 * (packet.current_position + i) + 1] = chr(int(lerp(float(ord(packet.green)), FADE_COLOR, 1.0-float(i)/float(strands))))
    #         led_strand.color_state[3 * (packet.current_position + i) + 2] = chr(int(lerp(float(ord(packet.blue)), FADE_COLOR, 1.0-float(i)/float(strands))))    

def update_matrix(led_matrices, led_matrix):
    led_matrix.is_showing_packet = False
    led_matrix.packet.text_being_displayed = False
    led_matrix.packet.current_position = led_matrix.position + 1
    led_matrix.packet.prev_target_position = MATRIX_POS 
    led_matrix.packet.target_position = get_next_available_matrix(led_matrices) 
    led_matrix.packet = None

def send_ant_to_matrix(packet, led_matrices):
    packet.text_being_displayed = True
    packet.current_position = led_matrices[packet.target_position].position
    led_matrices[packet.target_position].is_showing_packet = True
    led_matrices[packet.target_position].packet = packet
    text_speed = int(map_values(float(packet.speed), MAX_SPEED, MIN_SPEED, MIN_SPEED_LED, MAX_SPEED_LED))
    led_matrices[packet.target_position].update_hardware(packet.red, packet.green, packet.blue, text_speed)

def packet_passing(packet, led_strand):
    for i in range(0, 5):
        pos = 300 + (i*12) + packet.passing_pos
        led_strand.color_state[3*pos] = packet.red
        led_strand.color_state[3*pos + 1] = packet.green
        led_strand.color_state[3*pos + 2] = packet.blue
    packet.passing_pos += 1

def animate(packets, led_strand, word_list, led_matrices):
    """
    The animation begins by drawing the previous state, and then updating.
    i.e, it draws each atom at the position determined by the previous iteration
    and then procedes to determine its next position
    """
    while True:
        to_remove = []
        to_append = 0
        led_strand.clear_state()
        for packet in packets:  

            print "Packet red = " + str(ord(packet.red))
            print "Packet green = " + str(ord(packet.green))
            print "Packet blue = " + str(ord(packet.blue))
            print ""

            if not packet.text_being_displayed and not packet.is_passsing:
                color_strand_for_packet(led_strand, packet)
                packet.current_position += packet.speed
                if packet.current_position >= packet.target_position:
                    if packet.target_position == END_PIX:
                        to_remove.append(packet)
                        to_append += 1
                    elif not led_matrices[packet.target_position].is_showing_packet:
                        send_ant_to_matrix(packet, led_matrices)
                    else:
                        packet.is_passsing = True
            elif packet.is_passsing:
                if packet.passing_pos == 12:
                    packet.is_passsing = False
                    packet.passing_pos = 0
                    send_packet_to_end(packet)
                else:
                    packet_passing(packet, led_strand)
            else:
                color_pod(led_strand, packet)

        led_strand.update_hardware()        
        
        for led_matrix in led_matrices.values():
            if led_matrix.is_showing_packet and led_matrix.is_finished():
                update_matrix(led_matrices, led_matrix)
        
        for packet in to_remove:
            packets.remove(packet)

        for i in range(0, to_append):
            packets.append(get_new_packet(word_list, randint(int(MIN_SPEED), int(MAX_SPEED))))

        time.sleep(WAIT_TIME)

def main():
    """
    main thread for MurmurWall
    """
    word_list = get_latest_words()

    packets = []
    for i in range(1, NUM_PACKETS+1):
        packets.append(get_new_packet(word_list, i))

    led_port, matrix_port = get_ports()

    led_matrices = {MATRIX_POS: LedMatrix(False, matrix_port, None, MATRIX_POS)}

    led_strand = LedStrand(led_port, TOTAL_PIXELS)

    animate(packets, led_strand, word_list, led_matrices)

    #test_leds(led_strand)

if __name__ == "__main__":
    print 'running main animation...'
    main()
