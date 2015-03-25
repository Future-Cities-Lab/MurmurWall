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

import serial
from platform import system
from itertools import repeat
from time import sleep

class LedMatrix(object):
    """
    A class designed to represent a single LED matrix in the MurmurWall System
    
    Attributes:
        is_showing_packet - state representing if the LEDMatrix is currently displaying a packet
        port_number - the port number this LEDMatrix is communicating from
        packet - the packet this LEDMatrix is current displaying
        position - the LED of the strand that is the center of this matrix
    """

    def __init__(self, port_address, position, next_position):
        """
        Inits an LedMatrix instance with with a Serial, color state and number of pixels

        Args:

            position - An integer representing the pixel the matrix is located at
            next_position - An integer representing the next pixel postition to send each
                            packet to when finished displaying.
            port_address - A Serial object used for communication
        """
        self.port_address = port_address
        self.position = position
        self.next_position = next_position
        self.packets = []

    def update_hardware(self, color, text_speed, packet):
        """
        Updates the Matrix with the new word to display

        Begins by writting a '*' to the port to indicate to the hardware that it is going 
        to recieve new data

        Packages the data as a byte array:
            '[red|green|blue|letter_1|....|letter_n|\n|....|\n]'

        Writes the byte array to the port.

        Args:
            color - An (r,g,b) Tuple representing the color to display the packet with
            text_speed - An integer representing how fast to move the text
            packet - A Packet object to display in this matrix
        """
        print 'Sending : %s to : %i' % (packet.text, self.position,)
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
        Checks the status of matrix to see if it is finished displaying any text

        If we revive a '*', we are being told by the hardware it is finished with something.

        We subsequently read in the next 100 bytes to get the finished Packet.

        Returns:
            A string of the finished text
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
        Checks to see if the matrix is showing any text

        Returns:
            A boolean representing is the matrix is showing any text
        """
        return len(self.packets) > 0

    def shut_off(self):
        """
        Sends a signal to the matrix for it wipe out its current data
        Subsequently, closes the port connection.

        """
        self.port_address.write('&')
        sleep(1)
        self.port_address.close()
