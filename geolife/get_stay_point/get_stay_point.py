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
from base import get_distance
import logging.config
import math

logger = None

column_name = ("gps_userid", "gps_latitude", "gps_longitude", "gps_code",\
       "gps_altitude", "gps_UTC_timestamp", "gps_UTC_unix_timestamp")

def log_init():
    global logger
    if(logger == None):
        logging.config.fileConfig("../logger.conf")
        logger = logging.getLogger("root")
    return logger



def main():
    print "Welcome"
    gps_obj_list = dbutils.get_gps_record_time_order(0,0,20)
    counts = len(gps_obj_list)
    i =0
    while i < counts :
        j = i + 1
        gps_record =gps_obj_list[i]
        while (j < counts) :
            euclidean_distence = get_distance.get_distance(gps_obj_list[i], gps_obj_list[j])
            print "distence = %f km" % euclidean_distence
            if euclidean_distence > max_distence :
                t_diff = gps_obj_list[j].gps_UTC_unix_timestamp - gps_obj_list[i].gps_UTC_unix_timestamp
                if t_diff > max_timethreh:
                    stay
            j = j+1
        break;
    #for gps_record in gps_obj_list :
     #   gps_record.show()
    #print "\n"

log_init()
main()


