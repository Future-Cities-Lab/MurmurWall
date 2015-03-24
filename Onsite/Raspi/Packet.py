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

class Packet(object):
    """
    A class used to represent a packet used in MurmurWall 
    
    Attributes:
        length - number of LEDs this packet will cover
        speed - number of LEDs this packet will move each turn
        color - RGB tuple representing the color of this packet
        brightness - brightness of the center pixel of this packet
        current_position - current LED the middle pixel is at in the strand
        target_position - which LED the packet is heading towards
        text_being_displayed - a state representing if this packet is being
                               shown on an LED screen
    """
    def __init__(self, speed, color, text,
                 current_position, target_position,
                 prev_target_position, text_being_displayed, is_special=False):
        """
        Inits a Packet instance.
        """
        self.length = len(text)
        self.speed = speed
        self.red, self.green, self.blue = color
        self.text = text
        self.current_position = current_position
        self.prev_target_position = prev_target_position
        self.target_position = target_position
        self.text_being_displayed = text_being_displayed
        self.pod_speed = 0.017
        self.is_special = is_special

    def update_postion_strand(self):
        """
        Updates this packets current position based on its regular velocity
        """
        self.current_position += self.speed

    def update_postion_pod(self):
        """
        Updates this packet's current position based on its pod velocity
        """
        self.current_position += self.pod_speed

    def is_out_of_bounds(self, out_of_bounds):
        """

        Args:
            An integer representing when the pixel has gone out of bounds

        Return:
            A boolean representing if this packet is out of bounds
        """
        return self.current_position > out_of_bounds

    def has_reached_target(self):
        """
        Return:
            A boolean representing if this packet has reached its current target
        """
        return self.current_position >= self.target_position

    def target_is_end(self, end):
        """
        Args:
            An integer representing the final pixel in the LED strand

        Return:
            A boolean representing if this packet's target is the end
            of the LED strand
        """
        return self.target_position == end
