###File Name:filter_points.py
###Author:haicg
###Mail:lihaicg@126.com
###Created Time: Mon 07 Jul 2014 08:30:16 PM HKT
###File Name : filter_points.py
#!/usr/bin/python

import sys
import os
sys.path.append("..")
sys.path.append(".")
from sql_base import dbutils
from base import gps_record
from base import base_op
import logging.config
import logging
import math

logger = None

class CurrentGPSRecordList:
    def __init__(self):
        self.gps_list = None
        self.currentPos = 0

currentRecordList = CurrentGPSRecordList()
currentIndex = 0
column_name = ("gps_userid", "gps_latitude", "gps_longitude", "gps_code",\
       "gps_altitude", "gps_UTC_timestamp", "gps_UTC_unix_timestamp")

def log_init():
    global logger
    if(logger == None):
        if (os.path.exists(r"logger.conf")):
            logging.config.fileConfig("logger.conf")
        else:
            logging.config.fileConfig(r"../logger.conf")

        logger = logging.getLogger("root")
    return logger

#def getPreviousRecord():

def getNextRecord(userId):
    global currentRecordList
    global currentIndex
    if (not currentRecordList.gps_list) or (currentRecordList.currentPos == \
            len(currentRecordList.gps_list)) :
        currentRecordList.gps_list = \
            dbutils.get_gps_record_time_order(userId, currentIndex, 20000)
        if (not currentRecordList.gps_list) :
            currentIndex = 0
            currentRecordList.gps_list = None
            raise ValueError,'no more gps record'
            return None
        currentRecordList.currentPos = 0

    res = currentRecordList.gps_list[currentRecordList.currentPos]
    currentIndex += 1
    currentRecordList.currentPos += 1
    return res

''' The unit of the speed is km/h '''
def getSpeed(currentPoint, nextPoint):
    euclidean_distence = base_op.get_distance(currentPoint, nextPoint)
    #print "distence = %f km" % euclidean_distence
    time_tmp = nextPoint.gps_UTC_unix_timestamp - currentPoint.gps_UTC_unix_timestamp
    try :
        speedVal = euclidean_distence*3600/abs(time_tmp)
    except ZeroDivisionError:
        raise
    return speedVal

def storeErrorPoint(errorPoint):
    errorPoint.show()
    errorPoint.save("errorPoint.txt")

def filterUserRecords(userid = 1):
    i =0
    errorCount = 0
    oneUserTotalNum = dbutils.get_record_total_num(userid)
    print oneUserTotalNum
    if oneUserTotalNum == 0:
        return 0
    try:
        beginPoint = getNextRecord(userid)
    except ValueError, Error:
        return ;
    currentPoint = beginPoint
    nextPoint = beginPoint
    errorPointPre = None
    while i< oneUserTotalNum:
    #while i< 50:
        currentPoint = nextPoint
        try:
            nextPoint = getNextRecord(userid)
        except ValueError, Error:
            print Error
            break;
        try:
            speedVal = getSpeed(currentPoint, nextPoint)
        except ZeroDivisionError, Error:
            print Error
            ''' set this point as a error point '''
            speedVal = 130
        ''' If speed > 120km/h ,the mark the point as error '''
        if abs(speedVal) > 120:
            if errorPointPre:
                if errorPointPre.gps_UTC_unix_timestamp == \
                        currentPoint.gps_UTC_unix_timestamp:
                    storeErrorPoint(currentPoint);
                    errorPointPre = None
                    errorCount += 1
            else:
                errorPointPre = nextPoint

        i += 1
        #print "speed = %f km/h" % speedVal
    #nextPoint.show()
    return errorCount

def main():
    log_init()
    print "Welcome filter_points"
    #errorCount = filterUserRecords(0)
    #print "There is %d error records" %errorCount
    userlist = dbutils.get_total_users_list()
    for row in userlist:
        print row[0]
        errorCount = filterUserRecords(int(row[0]))
        print "There is %d error records" %errorCount
def testOneUser(userid = 1):
    errorCount = filterUserRecords(userid)
    print "There is %d error records in user %d" %(errorCount,userid)

  
def test():
    log_init()
    print "Welcome filter_points test"
    i =0
    errorCount = 0
    beginPoint = getNextRecord(0)
    beginPoint.show()
    beginPoint.save("test.txt")
    currentPoint = beginPoint
    nextPoint = beginPoint
    oneUserTotalNum = dbutils.get_record_total_num(0)
    #dbutils.get_gps_record_time_order(0 , 0, oneUserTotalNum+1)
    tmp = dbutils.get_gps_record_time_order(0 , oneUserTotalNum+2, 7)
    if tmp :
        print "error"
    else :
        print "empty"

#test()
#main()
testOneUser(128)
