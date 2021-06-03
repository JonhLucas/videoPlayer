from os import write
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage
from PyQt5.QtCore import *
import cv2
import time
import numpy as np

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

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")

        self.video_label = QtWidgets.QLabel(self.centralwidget)
        self.video_label.setGeometry(QtCore.QRect(0, 0, rect.width(), rect.height()))
        self.video_label.setStyleSheet("background-color: darkgray")
        self.video_label.setObjectName("video_label")

        self.marker = []
        for i in range(0,12):
            labelm = draggableLabel(self)
            labelm.move(0,0)
            labelm.setGeometry(QtCore.QRect(0, 0, 25, 25))
            labelm.setFrameShape(QtWidgets.QFrame.NoFrame)
            labelm.setPixmap(QtGui.QPixmap("resources/bandeira.png"))
            labelm.setScaledContents(True)
            labelm.setObjectName(self.nameMarker[i])
            labelm.setVisible(self.visibilityButton)
            self.marker.append(labelm)
        
        self.buttonLayout = QtWidgets.QWidget(self.centralwidget)
        self.buttonLayout.setGeometry(QtCore.QRect(10, 40, 120, 360))
        self.buttonLayout.setObjectName("buttonLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.buttonLayout)
        self.verticalLayout.setContentsMargins(0,0,0,0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.buttonList = []
        for i in range(0, 12):
            button = myButton()
            button.setObjectName("pushButton"+str(i))
            button.index = i
            button.setVisible(self.visibilityButton)
            button.clicked.connect(lambda: self.buttonClicked(i, button))
            self.verticalLayout.addWidget(button)
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
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.check = QtWidgets.QPushButton(self.layoutWidget)
        self.check.setObjectName("check")
        self.horizontalLayout.addWidget(self.check)

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(10, 10, 80, 23))
        self.pushButton_5.setObjectName("save")

        self.clean = QtWidgets.QPushButton(self.centralwidget)
        self.clean.setGeometry(QtCore.QRect(100, 10, 80, 23))
        self.clean.setObjectName("clean")
        self.clean.setText("clean")

        tracker = MouseTracker(self.video_label)
        tracker.positionChanged.connect(self.on_positionChanged)

        self.label_position = QtWidgets.QLabel(self.video_label, alignment=QtCore.Qt.AlignCenter)
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

        self.frame = None
        self.resolution = [0,0]
        self.getted = []

        #Thead
        self.worker = ThreadClass()

        self.setAcceptDrops(True)

    @QtCore.pyqtSlot(QtCore.QPoint)
    def on_positionChanged(self, pos):
        a = 30
        b = -15
        if self.video_label.geometry().width() < 3*a + pos.x():
            #print(self.video_label.geometry().width(), a + pos.x(), pos.x() - 2*a)
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
        self.buttonList[0].setText(_translate("MainWindow", "Corner esquerdo"))
        self.buttonList[1].setText(_translate("MainWindow", "Corner direito"))        
        self.buttonList[2].setText(_translate("MainWindow", "Meio esquerdo"))
        self.buttonList[3].setText(_translate("MainWindow", "Meio direito"))
        self.buttonList[4].setText(_translate("MainWindow", "Grande area 1"))
        self.buttonList[5].setText(_translate("MainWindow", "Grande area 2"))
        self.buttonList[6].setText(_translate("MainWindow", "Grande area 3"))
        self.buttonList[7].setText(_translate("MainWindow", "Grande area 4"))
        self.buttonList[8].setText(_translate("MainWindow", "Pequena area 1"))
        self.buttonList[9].setText(_translate("MainWindow", "Pequena area 2"))
        self.buttonList[10].setText(_translate("MainWindow", "Pequena area 3"))
        self.buttonList[11].setText(_translate("MainWindow", "Pequena area 4"))

        #linkar funções
        self.pushButton.clicked.connect(self.loadVideo)
        self.pushButton_2.clicked.connect(self.saveMarker)
        self.pushButton_3.clicked.connect(self.playPause)
        self.pushButton_4.clicked.connect(self.restart)
        self.pushButton_5.clicked.connect(self.toMark)
        self.clean.clicked.connect(self.cleanMarker)
        self.check.clicked.connect(self.checkMarker)

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
        frame = cv2.cvtColor(image[self.dy: self.dy + rect.height(), self.dx: rect.width() + self.dx, :], cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.video_label.setPixmap(QtGui.QPixmap.fromImage(image))

    def restart(self):
        self.worker.kill()
        self.worker.quit()
        if self.filename != "":
            if self.started:
                self.started = False
                self.pushButton_3.setText("Play")
            else:
                self.started = True
                self.pushButton_3.setText("Pause")
            self.video = cv2.VideoCapture(self.filename)
            ret, frame = self.video.read()
            self.worker.video = self.video
            self.worker.start()

    def loadVideo(self):
        _translate = QtCore.QCoreApplication.translate
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
            self.worker.video = self.video
            self.worker.setPhoto = self.setPhoto
            self.worker.start()
            self.pushButton_2.setEnabled(True)
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

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        position = event.pos()
        i = self.marker.index(event.source())
        #print("posi", position.x(), position)
        self.marker[i].move(position.x(), position.y()-25)
        event.accept()

    def saveMarker(self):
        getted = []
        arquivo = open('coordenadas.txt', 'w')
        arquivo.write('[[' + str(self.marker[0].x()+self.dx) + ',' +str(self.marker[0].y() + 25 + self.dy) + ',1]')
        getted.append([self.marker[0].x()+self.dx, self.marker[0].y() + 25 + self.dy, 1])
        for marker in self.marker[1:]:
            arquivo.write(',['+ str(marker.x( )+ self.dx)+ ',' + str(marker.y()+25+self.dy) + ',1]')
            getted.append([marker.x() + self.dx, marker.y() + 25 + self.dy, 1])
        arquivo.write(']')
        arquivo.close()
        self.getted = np.array(getted, np.float32)
        '''ret, self.frame = self.video.read()
        cv2.imwrite("frame.png", self.frame)'''

    def cleanMarker(self):
        i = 0
        for marker in self.marker:
            marker.move(0, 0)
            marker.setVisible(False)
            i += 1
        
    def buttonClicked(self, index, button):
        self.keepMarker = True
        self.index = (self.sender()).index
        #print("Here", (self.sender()).index)
    
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

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        a = 50
        if self.frame is not None:
            if (a0.key() == QtCore.Qt.Key_6):
                if rect.width() + self.dx + a > self.frame.shape[1]:
                    a = self.frame.shape[1] - (self.dx + rect.width())
                    #print(self.frame.shape[1], self.dx, rect.width(), a)
                self.dx += a
                self.moveMarker([a,0])
                self.setPhoto(self.frame)
            elif (a0.key() == QtCore.Qt.Key_4):
                if self.dx - a < 0:
                    a = self.dx
                self.dx -= a
                self.moveMarker([-a,0])
                self.setPhoto(self.frame)
            elif (a0.key() == QtCore.Qt.Key_8):
                if self.dy - a < 0:
                    a = self.dy
                self.dy -= a
                self.moveMarker([0, -a])
                self.setPhoto(self.frame)
            elif (a0.key() == QtCore.Qt.Key_2):
                if rect.height() + self.dy + a > self.frame.shape[0]:
                    a = self.frame.shape[0] - (self.dy + rect.height())
                    #print(self.frame.shape[0] , (self.dy + rect.height()))
                self.dy += a
                self.moveMarker([0, a])
                self.setPhoto(self.frame)
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

        id = np.zeros((12,1), np.int32)
        id[index] = mask

        return H, id

    def alline(self, imgs, M):
        w = np.array([[imgs[1].shape[1], 0, 1], [imgs[1].shape[1], imgs[1].shape[0], 1], [0, imgs[1].shape[0], 1], [0, 0, 1]])
        s = np.dot(M, w.T)
        for col in range(s.shape[1]):
            s[0, col] =  s[0, col] / s[2,col]
            s[1, col] =  s[1, col] / s[2,col]
        s = np.int32(s)
        dx = max(s[0])
        dy = max(s[1])
        dst = cv2.warpPerspective(imgs[1], M, ( max(dx, imgs[0].shape[1]), max(dy, imgs[0].shape[0])), borderValue = [0, 0, 0])
        return dst

    def drawField(self, H, mask):
        field = cv2.imread("resources/campo.png")
        result = self.frame.copy()

        fieldPerspective = self.alline([self.frame, field], H)

        result[np.where(fieldPerspective != [0,0,0])] = fieldPerspective[np.where(fieldPerspective != [0,0,0])]
        cv2.imwrite("result.png", result)

        #update frame
        self.setPhoto(result)

    def checkMarker(self):
        points = np.array([[1050, 660, 1],[1050, 0, 1],[525, 660, 1],[525, 0, 1],[1050, 531.5, 1],[1050, 128.5, 1],[885, 531.5, 1], [885, 128.5, 1],[1050, 421.5, 1],[1050 ,238.5, 1],[995, 421.5, 1],[995, 238.5, 1]])
        indexVisible = np.zeros((12,1), np.int32)

        #Pause video
        if self.started:
            self.playPause()

        #Save and filter visible marker
        self.saveMarker()
        for i in range(len(self.marker)):
            if self.marker[i].isVisible():
                indexVisible[i] = 1

        # Feild to frame
        H, mask = self.getHomography(points, self.getted, indexVisible.ravel() == 1)
        
        #draw field image
        self.drawField(H, mask)

        #Frame to field
        H1, mask = self.getHomography(self.getted, points, indexVisible.ravel() == 1)

        #check
        print("Expected\n", self.getted[:,0:2])
        a = np.dot(H, points.T).T
        result = a[:,0:2]/a[:,2:3]
        print("Result\n", result)


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
        time.sleep(0.1)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    screen = app.primaryScreen()
    size = screen.size()
    rect = screen.availableGeometry()
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())