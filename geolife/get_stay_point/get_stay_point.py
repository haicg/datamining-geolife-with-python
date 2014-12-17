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
from base import base_op
from base import file_op
from base import stay_point
import logging.config
import csv
import pickle
import os
import json
from convert_coordinate import convert_coordinate

logger = None

column_name = ("gps_userid", "gps_latitude", "gps_longitude", "gps_code",\
       "gps_altitude", "gps_UTC_timestamp", "gps_UTC_unix_timestamp")

def log_init():
    global logger
    if(logger == None):
        logging.config.fileConfig("logger.conf")
        logger = logging.getLogger("root")
    return logger

def calc_mean_pos(s_point,tmp_points):
    i = 0;
    latitude_sum = 0
    longitude_sum = 0
    altitude_sum = 0
    
    for p in tmp_points:
        latitude_sum = p.gps_latitude + latitude_sum
        longitude_sum = p.gps_longitude + longitude_sum
        altitude_sum = p.gps_altitude + altitude_sum
        i = i + 1
    s_point.mean_coordinate_latitude = latitude_sum/i
    s_point.mean_coordinate_longtitude = longitude_sum/i
    s_point.mean_coordinate_altitude = altitude_sum/i
    s_point.arrival_timestamp = tmp_points[0].gps_UTC_unix_timestamp
    s_point.leaving_timestamp = tmp_points[i-1].gps_UTC_unix_timestamp
    s_point.arrival_point = tmp_points[0].id
    s_point.leaving_point = tmp_points[i-1].id
    return s_point

def get_stay_points(userid = 1,max_distence = 0.2, max_speed = 2):
    print "Welcome"
     #units :km
    #userid = 0
    gps_obj_list = dbutils.get_gps_record_time_order(userid, 0,-1)
    stay_point_list = []
    counts = len(gps_obj_list)
    tmp_point_list = []
    i =0
    while i < counts :
        j = i + 1
        point_i =gps_obj_list[i]
        k = 0
        
        #del tmp_point_list[:]
        tmp_point_list = []
        tmp_point_list.insert(0, point_i)
        while (j < counts) :
            point_j = gps_obj_list[j]
            euclidean_distence = base_op.get_distance(point_i, point_j)
            #print "distence = %f km" % euclidean_distence
            k = k + 1
            tmp_point_list.insert(k, point_j)
            if euclidean_distence > max_distence :
                t_diff = point_j.gps_UTC_unix_timestamp - point_i.gps_UTC_unix_timestamp
                meanSpeed =  euclidean_distence / t_diff  * 1000      
                #print "speed = %f m/s" % meanSpeed
                #if t_diff > max_timethreshold:
                if meanSpeed < max_speed:
                    print "distence = %f km" % euclidean_distence
                    print "speed = %f m/s" % meanSpeed
                    print "time = %f s" % t_diff
                    
                    tmp_point_list.pop();
                    s = stay_point.stay_point()
                    s.userid = userid
                    calc_mean_pos(s, tmp_point_list)
                    stay_point_list.append(s)
                    #dbutils.insert_staypoint(s)
                    i = j
                    break
                else:
                    i = j
                    break;
            j = j+1
        if j == counts :
            s = stay_point.stay_point()
            s.userid = userid
            calc_mean_pos(s, tmp_point_list)
            stay_point_list.append(s)
            dbutils.insert_staypoint(s)
            i = j
    #    break;
    #for gps_record in gps_obj_list :
     #   gps_record.show()
    #print "\n"
    return stay_point_list
    
    
def get_stay_points_v2(userid = 1,max_distence = 0.2, max_speed = 2, max_time=15*60):
    print "Welcome"
     #units :km
    #userid = 0
    gps_obj_list = dbutils.get_gps_record_time_order(userid, 0,-1)
    stay_point_list = []
    counts = len(gps_obj_list)
    tmp_point_list = []
    i =0
    while i < counts :
        j = i + 1
        point_i =gps_obj_list[i]
        k = 0
        
        #del tmp_point_list[:]
        tmp_point_list = []
        tmp_point_list.insert(0, point_i)
        while (j < counts) :
            point_j = gps_obj_list[j]
            euclidean_distence = base_op.get_distance(point_i, point_j)
            t_diff = point_j.gps_UTC_unix_timestamp - point_i.gps_UTC_unix_timestamp
            #print "distence = %f km" % euclidean_distence
            k = k + 1
            tmp_point_list.insert(k, point_j)
            if t_diff > max_time :
                #t_diff = point_j.gps_UTC_unix_timestamp - point_i.gps_UTC_unix_timestamp
                meanSpeed =  euclidean_distence / t_diff  * 1000      
                #print "speed = %f m/s" % meanSpeed
                #if t_diff > max_timethreshold:
                if meanSpeed < max_speed:
                    #print "distence = %f km" % euclidean_distence
                    #print "speed = %f m/s" % meanSpeed
                    #print "time = %f s" % t_diff
                    
                    tmp_point_list.pop();
                    s = stay_point.stay_point()
                    s.userid = userid
                    calc_mean_pos(s, tmp_point_list)
                    stay_point_list.append(s)
                    #dbutils.insert_staypoint(s)
                    i = j
                    break
                else:
                    i = j
                    break;
            j = j+1
        if j == counts :
            s = stay_point.stay_point()
            s.userid = userid
            calc_mean_pos(s, tmp_point_list)
            stay_point_list.append(s)
            #dbutils.insert_staypoint(s)
            i = j
    #    break;
    #for gps_record in gps_obj_list :
     #   gps_record.show()
    #print "\n"
    return stay_point_list

