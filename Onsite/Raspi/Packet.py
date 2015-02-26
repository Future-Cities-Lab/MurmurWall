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
    def __init__(self, length, speed, red,
                 green, blue, brightness, text,
                 current_position, target_position,
                 prev_target_position, text_being_displayed, theta,
                 is_passsing, passing_pos):
        self.length = length
        self.speed = speed
        self.red = red
        self.green = green
        self.blue = blue
        self.brightness = brightness
        self.text = text
        self.current_position = current_position
        self.prev_target_position = prev_target_position
        self.target_position = target_position
        self.text_being_displayed = text_being_displayed
        self.theta = theta
        self.is_passsing = is_passsing
        self.passing_pos = passing_pos
