import time
import math

from random import randrange, choice, uniform

from Packet import Packet
from LedMatrix import LedMatrix
from LedStrand import LedStrand

from helper_functions import map_values, get_ports, lerp
from data_manager import get_latest_words

FRAMES_PER_SECOND = 30.0
SKIP_TICKS = 1000.0 / FRAMES_PER_SECOND

FADE_COLOR = 0.0

NUM_PIXELS = 360
TOTAL_PIXELS = NUM_PIXELS

START_PIX = 0
END_PIX = 299 

MATRIX_POS = 149

MAX_SPEED = 0.3
MIN_SPEED = 0.05

MAX_SPEED_LED = 40
MIN_SPEED_LED = 50

NUM_PACKETS = 4

WAIT_TIME = 0.0276

POD_AMT = 0.4

ORIG = [100.0, 25.0, 10.0, 0.0001]
DIFF = [75.0, 15.0, 5.0, 2.0]

def get_new_packet(word_list, speed):
    """
    Creates a new data packet to be used in MurmurWall
    """
    red = chr(randrange(0, 255))
    green = chr(0)
    blue = chr(255)
    bright = 255
    text = choice(word_list).upper().encode('ascii', 'ignore')
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

def color_pod(led_strand, packet, led_matrices):
    middle_pos = int(math.floor(led_matrices[MATRIX_POS].text_pos + 0.00001))
    currnt_count = led_matrices[MATRIX_POS].text_pos - middle_pos
    for i in range(0, 5):
        pos = 0
        if i % 2 == 0:
            pos = middle_pos + (i*12)
        else:
            by_pos = 300 + ((i+1)*12)
            pos = 2*(by_pos) - (middle_pos + ((i+1)*12) + 1)
        pos_n_two = ORIG[2] - (DIFF[2] * currnt_count)
        pos_n_one = ORIG[1] - (DIFF[1] * currnt_count)
        pos_middle = ORIG[0] - (DIFF[0] * currnt_count)
        pos_one = ORIG[1] + (DIFF[1] * currnt_count)
        pos_two = ORIG[2] + (DIFF[2] * currnt_count)
        pos_tree = ORIG[3] + (DIFF[3] * currnt_count)
        pos_list = [pos_n_two, pos_n_one, pos_middle, pos_one, pos_two, pos_tree]
        for j in range(-2, 4):
            if i % 2 == 0:
                if j > 0:
                    pixel_pos = pos + j + 2
                else:
                    pixel_pos = pos + j
                if pixel_pos >= 300 + (i*12) and pixel_pos <= 300 + (i*12) + 11:
                    alpha = map_values(pos_list[j+2], 0.0, 100.0, 0.0, 1.0)
                    float_red = float(ord(packet.red))
                    float_green = float(ord(packet.green))
                    float_blue = float(ord(packet.blue))
                    new_red = chr(int(lerp(float_red, FADE_COLOR, alpha)))
                    new_green = chr(int(lerp(float_green, FADE_COLOR, alpha)))
                    new_blue = chr(int(lerp(float_blue, FADE_COLOR, alpha)))
                    led_strand.color_state[3*pixel_pos] = new_red
                    led_strand.color_state[3*pixel_pos + 1] = new_green
                    led_strand.color_state[3*pixel_pos + 2] = new_blue
    led_matrices[MATRIX_POS].text_pos += led_matrices[MATRIX_POS].text_speed


def send_packet_to_end(packet):
    packet.prev_target_position = MATRIX_POS
    packet.target_position = END_PIX
    packet.current_position = MATRIX_POS + 1

def color_strand_for_packet(led_strand, packet):

    middle_pos = int(math.floor(packet.current_position + 0.00001))

    currnt_count = packet.current_position - middle_pos

    pos_n_two = ORIG[2] - (DIFF[2] * currnt_count)
    pos_n_one = ORIG[1] - (DIFF[1] * currnt_count)    
    pos_middle = ORIG[0] - (DIFF[0] * currnt_count)
    pos_one = ORIG[1] + (DIFF[1] * currnt_count)
    pos_two = ORIG[2] + (DIFF[2] * currnt_count)
    pos_tree = ORIG[3] + (DIFF[3] * currnt_count)

    pos_list = [pos_n_two, pos_n_one, pos_middle, pos_one, pos_two, pos_tree]

    for i in range(-2, 4):
        if i > 0:
            pixel_pos = middle_pos + i + 1
        else:
            pixel_pos = middle_pos + i
        if pixel_pos > packet.prev_target_position and pixel_pos < packet.target_position:
            alpha = map_values(pos_list[i+2], 0.0, 100.0, 0.0, 1.0)
            float_red = float(ord(packet.red))
            float_green = float(ord(packet.green))
            float_blue = float(ord(packet.blue))
            new_red = chr(int(lerp(float_red, FADE_COLOR, alpha)))
            new_green = chr(int(lerp(float_green, FADE_COLOR, alpha)))
            new_blue = chr(int(lerp(float_blue, FADE_COLOR, alpha)))
            led_strand.color_state[3*pixel_pos] = new_red
            led_strand.color_state[3*pixel_pos + 1] = new_green
            led_strand.color_state[3*pixel_pos + 2] = new_blue

    led_strand.color_state[3*(middle_pos+1)] = packet.red
    led_strand.color_state[3*(middle_pos+1) + 1] = packet.green
    led_strand.color_state[3*(middle_pos+1) + 2] = packet.blue

def update_matrix(led_matrices, led_matrix):
    led_matrix.is_showing_packet = False
    led_matrix.text_pos = 300.0
    led_matrix.text_speed = 0.0
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
    led_matrices[packet.target_position].text_speed = map_values(float(len(packet.text)), 0.0, 17.0, 0.015, 0.017)
    text_speed = int(map_values(packet.speed, MAX_SPEED, MIN_SPEED, MIN_SPEED_LED, MAX_SPEED_LED))
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
    to_remove = []
    to_append = 0
    led_strand.clear_state()
    for packet in packets:  
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
            color_pod(led_strand, packet, led_matrices)

    led_strand.update_hardware()        
    
    for led_matrix in led_matrices.values():
        if led_matrix.is_showing_packet and led_matrix.is_finished():
            update_matrix(led_matrices, led_matrix)
    
    for packet in to_remove:
        packets.remove(packet)

    for i in range(0, to_append):
        packets.append(get_new_packet(word_list, uniform(MIN_SPEED, MAX_SPEED)))

    #time.sleep(WAIT_TIME)

def main():
    """
    main thread for MurmurWall
    """
    word_list = get_latest_words()

    packets = []

    for i in range(1, NUM_PACKETS+1):
        packets.append(get_new_packet(word_list, uniform(MIN_SPEED, MAX_SPEED)))

    led_port, matrix_port = get_ports()

    led_matrices = {MATRIX_POS: LedMatrix(False, matrix_port, None, MATRIX_POS)}

    led_strand = LedStrand(led_port, TOTAL_PIXELS)
    
    sleep_time = 0

    last_time = time.time()

    while True:
        try:
            animate(packets, led_strand, word_list, led_matrices)
            current_time = time.time()
            sleep_time = 1./FRAMES_PER_SECOND - (current_time - last_time)
            last_time = current_time
            if sleep_time >= 0:
                time.sleep(sleep_time)
        except (KeyboardInterrupt, SystemExit):
            print ''
            print 'Goodbye!'
            led_strand.port_address.close()
            led_matrices[MATRIX_POS].port_address.close()
            raise

    #test_leds(led_strand)

if __name__ == "__main__":
    print 'running main animation...'
    main()
