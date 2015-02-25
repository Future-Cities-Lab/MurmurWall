import time

from random import randrange, choice, randint

from Packet import Packet
from LedMatrix import LedMatrix
from LedStrand import LedStrand

from helper_functions import map_values, get_ports
from data_manager import get_latest_words

NUM_PIXELS = 360
TOTAL_PIXELS = NUM_PIXELS

START_PIX = 0
END_PIX = 299 

MATRIX_POS = 149

MAX_SPEED = 4.0
MIN_SPEED = 1.0

MAX_SPEED_LED = 40
MIN_SPEED_LED = 50

NUM_PACKETS = 4

WAIT_TIME = 0.216

def get_new_packet(word_list, speed):
    """
    Creates a new data packet to be used in MurmurWall
    """
    red = chr(randrange(0, 255))
    green = 0
    blue = 255
    bright = 255
    text = choice(word_list).upper().encode('ascii', 'ignore') + '\n'
    length = len(text)
    if length % 2 == 0:
        length += 1
    cur_pos = START_PIX
    tar_pos = MATRIX_POS
    prev_tar_pos = START_PIX
    displaying = False
    return Packet(length, speed, red, green, blue, bright, text, cur_pos, tar_pos, prev_tar_pos, displaying)

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

def lerp(c2, c1, amt):
    return round(c1 + (c2-c1)*amt)

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
            
            print "This packet is : " + str(packet.length)

            if not packet.text_being_displayed:
                print "Moving, at pixel : " + str(packet.current_position) + ' and heading to : ' + str(packet.target_position) + '\n'
                
                strands = packet.length/2
                
                for i in range(1, strands):
                    
                    if packet.current_position - i > packet.prev_target_position:
                        led_strand.color_state[3 * (packet.current_position - i)] = chr(int(lerp(float(ord(packet.red)), 0.0, 1.0-float(i)/float(strands))))
                        led_strand.color_state[3 * (packet.current_position - i) + 1] = chr(int(lerp(float(ord(packet.green)), 0.0, 1.0-float(i)/float(strands))))
                        led_strand.color_state[3 * (packet.current_position - i) + 2] = chr(int(lerp(float(ord(packet.blue)), 0.0, 1.0-float(i)/float(strands))))

                    if packet.current_position + i < packet.target_position:
                        led_strand.color_state[3 * (packet.current_position + i)] = chr(int(lerp(float(ord(packet.red)), 0.0, 1.0-float(i)/float(strands))))
                        led_strand.color_state[3 * (packet.current_position + i) + 1] = chr(int(lerp(float(ord(packet.green)), 0.0, 1.0-float(i)/float(strands))))
                        led_strand.color_state[3 * (packet.current_position + i) + 2] = chr(int(lerp(float(ord(packet.blue)), 0.0, 1.0-float(i)/float(strands))))    

                led_strand.color_state[3*packet.current_position] = packet.red
                led_strand.color_state[3*packet.current_position + 1] = packet.green
                led_strand.color_state[3*packet.current_position + 2] = packet.blue

                packet.current_position += packet.speed
                
                if packet.current_position >= packet.target_position:
                    
                    print 'Data ant reached matrix : ' + str(packet.target_position)

                    if packet.target_position == END_PIX:
                        print 'Data ant is to be removed'
                        to_remove.append(packet)
                        to_append += 1
                    else:
                        if not led_matrices[packet.target_position].is_showing_packet:
                            print 'Sending ant to matrix'
                            packet.text_being_displayed = True
                            packet.current_position = led_matrices[packet.target_position].position
                            led_matrices[packet.target_position].is_showing_packet = True
                            led_matrices[packet.target_position].packet = packet
                            text_speed = int(map_values(float(packet.speed), MAX_SPEED, MIN_SPEED, MIN_SPEED_LED, MAX_SPEED_LED))
                            led_matrices[packet.target_position].update_hardware(packet.red, packet.green, packet.blue, text_speed)
                        else:
                            packet.prev_target_position = MATRIX_POS
                            packet.target_position = END_PIX
                            packet.current_position = MATRIX_POS + 1
            else:
                print 'Inside matrix, at position : ' + str(packet.current_position)
                for i in range(0, 5):
                    pos = 300 + (i*12)
                    led_strand.color_state[3*pos] = packet.red
                    led_strand.color_state[3*pos + 1] = packet.green
                    led_strand.color_state[3*pos + 2] = packet.blue

        led_strand.update_hardware()        
        
        for led_matrix in led_matrices.values():
            if led_matrix.is_showing_packet and led_matrix.is_finished():
                print '\nsending data ant to next matrix'
                led_matrix.is_showing_packet = False
                led_matrix.packet.text_being_displayed = False
                print "Adjusting packet " + str(led_matrix.packet.length)
                led_matrix.packet.current_position = led_matrix.position + 1
                print 'getting next matrix\n'
                led_matrix.packet.prev_target_position = MATRIX_POS 
                led_matrix.packet.target_position = get_next_available_matrix(led_matrices) 
                led_matrix.packet = None
        
        for packet in to_remove:
            print 'Removing data ant'
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
