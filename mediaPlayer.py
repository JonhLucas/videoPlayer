from os import write
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage, QTransform
from PyQt5.QtCore import *
import cv2
import time
import numpy as np
import csv
#import pandas as pd

from mouseTracker import MouseTracker
from draggableLabel import draggableLabel
from myButton import myButton

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("PyQt5 Media Player")
        self.resize(rect.width(), rect.height())
        self.setMinimumSize(QtCore.QSize(640, 500))

        self.visibilityButton = False

        self.nameMarker = ["corner_left", "corner_right", "mind_left", "mind_right",
         "area_goal_line_left", "area_goal_line_right","area_line_left", "area_line_right",
         "box_goal_line_left", "box_goal_line_right", "box_line_left", "box_line_right"]
        
        self.frontLabel = QtWidgets.QLabel(self)
        self.frontLabel.setGeometry(QtCore.QRect(0, 0, rect.width(), rect.height()))
        self.frontLabel.setStyleSheet("background-color: darkgray")
        self.frontLabel.setObjectName("frontLabel")

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")

        self.videoLabel = QtWidgets.QLabel(self.centralwidget)
        self.videoLabel.setGeometry(QtCore.QRect(0, 0, rect.width(), rect.height()))
        self.videoLabel.setObjectName("videoLabel")

        self.fieldMap = QtWidgets.QLabel(self.centralwidget)
        self.fieldMap.setGeometry(QtCore.QRect(0, 0, 132, 210))
        self.fieldMap.setObjectName("fieldMap")
        pixmap = QtGui.QPixmap("resources/campo.png")
        pixmap = pixmap.transformed(QTransform().rotate(90))
        self.fieldMap.setPixmap(pixmap)
        self.fieldMap.setScaledContents(True)
        self.fieldMap.move(10, 50)
        self.fieldMap.setVisible(self.visibilityButton)

        self.marker = []
        for i in range(0,23):
            labelm = draggableLabel(self)
            labelm.move(0,0)
            labelm.setGeometry(QtCore.QRect(0, 0, 25, 25))
            labelm.setFrameShape(QtWidgets.QFrame.NoFrame)
            labelm.setPixmap(QtGui.QPixmap("resources/bandeira.png"))
            labelm.setScaledContents(True)
            labelm.setObjectName('marker' + str(i))
            labelm.setVisible(self.visibilityButton)
            self.marker.append(labelm)

        #positionButton = [[135,40],[5,40],[135,150],[5,150],[110,40],[31,40],[110,75],[31,75],[88,40],[50,40],[88,60],[50,60]]
        positionButton = [[135,40],[5,40],[135,150],[5,150],[110,40],[31,40],[110,75],[31,75],[88,40],[50,40],[88,60],[50,60], [69,150], [135,255],[5,255],[110,255],[31,255],[110,225],[31,225],[88,255],[50,255],[88,235],[50,235]]

        self.buttonList = []
        for i in range(0, 23):
            button = myButton(self.centralwidget)
            button.setObjectName("pushButton"+str(i))
            button.index = i
            button.setGeometry(QtCore.QRect(positionButton[i][0], positionButton[i][1], 15, 15))
            button.setVisible(self.visibilityButton)
            #button.setVisible(True)
            button.clicked.connect(lambda: self.buttonClicked(i, button))
            #self.verticalLayout.addWidget(button)
            self.buttonList.append(button)

        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(110, rect.height() - 80, 340, 20))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)

        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)

        self.check = QtWidgets.QPushButton(self.layoutWidget)
        self.check.setObjectName("check")
        self.horizontalLayout.addWidget(self.check)


        #Slider
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(460, rect.height() - 80, 261, 16))
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setVisible(False)
        self.horizontalSlider.setSliderPosition(50)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.valueChanged.connect(self.valueChanged)

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(10, 10, 80, 23))
        self.pushButton_5.setObjectName("mark")
        

        self.clean = QtWidgets.QPushButton(self.centralwidget)
        self.clean.setGeometry(QtCore.QRect(100, 10, 80, 23))
        self.clean.setObjectName("clean")
        self.clean.setText("clean")

        self.clear = QtWidgets.QPushButton(self.centralwidget)
        self.clear.setGeometry(QtCore.QRect(750, rect.height() - 80, 80, 23))
        self.clear.setObjectName("clear")
        self.clear.setText("clear")
        self.clear.setVisible(False)
        #self

        tracker = MouseTracker(self.videoLabel)
        tracker.positionChanged.connect(self.on_positionChanged)

        self.label_position = QtWidgets.QLabel(self.videoLabel, alignment=QtCore.Qt.AlignCenter)
        self.label_position.setStyleSheet('background-color: lightgreen; border: 1px solid black')
        self.label_position.setObjectName("label_position")

        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()

        QtCore.QMetaObject.connectSlotsByName(self)

        self.started = False

        self.index = None
        self.keepMarker = False

        self.dx = 0
        self.dy = 0
        self.frameWidth = rect.width()
        self.frameHeight = rect.height()

        self.frame = None
        self.resolution = [0,0]
        self.getted = []

        self.field = None
        self.fieldHomography = None
        self.imgField = cv2.imread("resources/campo.png")

        #Homography calculated
        self.checked = False

        #Thead
        self.worker = ThreadClass()

        self.setAcceptDrops(True)

    @QtCore.pyqtSlot(QtCore.QPoint)
    def on_positionChanged(self, pos):
        a = 30
        b = -15
        if self.videoLabel.geometry().width() < 3*a + pos.x():
            #print(self.frontLabel.geometry().width(), a + pos.x(), pos.x() - 2*a)
            a = -(a*2)
        delta = QtCore.QPoint(a, b)
        self.label_position.show()
        self.label_position.move(pos + delta)
        self.label_position.setText("(%d, %d)" % (pos.x() + self.dx, pos.y() + self.dy))
        self.label_position.adjustSize()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.pushButton.setText(_translate("MainWindow", "Open"))
        self.pushButton_2.setText(_translate("MainWindow", "Save"))
        self.pushButton_3.setText(_translate("MainWindow", "Play"))
        self.pushButton_4.setText(_translate("MainWindow", "Restart"))
        self.pushButton_5.setText(_translate("MainWindow", "Mark"))
        self.check.setText(_translate("MainWindow", "Check"))

        #linkar funções
        self.pushButton.clicked.connect(self.loadVideo)
        self.pushButton_2.clicked.connect(self.saveMarker)
        self.pushButton_3.clicked.connect(self.playPause)
        self.pushButton_4.clicked.connect(self.restart)
        self.pushButton_5.clicked.connect(self.toMark)
        self.clean.clicked.connect(self.cleanMarker)
        self.check.clicked.connect(self.checkMarker)
        self.clear.clicked.connect(self.clearField)

        #desabilitar botões
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        self.clean.setEnabled(False)
        self.check.setEnabled(False)

    def playPause(self):
        if self.started:
            self.started = False
            self.worker.stop()
            self.pushButton_3.setText("Play")
        else:
            self.started = True
            self.worker.start()
            self.pushButton_3.setText("Pause")

    def setPhoto(self, image):
        self.frame = image
        frame = cv2.cvtColor(image[self.dy: self.dy + self.frameHeight, self.dx: self.frameWidth + self.dx, :], cv2.COLOR_BGR2RGB)
        img = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        #print("setPhoto", frame.shape)
        self.frontLabel.setPixmap(QtGui.QPixmap.fromImage(img))

    def restart(self):
        self.worker.kill()
        self.worker.quit()
        if self.filename != "":
            self.started = True
            self.pushButton_3.setText("Pause")
            self.video = cv2.VideoCapture(self.filename)
            ret, frame = self.video.read()
            self.worker.video = self.video
            self.worker.start()

    def loadVideo(self):
        _translate = QtCore.QCoreApplication.translate
        #self.filename = QFileDialog.getOpenFileName(filter="video(*.mp4 *.avi)")[0]
        self.filename = QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        if self.filename != "":
            if self.started:
                self.started = False
                self.pushButton_3.setText("Play")
            else:
                self.started = True
                self.pushButton_3.setText("Pause")
            self.video = cv2.VideoCapture(self.filename)
            ret, self.frame = self.video.read()

            if self.frame.shape[0] < rect.height() or self.frame.shape[1] < rect.width():
                self.frameHeight = self.frame.shape[0]
                self.frameWidth = self.frame.shape[1]
            else:
                self.frameWidth = rect.width()
                self.frameHeight = rect.height()

            self.frontLabel.setGeometry(QtCore.QRect(0, 0, self.frameWidth, self.frameHeight))

            self.dx = 0
            self.dy = 0
            self.field = None
            self.horizontalSlider.setVisible(False)
            self.videoLabel.clear()

            self.worker.video = self.video
            self.worker.setPhoto = self.setPhoto
            try:
                self.worker.start()
            except:
                print("erro ao iniciar Theard de atualização de frames")
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            self.pushButton_5.setEnabled(True)
            self.check.setEnabled(True)
            self.clean.setEnabled(True)
            if ret:
                self.setPhoto(self.frame)

    def toMark(self):
        self.visibilityButton = ~self.visibilityButton
        for button in self.buttonList:
            button.setVisible(self.visibilityButton)
        self.fieldMap.setVisible(self.visibilityButton)

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        position = event.pos()
        i = self.marker.index(event.source())
        #print("posi", position.x(), position)
        self.marker[i].move(position.x(), position.y()-25)
        event.accept()

    def saveMarker(self):
        transparency = self.horizontalSlider.value() / 100
        filename = self.filename[:-4].split('/')
        cv2.imwrite(filename[-1] + "_output.png",  self.frame + self.field * transparency)
        #print(self.field.shape, self.frame.shape)
        filename = self.filename[:-4].split('/')
        doc = open(filename[-1] + '_points.csv', 'w')
        with doc:
            writer = csv.writer(doc)
            for row in self.getted:
                writer.writerow(row)
        doc.close()

    def cleanMarker(self):
        i = 0
        for marker in self.marker:
            marker.move(0, 0)
            marker.setVisible(False)
            i += 1
        for button in self.buttonList:
            button.setStyleSheet('background-color: white;')
        
    def buttonClicked(self, index, button):
        self.keepMarker = True
        self.index = (self.sender()).index
        #print("Here", (self.sender()).index)
        (self.sender()).setStyleSheet('background-color: red;')
    
    def moveMarker(self, a):
        for marker in self.marker:
            if marker.isVisible():
                position = marker.pos()
                marker.move(position.x() - a[0], position.y() - a[1])
                #print(position, position.x() - a[0], position.y() - a[1])

    def mousePressEvent(self, event):
        position = event.pos()
        if self.keepMarker:
            self.keepMarker = False
            self.marker[self.index].move(position.x(), position.y()-25)
            self.marker[self.index].setVisible(True)
        #print("clicked", self.index, event.pos())
        self.buttonList[self.index].setStyleSheet('background-color: green;')

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        a = 50
        if self.frame is not None:
            if (a0.key() == QtCore.Qt.Key_6):
                if self.frameWidth + self.dx + a > self.frame.shape[1]:
                    a = self.frame.shape[1] - (self.dx + self.frameWidth)
                self.dx += a
                self.moveMarker([a,0])
            elif (a0.key() == QtCore.Qt.Key_4):
                if self.dx - a < 0:
                    a = self.dx
                self.dx -= a
                self.moveMarker([-a,0])
            elif (a0.key() == QtCore.Qt.Key_8):
                if self.dy - a < 0:
                    a = self.dy
                self.dy -= a
                self.moveMarker([0, -a])
            elif (a0.key() == QtCore.Qt.Key_2):
                if self.frameHeight + self.dy + a > self.frame.shape[0]:
                    a = self.frame.shape[0] - (self.dy + self.frameHeight)
                self.dy += a
                self.moveMarker([0, a])
            self.setPhoto(self.frame)
            if self.field is not None:
                self.valueChanged()
        else:
            print("não iniciado")
        return super().keyPressEvent(a0)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.worker.kill()
        self.worker.quit()
        a0.accept()
        return super().closeEvent(a0)

    def getHomography(self, points, getted, index):
        H, mask = cv2.findHomography(points[index, 0:2], getted[index, 0:2], cv2.RANSAC, 5.0)

        id = np.zeros((23,1), np.int32)
        id[index] = mask

        return H, id

    def alline(self, imgs, M):
        '''w = np.array([[imgs[1].shape[1], 0, 1], [imgs[1].shape[1], imgs[1].shape[0], 1], [0, imgs[1].shape[0], 1], [0, 0, 1]])
        s = np.dot(M, w.T)
        for col in range(s.shape[1]):
            s[0, col] =  s[0, col] / s[2,col]
            s[1, col] =  s[1, col] / s[2,col]
        s = np.int32(s)
        dx = max(s[0])
        dy = max(s[1])'''
        dst = cv2.warpPerspective(imgs[1], M, (imgs[0].shape[1], imgs[0].shape[0]), borderValue = [0, 0, 0])
        return dst

    def clearField(self):
        self.videoLabel.clear()
        self.field = None
        self.clear.setVisible(False)
        self.horizontalSlider.setVisible(False)

    def drawField(self):
        transparency = self.horizontalSlider.value() / 100
        img = np.zeros((rect.height(), rect.width(), 4), np.int8)
        
        field = self.alline([self.frame, self.imgField], self.fieldHomography)
        self.field = field

        img[:self.frameHeight, :self.frameWidth, :3] = cv2.cvtColor(field[self.dy: self.dy + self.frameHeight,self.dx: self.dx + self.frameWidth,:], cv2.COLOR_BGR2RGB)

        mask = np.where(img[:,:,0] != 0)
        img[mask[0], mask[1], 3] = 255 * transparency

        image = QImage(img, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGBA8888)
        self.videoLabel.setPixmap(QtGui.QPixmap.fromImage(image))

    def checkMarker(self):
        points = np.array([[1050, 660, 1],[1050, 0, 1],[525, 660, 1],[525, 0, 1],[1050, 531.5, 1],[1050, 128.5, 1],[885, 531.5, 1], [885, 128.5, 1],[1050, 421.5, 1],[1050 ,238.5, 1],[995, 421.5, 1],[995, 238.5, 1], [525, 330, 1], [0, 660, 1],[0, 0, 1], [0, 531.5, 1],[0, 128.5, 1],[165, 531.5, 1], [165, 128.5, 1], [0, 421.5, 1], [0 ,238.5, 1], [55, 421.5, 1], [55, 238.5, 1]])
        indexVisible = np.zeros((23,1), np.int32)
        
        #Slider
        self.horizontalSlider.setVisible(True)
        self.clear.setVisible(True)
        self.checked = True

        #Pause video
        if self.started:
            self.playPause()

        #Save and filter visible marker
        self.pushButton_2.setEnabled(True)
        getted = []
        for i in range(len(self.marker)):
            getted.append([self.marker[i].x() + self.dx, self.marker[i].y() + 25 + self.dy, 1])
            if self.marker[i].isVisible():
                indexVisible[i] = 1
        self.getted = np.array(getted, np.float32)

        # Feild to frame
        self.fieldHomography, mask = self.getHomography(points, self.getted, indexVisible.ravel() == 1)
        
        #draw field image
        self.drawField()

        #Frame to field
        H1, mask = self.getHomography(self.getted, points, indexVisible.ravel() == 1)

        #save Homography
        filename = self.filename[:-4].split('/')
        doc = open(filename[-1] + '_homography.csv', 'w')
        with doc:
            writer = csv.writer(doc)
            for row in H1:
                writer.writerow(row)
        doc.close()
        
    def valueChanged(self):
        img = np.zeros((rect.height(), rect.width(), 4), np.int8)
        
        img[:self.frameHeight, :self.frameWidth, :3] = cv2.cvtColor(self.field[self.dy: self.dy + self.frameHeight,self.dx: self.dx + self.frameWidth,:], cv2.COLOR_BGR2RGB)
        mask = np.where(img[:,:,0] != 0)
        img[mask[0], mask[1], 3] = 255 * self.horizontalSlider.value() / 100

        image = QImage(img, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGBA8888)
        self.videoLabel.setPixmap(QtGui.QPixmap.fromImage(image))

class ThreadClass(QThread):
    video = None
    resize = None
    setPhoto = None
    def run(self):
        a = 0
        self.is_running = True
        while self.video.isOpened() and self.is_running:
            ret, frame = self.video.read()
            if ret:
                self.setPhoto(frame)
                time.sleep(1/30)
            else:
                break

    def stop(self):
        self.is_running = False

    def kill(self):
        self.stop()
        #time.sleep(0.1)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    screen = app.primaryScreen()
    size = screen.size()
    rect = screen.availableGeometry()
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())