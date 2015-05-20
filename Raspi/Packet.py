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
    A class designed to create instances representing one Packet in the MurmurWall system
    
    Attributes:
        length - Integer: the number of LEDs this packet will cover
        speed - Integer: how fast the text will move
        color - RGB tuple: color value of this packet
        text - String: the text that will be displayed on the screens
        current_position - Integer: the current pixel this Packet is at
        target_position - Integer: the next pixel this Packet is heading to
        text_being_displayed - Boolean: is this text being displayed right now?
        pod_speed  - Float: how fast this Packet moves in a pod
        is_special - Boolean: is this Packet is a 'buzz word'
    """
    def __init__(self, speed, color, text,
                 current_position, target_position,
                 prev_target_position, text_being_displayed,is_special=False):
        """
        Args (see Attributes for description):
            speed 
            color
            text
            current_position 
            target_position
            text_being_displayed
            is_special

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
        Updates this packet's 'current_position' from its 'speed'
        """
        self.current_position += self.speed

    def update_postion_pod(self):
        """
        Updates this packet's 'current_position' from its 'pod_speed'
        """
        self.current_position += self.pod_speed

    def is_out_of_bounds(self, out_of_bounds):
        """

        Args:
            out_of_bounds - Integer: a pixel position outside MurmurWall

        Return:
            Boolean: is this packet out of bounds?
        """
        return self.current_position > out_of_bounds

    def has_reached_target(self):
        """
        Return:
            Boolean: has this packet reached its 'target_position'?
        """
        return self.current_position >= self.target_position

    def target_is_end(self, end):
        """
        Args:
            end - Integer: the final pixel in MurmurWall

        Return:
            Boolean: is this packet's 'target_position' at the end of MurmurWall?
        """
        return self.target_position == end
