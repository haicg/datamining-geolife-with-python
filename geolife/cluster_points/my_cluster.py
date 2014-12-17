# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 19:57:40 2014

@author: hai
"""


print(__doc__)

import numpy as np

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

# Plot result
import matplotlib.pyplot as plt

import sys
sys.path.append("..")
#from sql_base import dbutils
from base import base_op


def getPointsDistence(p1, p2):
    return base_op.calc_distance(p1[0],p1[1],p2[0],p2[1])
    
def getPointClusterDist(c, p):
    distList = []    
    for cpoint in c:
        distList.append(getPointsDistence(p, cpoint))
    return max(distList)
    
    

def updataClusterCenter(clusterP, p, num):
    p = clusterP*num + p
    return p/(num+1)

def myCluster(points):
    points = np.array(points);
    minDistence = 0.5 #km
    minCout = 15;
    labels = np.zeros(len(points), dtype=int)
    #isDeal = np.zeros(len(points), dtype=bool)
    k = 0
    clusterList = np.zeros((len(points),2),dtype=float)
    numInCluster = np.zeros(len(points))
    clusterListSore = []   
    for pointIdx in range(len(points)):
        
        i = 0
        while i < k:
            if (getPointClusterDist(clusterListSore[i], points[pointIdx]) < minDistence):
                clusterListSore[i].append(points[pointIdx])                
                clusterList[i] = updataClusterCenter(clusterList[i], points[pointIdx], numInCluster[i])
                labels [pointIdx] = i
                numInCluster[i] = numInCluster[i] + 1
                break        
            else:
                i = i + 1
        if i == k:
            
            #clusterListSore[i].append(points[pointIdx]) 
            tmpList = []
            tmpList.append(points[pointIdx])
            clusterListSore.append(tmpList)
            clusterList[i] = points[pointIdx]
            numInCluster[i] = numInCluster[i] + 1
            k = k + 1
   # clusterPoints = []
    #numInClusterRet = []
    mask = np.zeros(len(points),dtype=bool)
    pos = 0;
    for i in range(k):
        if (numInCluster[i] > minCout):
            mask [i] = True;
            labels = [pos if j == i else j for j in labels]
            pos = pos +1
        else:
            labels = [-1 if j == i else j for j in labels]
    return clusterList[mask],numInCluster[mask],labels


import csv
userid = 0
X = []
csv_name = "staypoints_%s.csv" %userid
with open(csv_name,"rb") as csvfp:
    reader = csv.reader(csvfp)
    for line in reader:
        X.append(line)
    X = np.array(X, np.float)
csvfp.close()

res = myCluster(X);
print res[0],res[1]

centerPoints = res[0]
labels = np.array(res[2])

# Black removed and is used for noise instead.
core_samples_mask = np.zeros_like(labels, dtype=bool)
#core_samples_mask = [True for i in core_samples_mask] 
core_samples_mask [:] = True
unique_labels = set(labels)
colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
fig = plt.figure(5)
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = 'k'
        continue

    class_member_mask = (labels == k)

    xy = X[class_member_mask & core_samples_mask]
    print "%d reference points contain %d points" %(k,len(xy))
    #print "%f mean pos %f" %xy.
    
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=8)
#    plt.xlim(30,42)
#    plt.ylim(116,122)
'''
    xy = X[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=6)
             '''
plt.plot(centerPoints[:, 0], centerPoints[:, 1], 'o', markerfacecolor='k',
             markeredgecolor='k', markersize=4)
plt.title('Estimated number of clusters: %d' % len(centerPoints))





