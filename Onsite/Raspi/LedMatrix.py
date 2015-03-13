import serial
from platform import system
from itertools import repeat
from time import sleep

class LedMatrix(object):
    """
    A class designed to create instances representing a single LED Matrix in the MurmurWall System
    Variables:
        is_showing_packet - state representing if the LEDMatrix is currently displaying a packet
        port_number - the port number this LEDMatrix is communicating from
        packet - the packet this LEDMatrix is current displaying
        position - the LED of the strand that is the center of this matrix
    """
    def __init__(self, port_address, position):
        self.port_address = port_address
        self.position = position
        self.packets = []

    def update_hardware(self, color, text_speed, packet):
        """
        Updates the Matrix with the new word to display
        """
        print 'Sending : ' + packet.text
        red, green, blue = color
        to_send = [red, green, blue, chr(text_speed)]
        self.packets.append(packet)        
        for letter in packet.text:
            to_send.append(letter)
        for _ in repeat(None, 141 - len(packet.text)):
            to_send.append('\n')
        self.port_address.write('*')
        if system() == "Darwin":
            self.port_address.write(to_send)
        else:
            self.port_address.write(str(bytearray(to_send)))

    def check_status(self):
        """
        Returns if hardware has finished displaying its current text
        """
        if self.port_address.inWaiting() > 0:
            first_byte = self.port_address.read(1)
            if first_byte == '*':
                out = self.port_address.read(100)
                return out.replace('\n', '')
            else:
                return 'messed up'
        else:
            return ''

    def is_showing_packets(self):
        """
        returns if hardware is showing any text
        """
        return len(self.packets) > 0

    def shut_off(self):
        """
        returns if hardware is showing any text
        """
        self.port_address.write('&')
        sleep(1)
        self.port_address.close()
