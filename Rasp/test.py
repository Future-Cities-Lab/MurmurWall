import sys
import time
import glob
import serial
import pprint

# Constants
BAUD_RATE = 9600

print ''
print 'Starting up MurmurWall!'
print ''

avail_ports = glob.glob('/dev/tty[A-Za-z]*')

print ''
print 'Here are the available ports : '
print ''

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(avail_ports)

print ''

print 'Getting Teensy Ports......'
print ''

teensy_ports = [avail_ports[x] for x in range(0,6)]

print 'Here are the teensy ports : '
print ''

pp.pprint(teensy_ports)

print ''

print 'Opening ports.......'
print ''

serial_ports = [serial.Serial(port_name, BAUD_RATE, timeout=1) for port_name in teensy_ports]

print 'Serial ports succesfully opened!'
print ''

print 'Starting main loop....'
print ''

input = 'Y'
while input is 'Y':
	for port in serial_ports:
		print 'Writing to ' + port.port + '.........'
		print ">> 'a'"
		print ''
		port.write('a')
		time.sleep(2)
		out = ''
		print 'Recieving from ' + port.port + '...'
		while port.inWaiting() > 0:
			out += port.read(1)
		if out is not '':
			print '>> ' + out
			print ''
		time.sleep(5)
	print 'Again?'
	input = raw_input(">> ")
	print ''

print 'Closing serial ports....'
print '' 

for serial_port in serial_ports: serial_port.close()

print 'Serial ports successfully closed!'
print ''

print 'Bye!'
print ''
