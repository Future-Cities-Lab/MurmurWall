import glob
import platform
import serial
import time

NUM_PIXELS = 57
TIME_DELAY = 6500

def get_available_ports():
    if platform.system() == "Darwin":
        return glob.glob('/dev/tty.*')
    else:
        return glob.glob('/dev/ttyS*') + glob.glob('/dev/ttyUSB*')

def my_range(start, stop, step):
    while start < stop:
        yield start
        start += step

def main():

    led_state = [chr(x*0) for x in range(0, 3*57)]

    led_port = serial.Serial(get_available_ports()[2], 115200, timeout=1)

    particle_position = 0


    while True:

        for position in my_range(0, 3*57, 3):
            led_state[position] = chr(0)
            led_state[position+1] = chr(0)
            led_state[position+2] = chr(0)

        if particle_position is 56:
            particle_position = 0

        particle_position += 1
        
        led_state[particle_position*3] = chr(0)
        led_state[particle_position*3 + 1] = chr(0)
        led_state[particle_position*3 + 2] = chr(255)

        particle_position += 1

        led_port.write(led_state)

        # print led_state

        # out = ''
        # while led_port.inWaiting() > 0:
        #     out += led_port.read(1)
        # if out is not '':
        #     print '>> ' + out
        #     print ''
        
        time.sleep(0.116)


if __name__ == "__main__":
    print 'running main animation............'
    main()
