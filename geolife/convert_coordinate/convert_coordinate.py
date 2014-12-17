# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 13:59:43 2014

@author: Administrator
"""
'''
       self.gps_latitude = 0.0
        self.gps_longitude = 0.0
        self.gps_code = 0
        self.gps_altitude = 0.0
        '''
import urllib
import urllib2
import sys
sys.path.append("..")
from sql_base import dbutils
from base import base_op
from base import stay_point
from base import gps_record
import logging.config
import csv
import json
import time
logger = None

def chunks(s,step):
    lenS=len(s)
    return [s[i:min(i+step,lenS)] for i in range(0,lenS,step)]
    
def convert_coordinate_batch(orinList):
    resPointList = []
    if len(orinList) > 100*1000:
        print "Over the maximum length "
        return 
    
    for p in chunks (orinList, 100):
        resPointList += convert_coordinate_post(p)
    return resPointList
    
def convert_coordinate_batch_array(arrayList):
    resPointList = []
    if len(arrayList) > 100*1000:
        print "Over the maximum length "
        return 
    
    for p in chunks (arrayList, 100):
        resPointList += convert_coordinate_post_array(p)
    return resPointList
    
def convert_coordinate_post_array(origArray):
    coordstr = ""
    resList = []
    for p in origArray:
        coordstr += "%f,%f;" %(p[0],p[1])
        
    ak = "88E1cff5f2d3a260ac4b3864d8a9adde"
    fromVal= "1" 
    toVal = "5"
    coords = "%s" %coordstr[0:-1]
    url = "http://api.map.baidu.com/geoconv/v1/"
 
    parm = {'ak':ak, 'from':fromVal,   'to':toVal,  'coords':coords }
    parm = urllib.urlencode(parm) 
    req = urllib2.Request(url, parm) 
    data = None
    #print url
    try:
        while  (not data):
            response = urllib2.urlopen(req)    
            data = response.read()
            data = json.loads(data)
            if (not data):
                print "sleep 1s"
                time.sleep(1)
            
        #print type(data)
        plist= data["result"]
    except :
        print "Error happen\n"
        return resList

    #print len(plist)
    for p in plist:
        point = gps_record.gps_record()
        
        point.gps_longitude = p["x"]
        point.gps_latitude  = p["y"]
        resList.append(point)
    return resList

def convert_coordinate_post(orig):
    coordstr = ""
    resList = []
    for p in orig:
        coordstr += "%f,%f;" %(p.gps_longitude,p.gps_latitude)

    ak = "88E1cff5f2d3a260ac4b3864d8a9adde"
    fromVal= "1" 
    toVal = "5"
    coords = "%s" %coordstr[0:-1]
    url = "http://api.map.baidu.com/geoconv/v1/"
 
    parm = {'ak':ak, 'from':fromVal,   'to':toVal,  'coords':coords }
    parm = urllib.urlencode(parm) 
    req = urllib2.Request(url, parm) 
    data = None
    #print url
    try:
        while  (not data):
            response = urllib2.urlopen(req)    
            data = response.read()
            data = json.loads(data)
            if (not data):
                print "sleep 1s"
                time.sleep(1)
            
        #print type(data)
        plist= data["result"]
    except :
        print "Error happen\n"
        return resList

    #print len(plist)
    for p in plist:
        point = gps_record.gps_record()
        
        point.gps_longitude = p["x"]
        point.gps_latitude  = p["y"]
        resList.append(point)
    return resList


def convert_coordinate_get(orig):
    coordstr = ""
    resList = []
    for p in orig:
        coordstr += "%f,%f;" %(p.gps_longitude,p.gps_latitude)
    coords = "coords=%s" %coordstr[0:-1]
    ak = "ak=88E1cff5f2d3a260ac4b3864d8a9adde"
    fromVal= "from=1" 
    toVal = "to=5"
    url = "http://api.map.baidu.com/geoconv/v1/?"+ ak \
    + "&"+ fromVal + "&" + toVal + "&" + coords
    ak = "88E1cff5f2d3a260ac4b3864d8a9adde"
 
    data = None

    #print url
    try:
        while  (not data):
            
            data = urllib2.urlopen(url)
            data = data.read()
            data = json.loads(data)
            if (not data):
                print "sleep 1s"
                time.sleep(1)
            
        #print type(data)
        plist= data["result"]
    except :
        print "Error happen\n"
        return None


    for p in plist:
        point = gps_record.gps_record()
        #print p["x"]
        point.gps_longitude = p["x"]
        point.gps_latitude  = p["y"]
        resList.append(point)
    return resList
    
    
    
def test():
    
    coords = []
    point = gps_record.gps_record()
    point.gps_longitude = 116.326624
    point.gps_latitude  = 39.977897
    coords.append(point)
    point = gps_record.gps_record()
    point.gps_longitude = 116.326626
    point.gps_latitude  = 39.977882
    coords.append(point)
    res = convert_coordinate_post(coords)
    print len(res)
#test()
