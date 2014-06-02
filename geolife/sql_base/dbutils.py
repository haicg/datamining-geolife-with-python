import sys
sys.path.append("..")
from base import gps_record

import MySQLdb
import os
import logging

logger = None


column_name = ("gps_userid", "gps_latitude", "gps_longitude", "gps_code",\
       "gps_altitude", "gps_UTC_timestamp", "gps_UTC_unix_timestamp")

def log_init():
    global logger
    if(logger == None):
        logger = logging.getLogger("root.sql.dbutils")
    return logger

#grant all privileges on geolife.`*` to geolife@"%" identified by "geolife"
#FLUSH   PRIVILEGES

dbconn = None

def connect_db():
    try:
        db = MySQLdb.connect(host="localhost" ,user="geolife",passwd="geolife",db="geolife")
        return db
    except MySQLdb.Error,e:
        warnString= "Mysql Error %d: %s" % (e.args[0], e.args[1])
        
        log_init().warning(warnString)

        if(e.args[0] == 1045 or e.args[0] == 1044):
            os._exit(1)

def close_db(conn):
    cursor = conn.cursor()
    if(cursor):
        cursor.close()
    conn.close()

def insert_into_db(conn, sql):
    try:
        cursor = conn.cursor()
        n = cursor.execute(sql) 
        print n
    except MySQLdb.Error,e:
#WARNING  Mysql Error sql = 1062 Duplicate entry "***" for key 'unique_key' 
        if (e.args[0] == 1062):
            return 0
        warnString = " Mysql Error sql = %d %s " % (e.args[0],e.args[1])
        log_init().warning(warnString)
        if(e.args[0] == 2006):
            return 2
        else:
            return 0

def insert_gps_record(conn, oneRecord):
    sql = "INSERT INTO geolife(gps_userid, gps_latitude, gps_longitude, gps_code, gps_altitude, gps_UTC_timestamp, gps_UTC_unix_timestamp) \
VALUES ('%d', '%f', '%f', '%d', '%f', '%s', '%s')" % \
        (oneRecord.gps_userid,oneRecord.gps_latitude,oneRecord.gps_longitude,oneRecord.gps_code,
                oneRecord.gps_altitude, oneRecord.gps_UTC_timestamp, oneRecord.gps_UTC_unix_timestamp)
        #  print sql
    return insert_into_db(conn, sql)



def query_gps( query_str):
    global dbconn
    gps_obj_list = []
    if (dbconn == None ):
        dbconn = connect_db()
    if (dbconn) :
        cur = dbconn.cursor();
        count = cur.execute(query_str)
        print 'There is %s rows record' %count
        #result = cur.fetchone()
        #results = cur.fetchall()
        
        results = cur.fetchmany(10)
        for row in results:
            gps_obj = gps_record.gps_record.__init_with_query_sql__(gps_record.gps_record(), row)
            gps_obj.printClass();
            gps_obj_list.append(gps_obj); 

        #print results
        #conn.commit()
        cur.close()
        dbconn.close()

def test():
    displist = ""
    for oneDisp in  column_name:
        displist = displist + oneDisp + ","
    displist = displist.strip(',')
    sqlStr = 'select %s from geolife where gps_userId =0 limit 10' %displist
    print sqlStr
    query_gps(sqlStr)

#test()

