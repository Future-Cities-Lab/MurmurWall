class Packet(object):
    """
    A class used to create instances representing one data packet used in the MurmurWall system
    Variables:
        length - number of LEDs this packet will cover
        speed - number of LEDs this packet will move each turn
        color - RGB tuple representing the color of this packet
        brightness - brightness of the center pixel of this packet
        current_position - current LED the middle pixel is at in the strand
        target_position - which LED the packet is heading towards
        text_being_displayed - a state representing if this packet is being shown on an LED screen
    """
    def __init__(self, length, speed, color, text,
                 current_position, target_position,
                 prev_target_position, text_being_displayed, is_special=False):
        self.length = length
        self.speed = speed
        self.red, self.green, self.blue = color
        self.text = text
        self.current_position = current_position
        self.prev_target_position = prev_target_position
        self.target_position = target_position
        self.text_being_displayed = text_being_displayed
        self.pod_speed = 0.017
        self.is_special = is_special

    def update_postion(self):
        """
        updates current position based on velocity
        """
        self.current_position += self.speed

    def is_out_of_bounds(self, out_of_bounds):
        """
        returns if packet is out of bounds
        """
        return self.current_position > out_of_bounds

    def has_reached_target(self):
        """
        returns if packet has reached it's current target
        """
        return self.current_position >= self.target_position

    def target_is_end(self, end):
        """
        returns if packet's target is the end of the LED Strip
        """
        return self.target_position == end
