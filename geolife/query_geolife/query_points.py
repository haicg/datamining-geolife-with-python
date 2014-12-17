# -*- coding: utf-8 -*-
"""
Created on Sun Dec 14 13:31:31 2014

@author: hyde
"""

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
from convert_coordinate import convert_coordinate
from base import base_op
from base import stay_point
import logging.config
import csv
import json
import os
import pickle
logger = None

column_name = ("gps_userid", "gps_latitude", "gps_longitude", "gps_code",\
       "gps_altitude", "gps_UTC_timestamp", "gps_UTC_unix_timestamp")

def log_init():
    global logger
    if(logger == None):
        logging.config.fileConfig("../logger.conf")
        logger = logging.getLogger("root")
    return logger
    
def chunks(s,step):
    lenS=len(s)
    return [s[i:min(i+step,lenS)] for i in range(0,lenS,step)]
    
def storeVar():
    varFileNamePre = "var_data/%d_var_points" %userid
    varFileName = varFileNamePre + '_0.txt'
    if os.path.isfile(varFileName) :#如果不存在就返回False 
        print "read from local file "
        mydb  = open(varFileName, 'r')  
        gps_obj_list = pickle.load(mydb)
    else:
        print "read from mysql"
        i = 0
        
        for gpsTmplist in chunks(gps_obj_list,4000):
            varFileName = varFileNamePre + "_%s.txt" %(i)      
            mydb = open(varFileName, 'w')  
            pickle.dump(gps_obj_list, mydb)  
            i += 1
        mydb = open("FileNum.txt", 'w')  
        pickle.dump(i, mydb)  
       
def savePointsToJson(userid, fileId, distPointList):
    datalist = []
    for p in distPointList:
        data = []
        data.append(p.gps_longitude);
        data.append(p.gps_latitude);
        data.append(1);
        datalist.append(data);
    fileGpoints = "%d_points_dir/points_gps_%d.js" %(userid,fileId)
    strTmp = "var data%d =" %fileId
    saveDate = {'data':datalist,'total':len(datalist),"rt_loc_cnt":47764510,"errorno":0,"NearestTime":"2014-08-29 15:20:00","userTime":"2014-08-29 15:32:11"}
    strTmp += json.dumps(saveDate,sort_keys=False)
    with open(fileGpoints,"w") as fp:
        fp.write(strTmp)
    fp.close()
    
def main():
    userid = 128
    
    gps_obj_list = dbutils.get_gps_record_time_order(userid, 0,-1)
    dbutils.close_db();
    print "next"
    dirName = "%d_points_dir_baidu_pos" %userid
    if not os.path.exists(dirName):
        os.mkdir(dirName)
    
    distPointList = []
    i = 0
    j = 0
    for p in chunks (gps_obj_list,100):
        i = i + 1
        distPointList += convert_coordinate.convert_coordinate_post(p)
        if i >=1000:
            savePointsToJson(userid, j, distPointList)
            distPointList = []
            j = j + 1
            i = 0
    savePointsToJson(userid, j, distPointList)
main()
    
    
    