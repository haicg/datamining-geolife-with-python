# -*- coding: utf-8 -*-
"""
Created on Sat Oct 11 09:55:07 2014

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

# Plot the ground truth
fig = plt.figure(1)
col = 'k'
#plt.xlim(30,100)
#plt.ylim(100,200)
plt.plot(X[:, 0], X[:, 1], '*', markerfacecolor='k',
         markeredgecolor='k', markersize=5)

# Compute DBSCAN
db = DBSCAN(eps=0.15, min_samples=4).fit(X)
#db = DBSCAN(eps=0.5, min_samples=10).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
##############################################################################
# Plot result


# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
fig = plt.figure(2)
centerPoint = []
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = 'k'
#        continue

    class_member_mask = (labels == k)

    xy = X[class_member_mask & core_samples_mask]
    
    #centerPoint.append()

    print "%d reference points contain %d points" %(k,len(xy))
    #print "%f mean pos %f" %xy.
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=14)
    print "center pos %f %f" %(np.mean(xy[:, 0]), np.mean(xy[:, 1]) ) 
'''
    xy = X[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=6)
             '''

plt.title('DBSCAN :Estimated number of clusters: %d' % n_clusters_)



# Plot the ground truth
#fig = plt.figure(2, figsize=(4, 3))

plt.show()
print "successful"

   

