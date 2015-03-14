"""
Module provides functions for managing the ports
"""

import serial
from glob import glob
from platform import system
from time import sleep


BAUD_RATE = 115200
TIMEOUT = None

def get_available_ports():
    """
    Returns serial ports available to system
    """
    if system() == "Darwin":
        port_address = '/dev/tty.*'
    else:
        port_address = '/dev/tty[A-Za-z]*'
    return glob(port_address) 

def check_port_response(port_to_check):
    """
    send a msg to different ports to correctly indentify them
    """
    print port_to_check.inWaiting()
    port_to_check.flushInput()
    print port_to_check.inWaiting()
    port_to_check.write('#')
    while port_to_check.inWaiting() == 0:
        port_to_check.flushInput()
        sleep(1)
        port_to_check.write('#')
        sleep(1)
        print port_to_check.inWaiting()
    response = port_to_check.read(1)
    port_to_check.flushInput()
    return response

def get_ports():
    """
    Returns the correct ports to be used by the hardware
    """
    current_ports = get_available_ports()
    print 'Available Ports are : \n%s\n' % (current_ports,)
    
    potential_ports = []
    for port in current_ports:
        if system() == "Darwin" and 'Bluetooth' not in port or system() != "Darwin" and 'ACM' in port:
            potential_ports.append(port) 
    for pot_port in potential_ports:
        print pot_port
        port_to_check = serial.Serial(pot_port, BAUD_RATE, timeout=TIMEOUT)
        response = check_port_response(port_to_check)
        print response
        if response is 'g':
            matrix_port_6 = port_to_check
        elif response is 'f':
            matrix_port_5 = port_to_check
        elif response is 'e':
            matrix_port_4 = port_to_check           
        elif response is 'd':
            matrix_port_3 = port_to_check
        elif response is 'c':
            matrix_port_2 = port_to_check
        elif response is 'b':
            matrix_port_1 = port_to_check
        elif response is 'a':
            led_port = port_to_check
    
    print '\nLED Port : \n%s\n' % (led_port,)

    print '\nMatrix Port 1: \n%s\n' % (matrix_port_1,)

    print '\nMatrix Port 2 : \n%s\n' % (matrix_port_2,)

    print '\nMatrix Port 3 : \n%s\n' % (matrix_port_3,)

    print '\nMatrix Port 4 : \n%s\n' % (matrix_port_4,)

    print '\nMatrix Port 5 : \n%s\n' % (matrix_port_5,)

    print '\nMatrix Port 6 : \n%s\n' % (matrix_port_6,)

    return led_port, matrix_port_1, matrix_port_2, matrix_port_3, matrix_port_4, matrix_port_5, matrix_port_6

def main():
    """ 
    Used to test this module

    """
    print get_ports()

if __name__ == "__main__":
    main()
