from serial_port import *
from aditional import *



port = Port('COM7')


while True:


    frame = port.read_frames()
    # int_to_hex_string_(frame)