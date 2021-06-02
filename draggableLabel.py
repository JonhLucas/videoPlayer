from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QDrag, QPixmap, QPainter
from PyQt5.QtCore import *

class draggableLabel(QLabel):
    position = None
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
            drag.setHotSpot(QtCore.QPoint(0, 25))
            drag.exec_(Qt.CopyAction | Qt.MoveAction)

    def releaseMouseEvent(self, event):
        return super(draggableLabel, self).releaseMouseEvent(event)
