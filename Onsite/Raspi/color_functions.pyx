from libc.math cimport round

ORIG = [100.0, 25.0, 10.0, 0.0001]
DIFF = [75.0, 15.0, 5.0, 2.0]

def map_values(double value, double i_start, double i_stop, double o_start, double o_stop): 
    return o_start + (o_stop - o_start) * ((value - i_start) / (i_stop - i_start))

def lerp(int channel_2, int channel_1, double amt):
    return round(channel_1 + (channel_2 - channel_1) * amt)

def color_strand_for_packet(led_strand, double current_position, char red, char green, char blue, int prev_target_position, int target_position):
    cdef int middle_pixel
    cdef double current_count
    
    middle_pixel = <int>(current_position + 0.00001)
    led_strand.color_state[3*(middle_pixel+1)] = red
    led_strand.color_state[3*(middle_pixel+1) + 1] = green
    led_strand.color_state[3*(middle_pixel+1) + 2] = blue

    current_count = current_position - middle_pixel
    curve = []
    for i in range(-2, 4):
        if i < 0:
            i = i * -1
        curve.append(ORIG[i] - (DIFF[i] * current_count))
    cdef int pixel_pos
    cdef double alpha
    for i in range(-2, 4):
        if i > 0:
            pixel_pos = middle_pixel + i + 1
        else:
            pixel_pos = middle_pixel + i
        if pixel_pos > prev_target_position and pixel_pos < target_position:
            alpha = map_values(curve[i+2], 0.0, 100.0, 0.0, 1.0)
            led_strand.color_state[3*pixel_pos] = <char>lerp(<int>red, 0.0, alpha)
            led_strand.color_state[3*pixel_pos + 1] = <char>lerp(<int>green, 0.0, alpha)
            led_strand.color_state[3*pixel_pos + 2] = <char>lerp(<int>blue, 0.0, alpha)
