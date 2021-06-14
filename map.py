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
H = np.genfromtxt('/home/jonh/Downloads/videoPlayer/Jogo4_homography.csv', delimiter=',')
homogeneus_coordanates = (np.dot(H, coordanates.T)).T
field_coordenates = homogeneus_coordanates / homogeneus_coordanates[:, 2:3] 
field_coordenates[:,2] = data[:, 8]
#%%
index = int(data[0,0])
last = int(data[-1,0])
img = cv2.imread("/home/jonh/Downloads/videoPlayer/resources/campo.png")
#%%
videoName = '/home/jonh/Downloads/Rastreio John/Jogo4.mp4'
outputName = videoName.split('/')
videoToProcess = cv2.VideoCapture(videoName)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
filename = outputName[-1][0:-4] + "_map.avi"
#out = cv2.VideoWriter(filename, fourcc, videoToProcess.get(cv2.CAP_PROP_FPS),(img.shape[1], img.shape[0]))
out = cv2.VideoWriter(filename, fourcc, 15,(img.shape[1], img.shape[0]))
#%%
for i in range(index, last+1):
    img2 = img.copy()
    w = field_coordenates[data[:, 0].ravel() == i, 0:3]
    cv2.putText(img2, 'Frame:' + str(i),(50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)
    for l in w:
        cv2.putText(img2, str(int(l[2])),(int(l[0]), int(l[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)
        #plt.imshow(img2)
    out.write(img2)
    #print(i)
out.release()
#%%
videoToProcess = cv2.VideoCapture(videoName)
ret, frame = videoToProcess.read()
ret, frame = videoToProcess.read()
filename = outputName[-1][0:-4] + "_map30.avi"
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out2 = cv2.VideoWriter(filename, fourcc,  videoToProcess.get(cv2.CAP_PROP_FPS),(frame.shape[1]+img.shape[1], frame.shape[0]))
i = index
base = np.zeros((frame.shape[0], frame.shape[1]+img.shape[1], 3), np.uint8)
while i <= last:
    ret, frame = videoToProcess.read()
    if ret:
        base[:frame.shape[0], :frame.shape[1]] = frame
        img2 = img.copy()
        w = field_coordenates[data[:, 0].ravel() == i, 0:3]
        cv2.putText(img2, 'Frame:' + str(i),(50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)
        for l in w:
            cv2.putText(img2, str(int(l[2])),(int(l[0]), int(l[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)
        base[:img.shape[0], frame.shape[1]:] = img2
        out2.write(base)
        print(i)
        i += 1
    else:
        print("end of video")
        videoToProcess.release()
        break
