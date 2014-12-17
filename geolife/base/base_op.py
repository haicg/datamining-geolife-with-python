###File Name:get_distence.py
###Author:haicg
###Mail:lihaicg@126.com
###Created Time: Mon 07 Jul 2014 08:13:00 PM HKT
###File Name : get_distence.py
#!/usr/bin/python

import math

'''Return value is the distance with the unit of mile  '''
def calc_distance(lat1, lon1, lat2, lon2):
    theta = lon1 -lon2
    dist = math.sin(math.radians(lat1))*math.sin(math.radians(lat2)) \
            + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))\
            * math.cos(math.radians(theta))
    if dist - 1 > 0 :
        dist = 1
    elif dist +1 < 0 :
        dist = -1
    dist = math.acos(dist)
    dist = math.degrees(dist)
    miles = dist * 60 * 1.1515
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
