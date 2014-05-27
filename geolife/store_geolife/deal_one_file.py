import os
import errno
from base import gps_record
from sql_base import dbutils
import logging
import file_op

dbConn = None
def setOneFileRecord(filename, userid):
    global dbConn
    readAndIstOneFile(filename, userid)
    dbConn.commit()

def insertOneRecord(recordStr, userid):
    global dbConn
    i = 0
    try:
        recordObj = gps_record.gps_record(recordStr, userid)
        if(dbConn == None) :
            dbConn = dbutils.connect_db()
        #if the connectint closed by mysal server ,then open the connection again
        while(dbutils.insert_gps_record(dbConn, recordObj) == 2 and i<4):
            dbConn = dbutils.connect_db()
            i = i+ 1
    except ValueError:
        print "Error"
        logging.config.fileConfig("logger.conf")
        logger = logging.getLogger("root")
        logger.warning("GPS Record Value Error " + userid + recordStr)

def readAndIstOneFile(filename, userid):
    fp = file_op.open_file(filename)
    logging.config.fileConfig("logger.conf")
    logger = logging.getLogger("root")
    logger.warning("GPS File name " + filename)
    for i in range(0,6):
        fp.readline()
    while True:
        line = fp.readline()
        if(line == ""):
            break
        print line
        insertOneRecord(line, userid)
    file_op.close_file(fp)

def close_conn():
    global  dbConn
    if(dbConn):
        dbutils.close_db(dbConn)
