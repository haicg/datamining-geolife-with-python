import sys
sys.path.append("..")
from base import gps_record

import MySQLdb
import os
import logging

logger = None


column_name = ("gps_userid", "gps_latitude", "gps_longitude", "gps_code",\
       "gps_altitude", "gps_UTC_timestamp", "gps_UTC_unix_timestamp","id")
table_name = "geolife"
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
        print warnString

        if(e.args[0] == 1045 or e.args[0] == 1044):
            os._exit(1)

def query_sql(query_str):
    global dbconn
    results = None
    if (dbconn == None ):
        dbconn = connect_db()
    if (dbconn) :
        try:
            cur = dbconn.cursor();
            count = cur.execute(query_str)
            results = cur.fetchall()
        except MySQLdb.Error,e:
            warnString = " Mysql Error sql = %d %s " % (e.args[0],e.args[1])
            log_init().warning(warnString)
            sys.exit(1)
    return results


def close_db(conn=None):
    global dbconn
    if (conn == None) :
        conn = dbconn
    if (conn == None) :
        return
    cursor = conn.cursor()
    if(cursor):
        cursor.close()
    conn.close()

def insert_into_db(sql,conn=None):
    global dbconn
    if (conn == None) :
        if (dbconn == None ):
            conn = connect_db()
        else:
            conn = dbconn
            
    if (conn) :
        try:
            cursor = conn.cursor()
            n = cursor.execute(sql)
            conn.commit();
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
    else :
        return 0

def insert_gps_record(conn, oneRecord):
    sql = "INSERT INTO geolife(gps_userid, gps_latitude, gps_longitude, gps_code, gps_altitude, gps_UTC_timestamp, gps_UTC_unix_timestamp) \
VALUES ('%d', '%f', '%f', '%d', '%f', '%s', '%s')" % \
        (oneRecord.gps_userid,oneRecord.gps_latitude,oneRecord.gps_longitude,oneRecord.gps_code,
                oneRecord.gps_altitude, oneRecord.gps_UTC_timestamp, oneRecord.gps_UTC_unix_timestamp)
        #  print sql
    return insert_into_db(sql,conn)
    
def insert_staypoint(s_point,conn=None):
    sql = "INSERT INTO staypoint(userid, arrival_timestamp, leaving_timestamp, mean_coordinate_latitude,\
mean_coordinate_longtitude, mean_coordinate_altitude, arrival_point, leaving_point )VALUES ('%d', '%d', '%d', '%f', '%f', '%f','%d','%d')" % \
        (s_point.userid, s_point.arrival_timestamp, s_point.leaving_timestamp, \
        s_point.mean_coordinate_latitude, s_point.mean_coordinate_longtitude, \
        s_point.mean_coordinate_altitude, s_point.arrival_point, s_point.leaving_point)

    return insert_into_db(sql,conn)


def query_gps( query_str):
    global dbconn
    gps_obj_list = []
    if (dbconn == None ):
        dbconn = connect_db()
    if (dbconn) :
        try:
            cur = dbconn.cursor();
            count = cur.execute(query_str)
            #print 'There is %s rows record' %count
            #result = cur.fetchone()
            #results = cur.fetchall()

            results = cur.fetchall()
            for row in results:
                gps_obj = gps_record.gps_record.__init_with_query_sql__(gps_record.gps_record(), row)
                gps_obj_list.append(gps_obj);
            return gps_obj_list
        except MySQLdb.Error,e:
            warnString = " Mysql Error sql = %d %s " % (e.args[0],e.args[1])
            log_init().warning(warnString)
            sys.exit(1)

        #print results
        #conn.commit()
        #cur.close()
        #dbconn.close()

'''
userid : user id
m: the first index
n: the number of elements
'''
def get_gps_record_time_order(userid, m, n):
    displist = ""

    for oneDisp in  column_name:
        displist = displist + oneDisp + ","
    displist = displist.strip(',')
    if(n > 0):
        sqlStr = 'select %s from geolife where gps_userId =%d order by gps_UTC_unix_timestamp limit %d,%d' %( displist, userid, m, n)
    else:
        sqlStr = 'select %s from geolife where gps_userId =%d order by gps_UTC_unix_timestamp ' %(displist, userid)
    #print sqlStr
    #log_init().debug(sqlStr)
    return query_gps(sqlStr)

def get_record_total_num(userid) :
    global dbconn
    query_str = 'select count(id) from %s where %s = %d' %(table_name, column_name[0], userid)
    #print query_str
    if (dbconn == None ):
        dbconn = connect_db()
    if (dbconn) :
        try:
            cur = dbconn.cursor();
            count = cur.execute(query_str)
            #print 'There is %s rows record' %count
            result = cur.fetchone()
            #print result
            #results = cur.fetchall()
        except MySQLdb.Error,e:
            warnString = " Mysql Error sql = %d %s " % (e.args[0],e.args[1])
            log_init().warning(warnString)
            sys.exit(1)
    return result[0]
def test():
    displist = ""
    for oneDisp in  column_name:
        displist = displist + oneDisp + ","
    displist = displist.strip(',')
    sqlStr = 'select %s from geolife where gps_userId =0 limit 10' %displist
    print sqlStr
    query_gps(sqlStr)

def get_total_users_list() :
    sqlStr = "select distinct gps_userid from %s" %table_name
    return query_sql(sqlStr)
#test()

