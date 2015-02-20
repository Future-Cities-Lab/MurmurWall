class Packet(object):
    """
    A class used to create instances representing one data packet used in the MurmurWall system
    Variables:
        length - Number of LEDs to cover
        speed - Number of LEDs to move each turn
        color - RGB tuple representing the color
        brightness - initial brightness of the center pixel
        current_position - current LED the middle pixel is at in the strand
        target_position - which LED the packet is heading towards
        text_being_displayed - a state representing if this packet is being shown on an LED screen
    """
    def __init__(self, length, speed, red, green, blue, brightness, text, current_position, target_position, text_being_displayed):
        self.length = length
        self.speed = speed
        self.red = red
        self.green = green
        self.blue = blue
        self.brightness = brightness
        self.text = text
        self.current_position = current_position
        self.target_position = target_position
        self.text_being_displayed = text_being_displayed
        