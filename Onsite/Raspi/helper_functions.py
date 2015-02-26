import glob
import platform
import time
import serial

BAUD_RATE = 115200
TIMEOUT = 1

def get_available_ports():
    """
    Returns serial ports available to system
    """
    if platform.system() == "Darwin":
        return glob.glob('/dev/tty.*')
    else:
        return glob.glob('/dev/tty[A-Za-z]*')

def get_ports():
    """
    Returns the correct ports to be used by the hardware
    """
    # TODO: FIGURE OUT WHY THIS FAILS SOMETIMES......
    current_ports = get_available_ports()
    print 'Available Ports are : \n'
    print current_ports
    print ''
    
    for i in range(0, 2):
        if platform.system() == "Darwin":
            pos = 2+i
        else:
            pos = i
        port = serial.Serial(current_ports[pos], BAUD_RATE, timeout=TIMEOUT)
        time.sleep(1.516)
        port.flushInput()
        port.flushOutput()
        port.write('#')
        time.sleep(1.516)
        out = ''
        print "Reading MAC Address...."
        while port.inWaiting() > 0:
            out += port.read(1)
            print out
        if out == '04:E9:E5:00:EC:51':
            led_port = port
        elif out == '04:E9:E5:01:0C:E0':
            matrix_port = port     
    
    print '\nFound LED Port, it is : \n'
    print led_port
    print ''

    print '\nnFound Matrix Port, it is : \n'
    print matrix_port
    print ''

    return led_port, matrix_port

def my_range(start, stop, step):
    """
    returns iterator that moves by a given step
    """
    while start < stop:
        yield start
        start += step

def map_values(value, i_start, i_stop, o_start, o_stop): 
    """
    Input: Stream of values, start and stop. Start and stop of output values
    Ouput: A mapping of the input to the output values
    """
    return o_start + (o_stop - o_start) * ((value - i_start) / (i_stop - i_start))

def lerp(color2, color1, amt):
    """
    c1,c2 - Colors to interpolate between
    amt - amount of interpolation
    Returns: interpotalted color
    """
    return round(color1 + (color2-color1)*amt)
        
