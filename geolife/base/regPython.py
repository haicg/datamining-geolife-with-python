# -*- coding: utf-8 -*-
"""
Created on Sun Dec 14 13:56:05 2014

@author: hyde
"""

import sys
from _winreg import *

# tweak as necessary 
version = sys.version[:3] 
installpath = sys.prefix  
regpath = "SOFTWARE\\Python\\Pythoncore\\%s\\" % (version)
installkey = "InstallPath"
pythonkey = "PythonPath"
pythonpath = "%s;%s\\Lib\\;%s\\DLLs\\" % (
installpath, installpath, installpath
)

def RegisterPy():
    print "begin RegisterPy "
    try:
        print "open key : %s"%regpath
        reg = OpenKey(HKEY_CURRENT_USER, regpath)
    except EnvironmentError as e:    
        try:           
            reg = CreateKey(HKEY_CURRENT_USER, regpath) 
            SetValue(reg, installkey, REG_SZ, installpath) 
            SetValue(reg, pythonkey, REG_SZ, pythonpath)
            CloseKey(reg) 
        except: 
            print "*** EXCEPT: Unable to register!" 
            return             
        
        print "--- Python", version, "is now registered!" 
        return

   
    if (QueryValue(reg, installkey) == installpath and 
        QueryValue(reg, pythonkey) == pythonpath): 
            CloseKey(reg) 
            print "=== Python", version, "is already registered!" 
            return CloseKey(reg) 

    print "*** ERROR:Unable to register!" 
    print "*** REASON:You probably have another Python installation!"

def UnRegisterPy():
    #print "begin UnRegisterPy "
    try:
        print "open HKEY_CURRENT_USER key=%s"%(regpath)
        reg = OpenKey(HKEY_CURRENT_USER, regpath)
        #reg = OpenKey(HKEY_LOCAL_MACHINE, regpath)
    except EnvironmentError:  
        print "*** Python not registered?!"
        return
    try:
       DeleteKey(reg, installkey)
       DeleteKey(reg, pythonkey)
       DeleteKey(HKEY_LOCAL_MACHINE, regpath)
    except:
       print "*** Unable to un-register!"
    else:
       print "--- Python", version, "is no longer registered!"            

if __name__ == "__main__":  
    RegisterPy()