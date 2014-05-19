import MySQLdb
import gps_record
import logging


def connect_db():
    try:
        db = MySQLdb.connect(host="localhost" ,user="geolife",passwd="geolife",db="geolife")
        return db
    except MySQLdb.Error,e:
        #logging.config.fileConfig("logger.conf")
        logger = logging.getLogger("root")
        #print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        logger.warning(e.args[0])
        logger.warning(" Mysql Error" +  e.args[1]) 

def close_db(conn):
    cursor = conn.cursor()
    conn.close()

def insert_into_db(conn, sql):
    try:
        cursor = conn.cursor()
        n = cursor.execute(sql) 
        print n
    except MySQLdb.Error,e:
        #logging.config.fileConfig("logger.conf")
#    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        #logger = logging.getLogger("root")
        #logger.warning(" Mysql Error sql =" + sql)
        logging.warning(e.args[0])
        #logger.warning(" Mysql Error" +  e.args[1]) 
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



