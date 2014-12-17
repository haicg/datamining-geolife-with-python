###File Name:stay_point.py
###Author:haicg
###Mail:lihaicg@126.com
###Created Time: 2014/6/6 15:26:42
###File Name : stay_point.py
#!/usr/bin/python

import time
import logging


LOG_HANDLE = None

class stay_point:
    def __init__(self):
        self.userid= -1
        self.arrival_point = -1
        self.arrival_timestamp = 0
        self.leaving_point = -1
        self.leaving_timestamp = 0
        self.mean_coordinate_latitude = None
        self.mean_coordinate_longtitude = None
        self.mean_coordinate_altitude = None
    def printSelf(self):
        print "userid = %d" %self.userid
        print "arrival_point = %d" %self.arrival_point
        print "arrival_timestamp = %d \n arrival_timestr=%s" %(self.arrival_timestamp, time.ctime(self.arrival_timestamp))
        print "leaving_point = %d" %(self.leaving_point)
        print "leaving_timestamp = %d \n leaving_timestr=%s" %(self.leaving_timestamp, time.ctime(self.leaving_timestamp))
        print "mean_coordinate_latitude = %f" %self.mean_coordinate_latitude
        print "mean_coordinate_longtitude = %f" %self.mean_coordinate_longtitude
        print "mean_coordinate_altitude = %f" %self.mean_coordinate_altitude
        

