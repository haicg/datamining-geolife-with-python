# -*- coding: utf-8 -*
###File Name:get_stay_point.py
###Author:haicg
###Mail:lihaicg@126.com
###Created Time: 2014/6/6 15:37:58
###File Name : get_stay_point.py
#!/usr/bin/python
import sys
sys.path.append("..")
from sql_base import dbutils
from base import gps_record
import logging.config

logger = None
def log_init():
    global logger
    if(logger == None):
        logging.config.fileConfig("../logger.conf")
        logger = logging.getLogger("root")
    return logger

column_name = ("gps_userid", "gps_latitude", "gps_longitude", "gps_code",\
       "gps_altitude", "gps_UTC_timestamp", "gps_UTC_unix_timestamp")

def get_distance(begin_point, end_point):
    '''这个函数还是有问题的，计算的公式是错误的 '''
    diff_latitude = float(begin_point.gps_latitude) - float(end_point.gps_latitude)
    diff_longitude = float(begin_point.gps_longitude) - float(end_point.gps_longitude)
    diff_altitude = float(begin_point.gps_altitude) - float(end_point.gps_altitude)

    begin_point.show()
    end_point.show()

    euclidean_distence = diff_latitude*diff_latitude + diff_longitude*diff_longitude + diff_altitude*diff_altitude  
    return euclidean_distence



def main():
    print "Welcome"
    gps_obj_list = dbutils.get_gps_record(0,0,20)
    counts = len(gps_obj_list)
    i =0
    while i < counts :
        j = i + 1
        gps_record =gps_obj_list[i]
        while (j < counts) :
            euclidean_distence = get_distance(gps_obj_list[i], gps_obj_list[j])
            print euclidean_distence
            j = j+1
        break;
    #for gps_record in gps_obj_list :
     #   gps_record.show()
    #print "\n"



log_init()
main()


