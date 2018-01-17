from aditional import *
from generate_time_perdiods import *

class Create_frames(object):

    def __init__(self,int_SN, start_time, Port_COM_class=None):
        #region INITIALS
        self.delta = 5*60 #
        self.sn = pack_SN_or_timestamp(int_SN)
        self.start_time_timestamp_rw_seconds = form_timestamp_from_dtime(  start_time )
        self.nex_day_rw_seconds = self.start_time_timestamp_rw_seconds + self.delta
        self.adress = 0xAA
        self.key = 0x20
        self.OMT = 30
        args = month_datetime(start_time)
        self.GeneratePeriods = Generate_time(*args)
        self.Port_COM_Class = Port_COM_class

        self.frame_already_send =[]
        #timeout dla ramki pierwszej
        self.actula_timeout_first_frame = 0
        #timeout dla ramki regularnej
        self.actula_timeout = 0
        self.ACK_timeout = 11

        self.generate_and_send_frame = False
        self.first_frame = True
        self.first_frame_ack=True
        #endregion
        #region FRAME

        # self.frame = [0x3D ,0xFF ,0x16 ,self.sn[0] ,self.sn[1] ,self.sn[2] ,self.sn[3] ,0x20
        #     ,0x01 ,0x99 ,0x54 ,0x31 ,0x12 ,0x15 ,0x05 ,0x15 ,0x09
        #     ,0x01 ,0x09 ,0x31 ,0x03 ,0x17 ,0x01 ,0x01 ,0x00 ,0x24
        #     ,0x7F ,self.OMT ,self.key ,self.key ,0x28 ,0x8C ,0x17 ,0x03 ,0x19
        #     ,0x04 ,0x03 ,0x55 ,0x02 ,0x01 ,0x32 ,0x00 ,0x00 ,0x00
        #     ,0x01 ,self.adress ,0x00 ,0x03 ,0x17 ,0x04 ,0x22 ,0x11 ,0x10
        #     ,0x0F ,0x4E ,0x20 ,0x13 ,0x88 ,0x82 ,0x64 ,0x66 ,0x09]

        # self.frame = [0x3D ,0xFF ,0x16 ,self.sn[0] ,self.sn[1] ,self.sn[2] ,self.sn[3] ,0x1F
        #     ,0xFC ,0x53 ,0x54 ,0x31 ,0x12 ,0x15 ,0x05 ,0x15 ,0x09
        #     ,0x01 ,0x09 ,0x31 ,0x03 ,0x17 ,0x01 ,0x01 ,0x00 ,0x24
        #     ,0x7F ,self.OMT ,self.key ,self.key ,0x28 ,0x8C ,0x17 ,0x03 ,0x19
        #     ,0x04 ,0x03 ,0x55 ,0x02 ,0x01 ,0x32 ,0x00 ,0x00 ,0x00
        #     ,0x01 ,self.adress ,0x00 ,0x03 ,0x17 ,0x04 ,0x22 ,0x11 ,0x10
        #     ,0x0F ,0x4E ,0x20 ,0x13 ,0x88 ,0x82 ,0x64 ,0x66 ,0x09]

        self.frame = [0x3D ,0xFF ,0x16 ,self.sn[0] ,self.sn[1] ,self.sn[2] ,self.sn[3] ,0x1F
            ,0xFC ,0x53 ,0x54 ,0x31 ,0x12 ,0x15 ,0x05 ,0x15 ,0x09
            ,0x01 ,0x09 ,0x31 ,0x03 ,0x18 ,0x01 ,0x15 ,0x00 ,0x24
            ,0x7F ,self.OMT ,self.key ,self.key ,0x28 ,0x8D ,0x17 ,0x00 ,0x24
            ,0x04 ,0x03 ,0x55 ,0x02 ,0x11 ,0x35 ,0x00 ,0x00 ,0x00
            ,0x01 ,self.adress ,0x00 ,0x03 ,0x18 ,0x01 ,0x15 ,0x12 ,0x10
            ,0x0B ,0x4E ,0x20 ,0x13 ,0x88 ,0x82 ,0x64 ,0x66 ,0x09]

        self.ack = [0x08 ,0xFF ,0x96 ,self.sn[0] ,self.sn[1] ,self.sn[2] ,self.sn[3] ,0x00, 0x00]

        #endregion
    def insert_timestamp_toFrame_bytes(self):
        self.frame[7:11] = pack_SN_or_timestamp(self.start_time_timestamp_rw_seconds)

    def add_timestamp_border(self):
        self.nex_day_rw_seconds = self.start_time_timestamp_rw_seconds + self.delta

    def create_new_border(self):
        self.start_time_timestamp_rw_seconds = self.GeneratePeriods.next_border_timestemp()
        self.add_timestamp_border()
        self.insert_timestamp_toFrame_bytes()
        print("\n         STWORZONO NOWE GRANICE WYSYLANIA start %r  stop %r\n"
              %(secods_to_datetime(self.start_time_timestamp_rw_seconds),secods_to_datetime(self.nex_day_rw_seconds)))


    def is_propper_SN(self,frame):
        # print(locate_unpack_SN(frame))
        # print(locate_unpack_SN(self.sn))
        # print(self.sn)
        if locate_unpack_SN(frame) == locate_unpack_SN(self.sn):
            return True
        else:
            return False

    def reset_ACK_timeout(self):
        self.actula_timeout = 0

    def check_frame_timestamp(self,frame):
        return locate_unpack_timestamp(frame)
    
    def remamber_previous_frame(self):
        self.frame_already_send = self.frame

    def send_first_frame_and_wait_for_ACK(self,frame_int_list):
        if self.first_frame:
            print("\n         WYSLANIE RAMKI PO RAZ PIERWSZY\n")
            self.insert_timestamp_toFrame_bytes()
            self.Port_COM_Class.write(self.frame)
            self.first_frame = False
        elif frame_int_list == self.ack and self.first_frame_ack:
            self.generate_and_send_frame = True
            self.first_frame_ack = False
            print("\n         ODEBRANIE RAMKI OD PIERWSZEJ PO ACK\n")

    def generate_and_write_frame(self,frame_int_list):
        tmp_timestamp_from_frame = self.check_frame_timestamp(frame_int_list)
        if tmp_timestamp_from_frame > self.nex_day_rw_seconds and self.generate_and_send_frame and is_propper_frame_type(frame_int_list):
            self.create_new_border()
            self.Port_COM_Class.write(self.frame)
            self.generate_and_send_frame = False
            print("\n         WYSLANIE RAMKI OD WYGENEROWANEJ\n")
        elif frame_int_list == self.ack and self.generate_and_send_frame == False and self.first_frame_ack == False:
            print("Zauwazono potwierdzenie odebrania dla podzielnika %r\n" % locate_unpack_SN(frame_int_list))
            self.generate_and_send_frame = True
            print("\n         ODEBRANIE RAMKI PO ACK OD WYGENEROWANEJ\n")

    def ack_out_of_time(self,frame_int_list):
        if frame_int_list != self.ack and self.first_frame_ack:
            print("\n         ODEBRANIE RAMKI CZEKAM NA ACK PIERWSZEJ - JESZCZE %r\n" % (
            self.ACK_timeout - self.actula_timeout_first_frame))
            self.check_ACK_timeout_first_frame()
        elif self.check_frame_timestamp(
                frame_int_list) > self.nex_day_rw_seconds and self.generate_and_send_frame == False and is_propper_frame_type(
                frame_int_list):
            print("\n         ODEBRANIE RAMKI CZEKAM NA ACK - JESZCZE %r\n" % (self.ACK_timeout - self.actula_timeout))
            self.check_ACK_timeout_general_frame()
        else:
            # self.generate_and_send_frame = True
            print("%r oczekuje wyzszego timestampa - aktualnie %s\n" % (
            locate_unpack_SN(frame_int_list), time_inside_frame(frame_int_list)))

    def check_ACK_timeout_first_frame(self):
        self.actula_timeout_first_frame += 1
        if self.actula_timeout_first_frame > self.ACK_timeout:
            self.first_frame = True
            self.actula_timeout_first_frame = 0
            print("\n         WYSTAPIL TIMEOUT OD RAMKI GLOWNEJ\n")

    def check_ACK_timeout_general_frame(self):
        self.actula_timeout += 1
        if self.actula_timeout > self.ACK_timeout:
            self.generate_and_send_frame = True
            self.actula_timeout = 0
            print("\n         WYSTAPIL TIMEOUT OD RAMKI PIERWSZEJ\n")

    def check_if_time_to_send(self, frame_int_list):
        if self.is_propper_SN(frame_int_list):

            self.send_first_frame_and_wait_for_ACK(frame_int_list)
            self.generate_and_write_frame(frame_int_list)
            self.ack_out_of_time(frame_int_list)



