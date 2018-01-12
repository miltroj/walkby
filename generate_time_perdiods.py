from aditional import *

class Generate_time(object):

    def __init__(self,year,month,day,hour=23,minute=55):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute


    def checkFebruary(self):
        if self.year % 4 == 0 and self.year % 100 != 0 or self.year % 400 == 0:
            return 29
        else:
            return 28

    def first_day_of_month(self):
        self.day = 5
        self.hour = 23
        self.minute= 55

    def fifht_day(self):
        daysInMonthDics = {1: 31, 2: self.checkFebruary(), 3:31, 4:30, 5:31 , 6:30, 7:30, 8:31, 9:30, 10:31, 11:30, 12:31}
        self.day = daysInMonthDics[self.month]
        return daysInMonthDics[self.month]

    def jump_to_next_month(self):
        if self.month < 12:
            self.month += 1
            self.day = 1
        else:
            self.month = 1
            self.year += 1
            self.day = 1

    def next_day(self):
        if 2>self.day >= 1:
            self.first_day_of_month()
        elif 5>self.day >= 2:
            self.first_day_of_month()
        elif self.fifht_day() >self.day >= 5:
            self.fifht_day()
        elif self.day == self.fifht_day():
            self.jump_to_next_month()
        args = self.minute,self.hour,self.day,self.month,self.year
        print("Wygenerowano nowy timestamp %s" %create_datetime(*args))
        return create_datetime(*args)

    def next_border_timestemp(self):
        return form_timestamp_from_dtime( self.next_day() ) # zwraca roznice w sekundach pomiedzy 2000 a aktualna data roznicy

if __name__ == "__main__":
    time_window = Generate_time(2018,1,1)

    for i in range(15):
        time_window.next_day()