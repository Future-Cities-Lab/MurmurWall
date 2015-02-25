import serial
import platform

class LedMatrix(object):
    """
    A class designed to create instances representing a single LED Matrix in the MurmurWall System
    Variables:
        is_showing_packet - state representing if the LEDMatrix is currently displaying a packet
        port_number - the port number this LEDMatrix is communicating from
        packet - the packet this LEDMatrix is current displaying
        position - the LED of the strand that is the center of this matrix
    """
    def __init__(self, is_showing_packet, port_address, packet, position):
        self.is_showing_packet = is_showing_packet
        self.port_address = port_address
        self.packet = packet
        self.position = position

    def update_hardware(self, red, green, blue, text_speed):
        """
        Updates the Matrix with the new word to display
        """
        if platform.system() == "Darwin":
            print 'Sending : ' + self.packet.text
            self.port_address.write(red)
            self.port_address.write(green)
            self.port_address.write(blue)
            self.port_address.write(chr(text_speed))
            self.port_address.write(self.packet.text)
        else:
            self.port_address.write(str(bytearray(red)))
            self.port_address.write(str(bytearray(green)))
            self.port_address.write(str(bytearray(blue)))  
            self.port_address.write(str(bytearray(text_speed)))                        
            self.port_address.write(str(bytearray(self.packet.text)))

    def is_finished(self):
        """
        Returns if hardware has finished displaying its current text
        """
        out = ''
        while self.port_address.inWaiting() > 0:
            out += self.port_address.read(1) 
        return out == 'Done'