if __name__ == "__main__":

    frame_sample        = '3E A2 0B 77 35 EE 6E 21 E9 E5 65 31 12 06 F0 10 E6 00 12 FB FC 00 DB DB 10 5B 10 6D 00 50 00 00 84 80 00 33 10 10 10 00 00 00 23 00 00 00 10 04 10 2B 00 00 3C 00 02 00 01 E9 10 E8 10 00 A0'
    frame_sample_higher = '3D FF 16 77 35 EE 6E 22 15 13 D4 31 12 15 05 15 09 01 09 31 03 17 01 01 00 24 7F 14 00 00 28 8C 17 03 19 04 03 55 02 01 32 00 00 00 01 DD 00 03 17 04 22 11 10 0F 4E 20 13 88 82 64 66 09'



    list_of_bytes = split_strTab_to_int(frame_sample)
    list_of_bytes_higher = split_strTab_to_int(frame_sample_higher)

    start_time = create_datetime(min=55, hours=23, days=1, months=1, years=2018)
    # print(start_time)
    # print(start_time.date())

    create_frame = Create_frames(int_SN=2000023150, start_time=start_time)
    #
    # print(int_to_hex_string_(create_frame.frame))
    # print(create_frame.start_time_timestamp_rw_seconds)
    # print(create_frame.nex_day_rw_seconds)
    #
    # create_frame.insert_timestamp_toFrame_bytes()
    #
    # print(int_to_hex_string_(create_frame.frame))

    # for i in range(7):
    #     create_frame.check_if_time_to_send(list_of_bytes)
    #     print(int_to_hex_string_(create_frame.frame))
    #
    # create_frame.check_if_time_to_send(list_of_bytes_higher)
    # print(int_to_hex_string_(create_frame.frame))

    print(create_frame.frame[28:30])

    print(is_propper_frame_type(list_of_bytes))