from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QDrag, QPixmap, QPainter
from PyQt5.QtCore import *
from PyQt5.QtCore import QMimeData, Qt

class pinLabel(QLabel):
    index = 0
    x = 0
    y = 0
    dx = 13
    dy = 50
    frameCoordanate = [0,0]

    def setup(self, index, i):
        self.index = index
        self.setGeometry(QtCore.QRect(0, 0, self.dx * 2, self.dy))
        self.x = index * 100 
        self.y = 200
        self.move(self.x - self.dx, self.y - self.dy)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        #self.setText(str(i) + '-' +str(self.index))
        self.setText(str(self.index))
        self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        a = "border-image: url(resources/pin"+str(i)+".png);"
        self.setStyleSheet(a)
        self.setObjectName("pin-" + str(i) + '-' + str(index))
        self.setVisible(False)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mimedata = QMimeData()
            mimedata.setText(self.text())
            drag.setMimeData(mimedata)
            pixmap = QPixmap(self.size())
            painter = QPainter(pixmap)
            painter.drawPixmap(self.rect(), self.grab())
            painter.end()
            drag.setPixmap(pixmap)
            drag.setHotSpot(QtCore.QPoint(self.dx, self.dy))
            drag.exec_(Qt.CopyAction | Qt.MoveAction)

    def drop(self, x, y, dx, dy, scale):
        self.move(x - self.dx, y - self.dy)
        self.x = x/scale
        self.y = y/scale
        #print('xy', x, y)
        self.setPositionToFrame([int(x/scale) + dx, int(y/scale) + dy])

    def movePin(self, x, y, scale):
        #self.move(int(self.x*scale) - x - self.dx, self.y - y - self.dy)
        self.x -= x/scale
        self.y -= y/scale

    def getPosition(self):
        return [self.x, self.y]

    def getPositionToFrame(self):
        return self.frameCoordanate

    def setPositionToFrame(self, a):
        self.frameCoordanate = a

    def releaseMouseEvent(self, event):
        return super(pinLabel, self).releaseMouseEvent(event)