def getStayPointsList(stayPointListFile,userid):
    if os.path.isfile(stayPointListFile) :#如果不存在就返回False 
        print "read from local file "
        mydb  = open(stayPointListFile, 'r')  
        stay_points_list = pickle.load(mydb)
    else:
        print "read from mysql"
        stay_points_list = get_stay_points_v2(userid)    
        mydb = open(stayPointListFile, 'w')  
        pickle.dump(stay_points_list, mydb) 
    return stay_points_list

    
def convert_staypoint_baidu_corrd(stay_points_list):
    orinArry = []
    for s in stay_points_list:
        p = []
        p.append(s.mean_coordinate_longtitude)
        p.append(s.mean_coordinate_latitude)
        orinArry.append(p)
    return convert_coordinate.convert_coordinate_batch_array(orinArry)
    
    
def saveStayPointsToJson(distPointList, filepath='', fileId = 0 ):
    if not distPointList:
        print "Null Value"
        return
    datalist = []
    for p in distPointList:
        data = []
        data.append(p.gps_longitude);
        data.append(p.gps_latitude);
        data.append(1);
        datalist.append(data);
    strTmp = "var data%d =" %fileId
    saveDate = {'data':datalist,'total':len(datalist),"rt_loc_cnt":47764510,"errorno":0,"NearestTime":"2014-08-29 15:20:00","userTime":"2014-08-29 15:32:11"}
    strTmp += json.dumps(saveDate,sort_keys=False)
    with open(filepath, "w") as fp:
        fp.write(strTmp)
    fp.close()
def saveStayPointsBaiduCoordToJson(stay_points_list,dirName,userid):
    stay_points_list_baidu = []
    stay_points_list_baidu = convert_staypoint_baidu_corrd(stay_points_list)
    filetype = ""
    filepath = "%s/points_staypoints_baidu_%d%s.js" %(dirName, userid,filetype)
    saveStayPointsToJson(stay_points_list_baidu, filepath)
    
def saveStayPointsToCsv(csv_name, stay_points_list):
    with open(csv_name,"wb") as csvfp:
        writer = csv.writer(csvfp)
        for p in stay_points_list:
             writer.writerow([p.mean_coordinate_latitude]+[p.mean_coordinate_longtitude]);
        print len(stay_points_list)
    csvfp.close()
def printStayPoints(stay_points_list,n):
    for i in range(n):
        stay_points_list[i].printSelf()
        
def sampleImportantSpot(sTime, eTime, minDis, importantSpot,stay_points_list):
    sampleRes = []   
    disThreh = 200 #unit is mile
    n = len(stay_points_list)
    i = 0
    imLat = importantSpot.mean_coordinate_latitude
    imLon = importantSpot.mean_coordinate_longtitude
    
    while (i < n):
        entTime = stay_points_list[i].arrival_timestamp
        leaTime =stay_points_list[i].leaving_timestamp
        lat = stay_points_list[i].mean_coordinate_latitude
        lon = stay_points_list[i].mean_coordinate_longtitude
        #unit is mile
        dis = base_op.calc_distance(imLat,imLon,lat,lon)
        if (dis < disThreh):
            j = 0
            while(sTime < entTime):
                sTime += 60*10
                j = j + 1;
                if (j== 6) :
                    sampleRes.append(0)
                    j = 0
            while(sTime < leaTime):
                sTime += 60*10*6
                sampleRes.append(1)
        i += 1
    while (sTime < eTime) :
        sTime += 60*10*6
        sampleRes.append(0)
    print len(sampleRes)
    return sampleRes
    #print sampleRes
                
            
            
            
            
    
def main():
    userid = 128
    dirName = "stay_points_dir" 
    stayPointNumFile = dirName+"/%d_staypoints_num.txt" %userid
    stayPointListFile = dirName+"/%d_staypoints_list.txt" %userid
    csv_name = dirName+ "/staypoints_%s.csv" %userid
   
    
    if not os.path.exists(dirName):
        os.mkdir(dirName)  
    stay_points_list = getStayPointsList(stayPointListFile, userid)
    sTime = 1176483388
    eTime = 1299715222
    minDis = 200
    importantSpot = stay_points_list[0]
    #saveStayPointsToCsv(csv_name,stay_points_list)
    sampleList = sampleImportantSpot(sTime, eTime, minDis, importantSpot,stay_points_list)
    stayPointSampleListFile = dirName+"/%d_staypoints_sample_list_0.txt" %userid    
    mydb = open(stayPointSampleListFile, 'w')  
    pickle.dump(sampleList, mydb)     
    #mydb = open(stayPointNumFile, 'w')  
    #pickle.dump(len(stay_points_list), mydb) 
    #saveStayPointsBaiduCoordToJson(stay_points_list, dirName, userid)
    #printStayPoints(stay_points_list, 2)
    print "successfully!"
        
log_init()
main()


