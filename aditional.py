import datetime


def date_time_now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f") + " "

def int_to_hex_string(list):
    temp_retunr = ''
    for el in list:
        temp_retunr += hex(el).replace("0x",'') + ' '
    print(temp_retunr)
    return temp_retunr.upper()

def int_to_hex_string_(table):
    temp =  ' '.join(format(s,'02x') for s in table).upper()
    print(temp)
    return temp