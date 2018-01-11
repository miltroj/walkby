import serial
from aditional import *

class Port(object):

    def __init__(self, port_Com):
        self.COM_port = port_Com
        self.serial_opened = serial.Serial(self.COM_port, baudrate=11520, dsrdtr = True, timeout=.1)


    def read_frames(self):
        while True:
            returned = []
            if self.serial_opened.inWaiting() != 0:
                temp_read = self.serial_opened.read(1)
                size = ord(temp_read[0])
                returned = [ ord(temp_read[0])]
                while len(temp_read) < size + 1:
                    if self.serial_opened.inWaiting() == 0:
                        break
                    readed = self.serial_opened.read(1)
                    returned.append(  ord(readed) )
                # print("%s %r" % (date_time_now(), returned))
                parse_frames_with_date(returned)
                return returned

    def write(self, frame):
        self.serial_opened.flushInput()
        self.serial_opened.write(frame)