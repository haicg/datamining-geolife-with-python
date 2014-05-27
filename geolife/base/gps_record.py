#!/usr/bin/python
#  File Name : gps_record.py

import time
import logging

class gps_record:
    def __init__(self, recordStr, userid):
       
        global LOG_HANDLE
        record = recordStr.split(',');	
        try:
            self.gps_userid = int(userid)
            self.gps_latitude = float(record[0])
            self.gps_longitude = float(record[1])
            self.gps_code = int(record[2])
            self.gps_altitude = float(record[3])
            self.gps_date = record[5]
            self.gps_time = record[6]
            time_str = (self.gps_date+' '+self.gps_time).rstrip()
            self.gps_UTC_timestamp = time_str
        except ValueError :
            print "Value Error " 
            #logging.warning("Value Error " + userid + recordStr)
            raise ValueError
        try:
            timeArray = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            self.gps_UTC_unix_timestamp = int(time.mktime(timeArray))
        except ValueError:
            print 'unconverted data remains'
            #logging.warning("unconverted data remains " + userid + recordStr)
            raise ValueError
