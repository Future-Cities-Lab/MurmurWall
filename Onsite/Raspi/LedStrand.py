# TODO: Make this a singleton

import serial

import platform

class LedStrand(object):
    """
    A singleton class representing the LED strand used in the MurmurWall System
    Variables:
        color_state - state representing the next color state to send to the LED hardware
        port_number - the port number the LED hardware communicates over
    """
    def __init__(self, port_address):
        self.color_state = [chr(x*0) for x in range(0, 3*56)]
        self.port_address = port_address

    def update_hardware(self):
        """
        Updates the LEDs with the next color state
        """
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
        # TODO: make this more clever
        self.color_state = [chr(x*0) for x in range(0, 3*56)]



