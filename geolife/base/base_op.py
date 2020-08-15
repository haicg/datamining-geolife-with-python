###File Name:get_distence.py
###Author:haicg
###Mail:lihaicg@126.com
###Created Time: Mon 07 Jul 2014 08:13:00 PM HKT
###File Name : get_distence.py
#!/usr/bin/python

import math
from geopy import distance

'''Return value is the distance with the unit of mile  '''

# 这个函数以前计算距离可能有点问题，不够精准，同时对于边界问题处理过于粗暴
# 这个修改成GeoPy的实现
def calc_distance(lat1, lon1, lat2, lon2):
    newport_ri = (lat2, lon2)
    cleveland_oh = (lat1, lon1,)
    miles = distance.distance(newport_ri, cleveland_oh).miles
    return miles;


'''Return value is the distance with the unit of mile  '''
def calc_points_distance(p1, p2):
    return calc_distance(p1.x, p1.y, p2.x, p2.y)
    

def get_distance(begin_point, end_point):
    lat1 = float(begin_point.gps_latitude)
    lat2 = float(end_point.gps_latitude)
    lon1 = float(begin_point.gps_longitude)
    lon2 = float(end_point.gps_longitude)
    #begin_point.show()
    #end_point.show()
    ''' The unit of the distance is kilometer'''
    euclidean_distence = calc_distance(lat1, lon1, lat2, lon2) * 1.609344
    return euclidean_distence
