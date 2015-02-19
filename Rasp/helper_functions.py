import glob
import platform

def get_available_ports():
    if platform.system() == "Darwin":
        return glob.glob('/dev/tty.*')
    else:
        return glob.glob('/dev/tty[A-Za-z]*')

def my_range(start, stop, step):
    while start < stop:
        yield start
        start += step
        