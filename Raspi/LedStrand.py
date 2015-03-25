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

# TODO: Make this a singleton

import serial
from platform import system
from time import sleep

class LedStrand(object):
    """
    A class representing the LED strand used in the MurmurWall System
    
    Attributes:
        color_state - state representing the next color state to send to the LED hardware
        port_number - the port number the LED hardware communicates over
    """
    def __init__(self, port_address, num_pixels):
        """
        Inits and instance of LedStrand with a port address, color state and number of pixels

        Args:

            num_pixels - An integer representing how many pixels are in the LED strand
            port_address - A Serial object used for communication
        """
        self.num_pixels = num_pixels
        self.color_state = [chr(0)] * (3*self.num_pixels)
        self.port_address = port_address

    def update_hardware(self):
        """
        Updates the LED hardware with the next color state

        Sends a '*' message to the hardware indicating it needs to revive
        the new color state.

        Subsequently, writes the color state as a byte array to the hardware
        """
        self.port_address.write('*')
        if system() == "Darwin":
            self.port_address.write(self.color_state)
        else:
            self.port_address.write(str(bytearray(self.color_state)))

    def clear_state(self):
        """
        Resets the LED state to black
        """
        self.color_state = [chr(0)] * 3*self.num_pixels

    def shut_off(self):
        """
        Sends a '%' to the LED hardware, telling it to wipe out its current data
        Subsequently, closes the port connection.

        """
        self.port_address.write('%')
        sleep(1)
        self.port_address.close()
