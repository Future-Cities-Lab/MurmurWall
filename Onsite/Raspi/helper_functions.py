import glob
import platform
import time
import serial

BAUD_RATE = 115200
TIMEOUT = None

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
    current_ports = get_available_ports()
    print 'Available Ports are : \n'
    print current_ports
    print ''

    if platform.system() == "Darwin":
        for port in current_ports:
            if 'Bluetooth' not in port:
                print port
                pot_port = serial.Serial(port, BAUD_RATE, timeout=TIMEOUT)
                time.sleep(1)
                pot_port.write('#')
                time.sleep(1)
                response = pot_port.read(1)
                print response
                if response is 'a':
                    matrix_port = pot_port
                elif response is 'b':
                    led_port = pot_port
        matrix_port.flushInput()
        led_port.flushInput()
    else:
        for port in current_ports:
            if 'ACM' in port:
                print port
                pot_port = serial.Serial(port, BAUD_RATE, timeout=TIMEOUT)
                print pot_port.inWaiting()
                pot_port.flushInput()
                print pot_port.inWaiting()
                while pot_port.inWaiting() == 0:
                     pot_port.flushInput()
                     time.sleep(1)
                     pot_port.write('#')
                     time.sleep(1)
                     print pot_port.inWaiting()
                response = pot_port.read(1)
                pot_port.flushInput()
                print response
                if response is 'a':
                    matrix_port = pot_port
                elif response is 'b':
                    led_port = pot_port
    
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
        
