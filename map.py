# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import csv
import cv2
import matplotlib.pyplot as plt

#%%
a = np.genfromtxt('Jogo4 - Atualizado.csv', delimiter=',')
data = np.array(a[1:,:], np.float64)
coordanates = data[:, 6:8]
ones = np.ones((coordanates.shape[0], 1), np.float64)
coordanates = np.hstack((coordanates, ones))
H = np.array([[-6.43920837e-01, -2.78170456e+00, 1.23878568e+03], [-2.84408766e-01, -2.32038397e+00,  9.15457942e+02], [-4.50046975e-04, -2.69442500e-03,  1.00000000e+00]], np.float64)
homogeneus_coordanates = (np.dot(H, coordanates.T)).T
field_coordenates = homogeneus_coordanates / homogeneus_coordanates[:, 2:3] 
field_coordenates[:,2] = data[:, 8]
#%%
index = int(data[0,0])
last = int(data[-1,0])
w = field_coordenates[data[:, 0].ravel() == index, 0:2]

img = cv2.imread("/home/jonh/Downloads/videoPlayer-main (1)/videoPlayer-main/resources/campo.png")

b = np.where(w[:,0] < img.shape[0])
a = field_coordenates[b]
#%%
videoName = 'Jogo4.mp4'
outputName = videoName.split('/')
videoToProcess = cv2.VideoCapture(videoName)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
filename = outputName[-1][0:-4] + "_map.avi"
out = cv2.VideoWriter(filename, fourcc, 15,(img.shape[1], img.shape[0]))
#%%
for i in range(index, last+1):
    img2 = img.copy()
    w = field_coordenates[data[:, 0].ravel() == i, 0:2]
    b = np.where(w[:, 1] < img.shape[0])
    a = field_coordenates[b]
    cv2.putText(img2, 'Frame:' + str(i),(50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)
    for l in a:
        cv2.putText(img2, str(int(l[2])),(int(l[0]), int(l[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)
        #plt.imshow(img2)
    out.write(img2)
    print(i)
out.release()
#%%
H1 = np.array([[-4.49895260e-01, -1.89210360e+00,  1.25720572e+03],[-1.93363301e-01, -1.63438028e+00,  9.59749538e+02],[-3.09733473e-04, -1.83271704e-03,  1.00000000e+00]], np.float32)
coor = np.array( [[1857., 754.,1],[1760., 379.,1],[ 244., 712.,1],[1050., 463.,1],[1809.359362,    569.82227579,1],[1765.5389551,   400.41348623,1],[1201.01350985,  596.30125405,1],[1448.59164555,  435.20658586,1],[1789.76455086,  494.06913991,1],[1772.0417156,   425.55302423,1],[1604.77261867,  507.55051388,1],[1637.96459118,  438.93432399,1]], np.float32)
sd = np.dot(H1, coor.T).T
print(sd/sd[:, 2:3])

new = np.dot(H1, coordanates[data[:, 0].ravel() == index,:].T).T
n = new/new[:,2:3]
print(n)
