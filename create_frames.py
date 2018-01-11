from aditional import *

class Create_frames(object):

    def __init__(self,int_SN, start_time):
        self.sn = pack_SN_or_timestamp(int_SN)
        self.start_time_timestamp_rw_seconds = form_timestamp_from_dtime(  start_time )
        self.nex_day_rw_seconds = self.start_time_timestamp_rw_seconds + 5*60 #ustawia nastepny dzien na 5 min pozniej
        self.adress = 0xDD

        #region FRAME

        self.frame = [0x3D ,0xFF ,0x16 ,self.sn[0] ,self.sn[1] ,self.sn[2] ,self.sn[3] ,0x1F
            ,0xFC ,0x54 ,0x08 ,0x31 ,0x12 ,0x15 ,0x05 ,0x15 ,0x09
            ,0x01 ,0x09 ,0x31 ,0x03 ,0x17 ,0x01 ,0x01 ,0x00 ,0x24
            ,0x7F ,0x14 ,0x00 ,0x00 ,0x28 ,0x8C ,0x17 ,0x03 ,0x19
            ,0x04 ,0x03 ,0x55 ,0x02 ,0x01 ,0x32 ,0x00 ,0x00 ,0x00
            ,0x01 ,self.adress ,0x00 ,0x03 ,0x17 ,0x04 ,0x22 ,0x11 ,0x10
            ,0x0F ,0x4E ,0x20 ,0x13 ,0x88 ,0x82 ,0x64 ,0x66 ,0x09]

        #endregion
    def insert_timestamp_toFrame_rw_seconds(self):
        self.frame[7:11] = pack_SN_or_timestamp(self.start_time_timestamp_rw_seconds)




if __name__ == "__main__":
    start_time = create_datetime(min=55, hours=23, days=12, months=10, years=2018)
    print(start_time)
    print(start_time.date())
    create_frame = Create_frames(int_SN=2000023150, start_time=start_time)

    print(int_to_hex_string_(create_frame.frame))
    print(create_frame.start_time_timestamp_rw_seconds)
    print(create_frame.nex_day_rw_seconds)

    create_frame.insert_timestamp_toFrame_rw_seconds()

    print(int_to_hex_string_(create_frame.frame))