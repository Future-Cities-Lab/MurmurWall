import serial
import time
import platform

from random import randrange

from Packet import Packet
from LedMatrix import LedMatrix
from LedStrand import LedStrand

from helper_functions import get_available_ports, my_range

NUM_PIXELS = 57

BAUD_RATE = 115200
TIMEOUT = 1

# these should stay in this script
def get_new_packet():
    return Packet(5, 1, chr(randrange(0,255)), chr(randrange(0,255)), chr(randrange(0,255)), 255, 'TestTextTESTETS\n', 0, 28, False)

def get_next_available_matrix():
    return 56

def main():

    # Manager Variables
    packets = []
    packets.append(Packet(5, 1, chr(randrange(0,255)), chr(randrange(0,255)), chr(randrange(0,255)), 255, 'Suckers whut\n', 0, 28, False))

    print get_available_ports()
    led_port = ''
    matrix_port = ''
    if platform.system() == "Darwin":
        led_port = serial.Serial(get_available_ports()[2], BAUD_RATE, timeout=TIMEOUT)
        matrix_port = serial.Serial(get_available_ports()[3], BAUD_RATE, timeout=TIMEOUT)
    else:
        led_port = serial.Serial(get_available_ports()[0], BAUD_RATE, timeout=TIMEOUT)
    print led_port

    led_matrices = {28: LedMatrix(False, matrix_port, packets[0], 28)}

    led_strand = LedStrand(led_port)

    # Manager Algorithm-1

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
                        new_packet = get_new_packet()
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
