import sys
sys.path.append("..")
from sql_base import dbutils
import errno
import os
import deal_one_file
import file_op
import logging
import logging.config

LOG_HANDLE = None
logger = None
def log_init():
    global logger
    if(logger == None):
        logging.config.fileConfig("../logger.conf")
        logger = logging.getLogger("root")
    return logger

def storeFilePathList(name, listContext):
    #fp = file_op.open_file_write("filepathList.txt")
    file_op.store_list("filepathList.txt", name, listContext);

def main():
    log_init();
    DataPath = "./Data/"
#    getFilePathListL1();
    FilePathListL1Str = None
    FilePathListL1 = None
    try :
        FilePathListL1Str = file_op.get_store_list("filepathList.txt", "FilePathListL1")
        if (FilePathListL1Str):
            FilePathListL1 = FilePathListL1Str.rstrip().split(",");
        else:
            return
    except IOError:
        if not (FilePathListL1Str):
            FilePathListL1 = os.listdir(DataPath) #000 001
            storeFilePathList("FilePathListL1", FilePathListL1)
    FilePathL1 = None
    #for FilePathL1 in FilePathListL1:
    for i in range (len(FilePathListL1)):
        FilePathL1 = FilePathListL1.pop()
        FilePathFullL1 = DataPath+FilePathL1 #000 001
        if os.path.isdir(FilePathFullL1) :    
            userId = FilePathL1
            try:
                int(userId, 10)
            except ValueError:
                logger.warning("dir error " + FilePathFullL1 )
                storeFilePathList("FilePathListL1", FilePathListL1)
                continue
            FilePathListL2 = os.listdir(FilePathFullL1) #Trajectory
            for FilePathL2 in FilePathListL2:
                FilePathFullL2 = FilePathFullL1 + '/' +FilePathL2 #Trajector
                try:
                    FilePathFullL2.index('Trajectory')
                except ValueError:
                    logger.warning("dir error " + FilePathFullL2 )
                    continue
                print FilePathFullL2
                if os.path.isdir(FilePathFullL2) :    
                    FilePathListL3 = os.listdir(FilePathFullL2) #20090428051631.plt
                    FilePathListL3.sort()
                    for FilePathL3 in FilePathListL3:
                        extension = os.path.splitext(FilePathL3) 
                        if extension[1] != '.plt' :
                            logger.warning("dir error " + FilePathL3 )
                            continue;
                        FilePathFullL3 = FilePathFullL2 + "/" + FilePathL3 #20090428051631.plt
                        if os.path.isfile(FilePathFullL3) :
                            deal_one_file.setOneFileRecord(FilePathFullL3, userId)
                        
            #FilePathListL1.remove(FilePathL1)
            logger.warning(FilePathListL1);
            storeFilePathList("FilePathListL1", FilePathListL1)
            print "ok"

main()
deal_one_file.close_conn();
print "Store the GPS data Successfully"
