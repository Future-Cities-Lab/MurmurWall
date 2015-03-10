import time
import Queue
import threading
import itertools

from random import randrange, uniform, shuffle

from Packet import Packet
from LedMatrix import LedMatrix
from LedStrand import LedStrand

from helper_functions import get_ports
from data_manager import get_latest_buckets

from color_functions import map_values, color_strand_for_packet, color_pod_for_packet

FRAMES_PER_SECOND = 30.0
SKIP_TICKS = 1000.0 / FRAMES_PER_SECOND

NUM_PIXELS = 360
TOTAL_PIXELS = NUM_PIXELS

START_PIX = 0
END_PIX = 299 

MATRIX_POS = 149

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
    tar_pos = MATRIX_POS
    prev_tar_pos = START_PIX
    displaying = False
    return Packet(length, speed, color, 
                  text, cur_pos, tar_pos, prev_tar_pos,
                  displaying, is_special)

def get_next_available_matrix():
    """
    Returns the next available matrix in MurmurWall
    """
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

def send_packet_to_matrix(packet, led_matrices):
    """
    Send packet to matrix to be displayed
    """
    packet.text_being_displayed = True
    packet.current_position = 300
    led_matrices[packet.target_position].packets.append(packet)
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
    for _ in itertools.repeat(None, num_of_packets_to_append):
        text = related_terms_queue.get()
        packets.append(get_new_packet(text, uniform(MIN_SPEED, MAX_SPEED), None))

def update_matrices(led_matrices):
    """
    checks if matrices are finished displaying a word
    if so, they send the packet along
    """
    for led_matrix in led_matrices.values():
        word = led_matrix.check_status()
        if word is not '' and 'messed up':
            for packet in led_matrix.packets:
                if packet.text == word:
                    packet_to_update = packet
            led_matrix.packets.remove(packet_to_update)
            packet_to_update.text_being_displayed = False
            packet_to_update.current_position = 150 + 0.000002
            packet_to_update.prev_target_position = MATRIX_POS 
            packet_to_update.target_position = get_next_available_matrix()  

def update_packets(packets, packets_to_remove, led_strand, led_matrices):
    """
    does a bunch of complicated shit to update the packets
    """
    num_of_packets_to_append = 0
    for packet in packets:
        if packet.is_out_of_bounds(400):
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
                    if packet.target_is_end(300):
                        packets_to_remove.append(packet)
                        if not packet.is_special:
                            num_of_packets_to_append += 1
                    else:
                        send_packet_to_matrix(packet, led_matrices)
            else:
                color_pod_for_packet(led_strand.color_state, packet.current_position,
                                     packet.red, packet.green, packet.blue)
                packet.update_postion_pod()
    return num_of_packets_to_append

def animate(packets, led_strand, related_terms_queue, led_matrices):
    """
    The animation begins by drawing the previous state, and then updating.
    i.e, it draws each packet at the position determined by the previous iteration
    and then procedes to determine its next position
    """        
    led_strand.clear_state()

    packets_to_remove = []

    num_of_packets_to_append = update_packets(packets, packets_to_remove, led_strand, led_matrices)

    led_strand.update_hardware()        
    
    update_matrices(led_matrices)
    
    remove_packets(packets_to_remove, packets)

    add_new_packets(num_of_packets_to_append, packets, related_terms_queue)

def update_queue(related_terms_pqueue):
    """
    updates the words being displayed in the queue
    """
    trend_buckets = get_latest_buckets()
    related_terms_list = []
    for trend in trend_buckets:
        for related_term in trend_buckets[trend]["Top searches for"]:
            term = related_term.upper().encode('ascii', 'ignore')
            if term not in related_terms_list:
                related_terms_list.append(term)
    shuffle(related_terms_list)
    for i in range(0, len(related_terms_list)):
        related_terms_pqueue.put(related_terms_list[i])
    global updating
    updating = True
    print related_terms_pqueue.qsize()


def main():
    """
    main thread for MurmurWall
    """
    related_terms_queue = Queue.Queue()
    update_queue(related_terms_queue)
    packets = []
    for _ in itertools.repeat(None, NUM_PACKETS):    
        text = related_terms_queue.get()
        packets.append(get_new_packet(text, uniform(MIN_SPEED, MAX_SPEED), None))
    led_port, matrix_port = get_ports()
    led_matrices = {MATRIX_POS: LedMatrix(matrix_port, MATRIX_POS)}
    led_strand = LedStrand(led_port, TOTAL_PIXELS)
    sleep_time = 0
    last_time = time.time()
    updating = False
    priority_time = time.time()
    buzz_pos = 0

    while True:
        try:
            if related_terms_queue.qsize() <= 300 and not updating:
                updating = True
                thread = threading.Thread(target=update_queue, args=(related_terms_queue,))
                thread.start()
            if time.time() - priority_time >= 50:
                priority_time = time.time()
                color = (chr(255), chr(255), chr(255))
                packets.append(get_new_packet(BUZZ_WORDS[buzz_pos], 0.5, color, True))
                buzz_pos += 1
                buzz_pos %= len(BUZZ_WORDS)
            animate(packets, led_strand, related_terms_queue, led_matrices)
            current_time = time.time()
            sleep_time = 1./FRAMES_PER_SECOND - (current_time - last_time)
            last_time = current_time
            if sleep_time >= 0:
                time.sleep(sleep_time)
        except (KeyboardInterrupt, SystemExit):
            print ''
            print 'Goodbye!'
            led_matrices[MATRIX_POS].shut_off()
            led_strand.shut_off()
            raise
        except IOError:
            print 'Shit Error Restarting'
            time.sleep(5)

            related_terms_queue = Queue.Queue()
            update_queue(related_terms_queue)
            packets = []
            for _ in itertools.repeat(None, NUM_PACKETS):     
                text = related_terms_queue.get()
                packets.append(get_new_packet(text, uniform(MIN_SPEED, MAX_SPEED), None))
            led_port, matrix_port = get_ports()
            led_matrices = {MATRIX_POS: LedMatrix(matrix_port, MATRIX_POS)}
            led_strand = LedStrand(led_port, TOTAL_PIXELS)
            sleep_time = 0
            last_time = time.time()
            updating = False
            priority_time = time.time()
            buzz_pos = 0

if __name__ == "__main__":
    print 'running main animation...'
    main()
