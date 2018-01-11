from serial_port import *
from create_frames import *

start_time= create_datetime(min=55,hours=23,days=12,months=10,years=2018)

#region classes
try:
    port = Port('COM7')
    create_frame = Create_frames(int_SN=2000023150,start_time=start_time,Port_COM_class=port)
except:
    print("Problem w inicjalizacji portu")
#endregion

while True:


    frame = port.read_frames()
    # int_to_hex_string_(frame)