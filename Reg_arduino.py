import serial
from serial import Serial
import time
import schedule
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import datetime
import gspread
from gspread.models import Worksheet
from datetime import date
import calendar

serial=serial.Serial('COM3', baudrate=9600)

def push_data_to_cloud(data):
            scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                    "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
            gc = gspread.service_account(filename='pqt13.json')
            sh = gc.open_by_key('1rPuDSwwoylWiGNfplsmVjYWw0y2hFiDs-ixJ0EbbF9w')
            Worksheet= sh.worksheet('Sheet2')
            creds_sample = ServiceAccountCredentials.from_json_keyfile_name("pqt13.json", scope)
            client = gspread.authorize(creds_sample)
            sheet = sh.worksheet('Sheet2')
            f2=datetime.datetime.now().strftime("%H:%M:%S")
            f3=str(datetime.date.today())
            my_date = date.today()
            day=calendar.day_name[my_date.weekday()]
            """cell=Worksheet.find(data[0:-1])"""

            list_of_lists=Worksheet.get_all_values()
            count_bill=0
            count_treatment=0
            week=1
            for i in list_of_lists:
                if data[0:-1]==i[0]:
                    """doctor=i[5]"""
                    day=i[2]
                    """time_of_bill=i[6]"""
                    if i[2]=='Monday' and list_of_lists[list_of_lists.index(i)-1][2] == 'Sunday':
                        week=int(list_of_lists[list_of_lists.index(i)-1][1])+1
                    else:
                        week=int(list_of_lists[list_of_lists.index(i)-1][1])
            data_to_append = [f3,f2,data[0:-1],day,week]          
            sheet.append_row(data_to_append)
            print("data pushed")

while True:
    if serial.inWaiting()>0:
        read_result=serial.readline()
        data= read_result.decode("utf-8","replace")
        print(data)
        push_data_to_cloud(data)



        
       