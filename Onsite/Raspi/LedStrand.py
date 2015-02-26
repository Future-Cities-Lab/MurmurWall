# TODO: Make this a singleton

import serial
import platform
import pprint

class LedStrand(object):
    """
    A singleton class representing the LED strand used in the MurmurWall System
    Variables:
        color_state - state representing the next color state to send to the LED hardware
        port_number - the port number the LED hardware communicates over
    """
    def __init__(self, port_address, num_pixels):
        self.num_pixels = num_pixels
        self.color_state = [chr(0)] * (3*self.num_pixels)
        self.port_address = port_address

    def update_hardware(self):
        """
        Updates the LEDs with the next color state
        """

        pprint.PrettyPrinter(indent=4).pprint([ord(x) for x in self.color_state])
        if platform.system() == "Darwin":
            self.port_address.write(self.color_state)
        else:
            self.port_address.write(str(bytearray(self.color_state)))

    def check_response(self):
        """
        returns a response from the hardware 
        """
        out = ''
        while self.port_address.inWaiting() > 0:
            out += self.port_address.read(1)
        if out == '':
            return 'Nothing from the hardware'
        else:
            return "The hardware returned : " + out

    def clear_state(self):
        """
        clears the color state (sets all RGB values to black)
        """
        self.color_state = [chr(0)] * 3*self.num_pixels
