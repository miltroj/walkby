from serial_port import *
from create_frames import *

start_time= create_datetime(min=55,hours=23,days=1,months=1,years=2017)

#region classes
try:
    port = Port('COM7')
    create_frame = Create_frames(int_SN=2000004927,start_time=start_time,Port_COM_class=port)
except:
    print("Problem w inicjalizacji portu")
#endregion

while True:


    frame = port.read_frames()
    create_frame.check_if_time_to_send(frame)