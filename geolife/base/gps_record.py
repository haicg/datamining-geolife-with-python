#!/usr/bin/python
#  File Name : gps_record.py

import time
import logging

LOG_HANDLE = None

class gps_record:
    def __init__(self):
        self.gps_userid = -1
        self.gps_latitude = 0.0
        self.gps_longitude = 0.0
        self.gps_code = 0
        self.gps_altitude = 0.0
        self.gps_date = None
        self.gps_time = None
        self.gps_UTC_timestamp = None

    def __init_with_txt_record__(self, recordStr, userid):
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
        return self
    
    def __init_with_query_sql__(self, recordRes):
        global LOG_HANDLE
        try:
            self.gps_userid = recordRes[0]
            self.gps_latitude = recordRes[1]
            self.gps_longitude = recordRes[2]
            self.gps_code = recordRes[3]
            self.gps_altitude = recordRes[4]
            self.gps_UTC_timestamp = recordRes[5]
            self.gps_UTC_unix_timestamp = recordRes[6]

        except ValueError :
            print "Value Error " 
            #logging.warning("Value Error " + userid + recordStr)
            raise ValueError
        return self
    def printClass(self):
        print self.gps_userid 
        print self.gps_latitude
        print self.gps_longitude 
        print self.gps_code
        print self.gps_altitude
        print self.gps_UTC_timestamp
        print self.gps_UTC_unix_timestamp
