from serial_port import *
from create_frames import *

start_time= create_datetime(min=55,hours=23,days=31,months=5,years=2017)
COM = 'COM7'
#region classes
try:
    port = Port(COM)
    create_frame_Podzielnik_1 = Create_frames(int_SN=2000040811,start_time=start_time,Port_COM_class=port)
    # create_frame_Podzielnik_2 = Create_frames(int_SN=2000040811,start_time=start_time,Port_COM_class=port)
    # create_frame_Podzielnik_3 = Create_frames(int_SN=2000040811,start_time=start_time,Port_COM_class=port)
    # create_frame_Podzielnik_4 = Create_frames(int_SN=2000040811,start_time=start_time,Port_COM_class=port)
except:
    print("Problem w inicjalizacji portu")
#endregion

port.filtered_SN = [2000040811] #wewnatrz filtrowane SNy przykladowo [2000004927,2000004921,itd]
# Klucz = 2020
# adres = DD
# OMT   = 30
# nadawanie 27/7

while True:

    received_frame = port.read_frames()
    # create_frame_Podzielnik_1.check_if_time_to_send(received_frame)