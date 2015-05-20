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
from time import sleep

class LedStrand(object):
    """
    A class representing an LED strand used in the MurmurWall System
    
    Attributes:
            color_state = an array of bytes (RGB) to send to the hardware
            num_pixels - An integer representing how many pixels are in the LED strand
            port_address - A Serial object used for communication
    """
    def __init__(self, port_address, num_pixels, background_color):
        """
        Inits and instance of LedStrand with a port address, color state and number of pixels

        Args (see Attributes for description):

            num_pixels - An integer representing how many pixels are in the LED strand
            port_address - A Serial object used for communication

        """
        self.num_pixels = num_pixels
        self.color_state = [chr(0)] * (3*self.num_pixels)
        self.background_r, self.background_g, self.background_b = background_color
        for i in range(0, self.num_pixels):
            self.color_state[3*i] = self.background_r
            self.color_state[(3*i)+1] =  self.background_g
            self.color_state[(3*i)+2] =  self.background_b
        self.port_address = port_address

    def update_hardware(self):
        """
        Updates the hardware with the current 'color_state'
        Sends an '*' to the hardware as part of a serial protocol
        """
        self.port_address.write('*')
        if system() == "Darwin":
            self.port_address.write(self.color_state)
        else:
            self.port_address.write(str(bytearray(self.color_state)))

    def clear_state(self):
        """
        Sets every pixel in 'color_state' to black
        """
        for i in range(0, self.num_pixels):
            self.color_state[3*i] =  self.background_r
            self.color_state[(3*i)+1] =  self.background_g
            self.color_state[(3*i)+2] =  self.background_b
            
    def shut_off(self):
        """
        Sends an '%' to the hardware, telling it to wipe out its current data
        Subsequently, closes the port connection.
        """
        self.port_address.write('%')
        sleep(1)
        self.port_address.close()
