import serial
import platform

# THIS SHOULD BE A SINGLETON!
class LedStrand(object):
    """
    A singleton class representing the LED strand used in the MurmurWall System
    Variables:
        color_state - state representing the next color state to send to the LED hardware
        port_number - the port number the LED hardware communicates over
    """
    def __init__(self, port_address):
        self.color_state = [chr(x*0) for x in range(0, 3*57)]
        self.port_address = port_address

    def update_hardware(self):
        if platform.system() == "Darwin":
            self.port_address.write(self.color_state)
        else:
            self.port_address.write(str(bytearray(self.color_state)))

    def check_response(self):
        out = ''
        while self.port_address.inWaiting() > 0:
            out += self.port_address.read(1)
        return out

    def clear_state(self):
        self.color_state = [chr(x*0) for x in range(0, 3*57)]



