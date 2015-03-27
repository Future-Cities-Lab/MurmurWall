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

from libc.math cimport round
from libc.stdlib cimport atoi


ORIG = [100.0, 25.0, 10.0, 5]
DIFF = [75.0, 15.0, 5.0, 2.0]

def map_values(double value, double i_start, double i_stop, double o_start, double o_stop): 
    return o_start + (o_stop - o_start) * ((value - i_start) / (i_stop - i_start))

def lerp(int channel_2, int channel_1, double amt):
    return round(channel_1 + (channel_2 - channel_1) * amt)

def color_strand_for_packet(list color_state, double current_position, bytes red, bytes green, bytes blue, int prev_target_position, int target_position):
    cdef int middle_pixel
    cdef double current_count

    middle_pixel = <int>(current_position + 0.00001)

    color_state[3*(middle_pixel+1)] = red
    color_state[3*(middle_pixel+1) + 1] = green
    color_state[3*(middle_pixel+1) + 2] = blue

    current_count = current_position - middle_pixel
    curve = []
    for i in range(-2, 4):
        if i < 0:
            i = i * -1
        curve.append(ORIG[i] - (DIFF[i] * current_count))

    cdef int pixel_pos
    cdef double alpha
    cdef int new_red, new_green, new_blue
    for i in range(-2, 4):
        if i > 0:
            pixel_pos = middle_pixel + i + 1
        else:
            pixel_pos = middle_pixel + i
        if pixel_pos > prev_target_position and pixel_pos < target_position:
            alpha = map_values(curve[i+2], 0.0, 100.0, 0.0, 1.0)
            new_red = lerp(float(ord(red)), 0.0, alpha)
            new_green = lerp(float(ord(green)), 0.0, alpha)
            new_blue = lerp(float(ord(blue)), 0.0, alpha)
            color_state[3*pixel_pos] = chr(new_red)
            color_state[3*pixel_pos + 1] = chr(new_green)
            color_state[3*pixel_pos + 2] = chr(new_blue)

def color_pod_for_packet(list color_state, double current_position, bytes red, bytes green, bytes blue):

    cdef int middle_pixel
    cdef double current_count

    middle_pixel = <int>(current_position + 0.00001)

    current_count = current_position - middle_pixel

    curve = []
    for i in range(-2, 4):
        if i < 0:
            i = i * -1
        curve.append(ORIG[i] - (DIFF[i] * current_count))

    cdef int pos, by_pos, pixel_pos
    cdef double alpha
    cdef int new_red, new_green, new_blue
    for i in range(0, 5):
        pos = 0
        if i % 2 == 0:
            pos = middle_pixel + (i*12)
        else:
            by_pos = 300 + ((i+1)*12)
            pos = 2*(by_pos) - (middle_pixel + ((i+1)*12) + 1)
        for j in range(-2, 4):
            if i % 2 == 0:
                pixel_pos = pos + j
                if pixel_pos >= 300 + (i*12) and pixel_pos <= 300 + (i*12) + 11:
                    alpha = map_values(curve[j+2], 0.0, 100.0, 0.0, 1.0)
                    new_red = lerp(float(ord(red)), 0.0, alpha)
                    new_green = lerp(float(ord(green)), 0.0, alpha)
                    new_blue = lerp(float(ord(blue)), 0.0, alpha)
                    color_state[3*pixel_pos] = chr(new_red)
                    color_state[3*pixel_pos + 1] = chr(new_green)
                    color_state[3*pixel_pos + 2] = chr(new_blue)
