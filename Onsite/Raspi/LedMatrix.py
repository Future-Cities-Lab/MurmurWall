import serial
import platform
import time
import itertools

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
        for _ in itertools.repeat(None, 141 - len(packet.text)):
            to_send.append('\n')
        self.port_address.write('*')
        if platform.system() == "Darwin":
            self.port_address.write(to_send)
        else:
            self.port_address.write(str(bytearray(to_send)))

    def check_status(self):
        """
        Returns if hardware has finished displaying its current text
        """
        if self.port_address.inWaiting() > 0:
            print 'Got something, reading more'
            first_byte = self.port_address.read(1)
            print 'Time to get it all'
            if first_byte == '*':
                print 'Got it all'
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
        print 'sending'
        self.port_address.write('&')
        time.sleep(1)
        self.port_address.close()
