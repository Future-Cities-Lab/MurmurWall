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
from color_functions import lerp, map_values

class LedMatrix(object):
    """
    A class designed to create instances representing one LED matrix in the MurmurWall system
    
    Attributes:

        is_showing_packet - A Boolean representing if the LEDMatrix is currently displaying any packets
        port_number - A Serial object to communicate with the hardware throuh
        packets - A List of Packet objects this LEDMatrix is current displaying
        position - An Integer representing this LEDMatrix's position in MurmurWall
        next_position - An Integer representing a refrence to this Matrices neighbor
        
    """

    def __init__(self, port_address, position, next_position):
        """
        Inits an LedMatrix instance 

        Args (see Attributes for description):
            is_showing_packet - A Boolean representing if the LEDMatrix is currently displaying any packets
            port_number - A Serial object to communicate with the hardware throuh
            position - An Integer representing this LEDMatrix's position in MurmurWall
            next_position - An Integer representing a refrence to this Matrices neighbor
        """
        self.port_address = port_address
        self.position = position
        self.next_position = next_position
        self.packets = []

    def update_hardware(self, color, text_speed, packet):
        """
        Updates the Matrix with a new Packet to display

        Begins by writting a '*' to the hardware, readying it to recieve new data

        Packages the data as a byte array:
            '[red|green|blue|letter_1|....|letter_n|\n|....|\n]'

        Writes the byte array to the port

        Args:
            color - An (r,g,b) Tuple representing the color to display the packet with
            text_speed - An integer representing how fast to move the text
            packet - A Packet object to display in this matrix
        """
        print 'Sending : %s to : %i' % (packet.text, self.position,)
        red, green, blue = color
        amt = map_values(len(self.packets), 0, 8, 0.01, 1)
        amt = 1.0 - amt
        red = chr(int(lerp(ord(red), 0, amt)))
        green = chr(int(lerp(ord(green), 0, amt)))
        blue = chr(int(lerp(ord(blue), 0, amt)))

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
        Checks the status of matrix to see if it has finished displaying any Packets

        If a '*' has been recieved, then the hardware has finished with some Packet.

        Subsequently reads in the next 100 bytes to get text of the finished Packet.

        Returns:
            A String of the text of the finished Packet
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
        Checks to see if the matrix is showing any Packets

        Returns:
            A Boolean representing is the matrix is showing any Packets
        """
        return len(self.packets) > 0

    def shut_off(self):
        """
        Sends a '&'' to the hardware, telling it to empty all of its data
        Subsequently closes the port connection.
        """
        self.port_address.write('&')
        sleep(1)
        self.port_address.close()
