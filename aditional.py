import datetime
from struct import *


def split_strTab_to_int(tab):
    temp_tab = tab.split(' ')
    return [int(el ,16)for el in temp_tab]

def create_datetime(min,hours,days,months,years):
    return datetime.datetime(second=0,minute=min,hour=hours,day=days,month=months,year=years)

def date_time_now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f") + " "

def date_time_now_short():
    return datetime.datetime.now().strftime("%Y-%m-%d") + " "

def data_time_zero():
    return datetime.datetime(minute=0,second=0,day=1,month=1,year=2000)


#region split_datetime

def month_datetime(datetime):
    year    = int(datetime.strftime("%Y"))
    month   = int(datetime.strftime("%m"))
    day     = int(datetime.strftime("%d"))
    hour    = int(datetime.strftime("%H"))
    minute  = int(datetime.strftime("%M"))
    return year, month, day, hour,minute
#endregion



def int_to_hex_string(list):
    temp_retunr = ''
    for el in list:
        temp_retunr += hex(el).replace("0x",'') + ' '
    print(temp_retunr)
    return temp_retunr.upper()

def int_to_hex_string_(table):
    temp =  ' '.join(format(s,'02x') for s in table).upper()
    # print(temp)
    return temp

def parse_frames_with_date(table):
    temp_string = date_time_now() + int_to_hex_string_(table)
    print(temp_string)
    return temp_string

def cut_sn(int_tab):
    if len(int_tab) > 7:
        return int_tab[3:7]
    elif len(int_tab) == 4:
        return int_tab
    return None

def cut_timestamp(int_tab):
    if len(int_tab) > 11:
        return int_tab[7:11]
    return None

def unpack_four_bytes(four_int_tab):
    return unpack(">I", bytearray(four_int_tab))[0]

def pack_for_bytes(integer):
    return bytearray( pack(">I", integer) )

def locate_unpack_SN(int_tab):
    temp_tab = cut_sn(int_tab)
    if temp_tab is not None:
        return unpack_four_bytes(temp_tab)
    else:
        print("Zbyt krotka ramka - nie odczytano numeru SN")
        return None

def locate_unpack_timestamp(int_tab):
    temp_tab = cut_timestamp(int_tab)
    if temp_tab is not None:
        return unpack_four_bytes(temp_tab)
    else:
        print("Zbyt krotka ramka - nie znaleziono timestampa")
        return None

def pack_SN_or_timestamp(integer):
    return [el for el in pack_for_bytes(integer)]

#timestamp in seconds
def form_timestamp_from_dtime(date_time):
    print(date_time)
    return int((date_time - data_time_zero()).total_seconds())

def convert_frame_to_char(list_of_int):
    frame = ''
    for element in list_of_int:
        frame += chr(element)
    # print "%r" %frame
    return frame

def is_propper_SN_in_the_list(frame , SN_list):
    if locate_unpack_SN(frame) in SN_list:
        return True
    elif len(SN_list) == 0:
        return True
    else:
        return False

def time_inside_frame(list_of_bytes):
    temp_time_int = locate_unpack_timestamp(list_of_bytes)
    if temp_time_int is None:
        return ''
    else:
        return (data_time_zero() + datetime.timedelta(seconds=temp_time_int)).strftime("%Y-%m-%d %H:%M:%S") + " | "


def log_to_file_write(func):
    def func_wrapper(self, frame):
        temp_frame_string = " ".join(format(byteInt, '02x') for byteInt in frame).upper()
        with open("log/loger-{}.txt".format(date_time_now_short()), 'a') as file:
            file.write(date_time_now() + " SND " + time_inside_frame(frame)  + temp_frame_string + "\n")
        return func(self , frame)
    return func_wrapper

def log_to_file_read(func):
    def func_wrapper(self):
        temp_func_return = func(self)
        if temp_func_return is not None:
            temp_frame_string = " ".join(format(byteInt, '02x') for byteInt in temp_func_return).upper()
            with open("log/loger-{}.txt".format(date_time_now_short()), 'a') as file:
                file.write(date_time_now() + " RCV " + time_inside_frame(temp_func_return) + temp_frame_string + "\n")
        return temp_func_return
    return func_wrapper

if __name__ == "__main__":

    frame_sample = '3E A2 0B 77 35 EE 6E 21 E9 E5 65 31 12 06 F0 10 E6 00 12 FB FC 00 DB DB 10 5B 10 6D 00 50 00 00 84 80 00 33 10 10 10 00 00 00 23 00 00 00 10 04 10 2B 00 00 3C 00 02 00 01 E9 10 E8 10 00 A0'

    list_of_bytes = split_strTab_to_int(frame_sample)

    print("%r" %list_of_bytes)
    print("%r" %cut_timestamp(list_of_bytes))

    print("Rozpakowany SN %r" %locate_unpack_SN(list_of_bytes))
    seconds_from_timestamp = locate_unpack_timestamp(list_of_bytes)
    print("Rozpakowany timestamp w sekundach %r" %seconds_from_timestamp)


    data_czas =datetime.datetime(minute=0,second=0,day=1,month=1,year=2000)
    print(data_czas)
    time_delta = datetime.timedelta(seconds=seconds_from_timestamp)
    print(time_delta)

    actual_time = time_delta + data_czas
    print(actual_time)

    to_timestamp = actual_time - data_czas
    print(int(to_timestamp.total_seconds()))
    timestamp_to_pack = int(to_timestamp.total_seconds())
    packed = pack_for_bytes(timestamp_to_pack)
    print(" ".join( format(hex(el)) for el in packed))

    timestamp_table = [el for el in packed]
    print("%r" %timestamp_table)

    print("packed sn %r" %pack_SN_or_timestamp(2000023150))

    print(month_datetime(datetime.datetime.now()))

    arg = 55, 23, 1, 1, 2017
    piaty_start = pack_for_bytes(  form_timestamp_from_dtime(create_datetime(*arg)))

    print ("%r" %piaty_start)

    for el in piaty_start:
        print("%r" %hex(el))


    # timestamp z ramki na konsole parsowanie
    czas_int  = locate_unpack_timestamp(list_of_bytes)
    print(czas_int)
    calkowity_czas = data_time_zero() + datetime.timedelta(seconds=czas_int)
    print(calkowity_czas)
    print(type( calkowity_czas.strftime("%Y-%m-%d %H:%M:%S:%f")))
    print(time_inside_frame(list_of_bytes))