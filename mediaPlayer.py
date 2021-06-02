from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QListWidget, QHBoxLayout,QListWidgetItem

from PyQt5.QtGui import QImage, QIcon
from PyQt5.QtCore import *
import cv2
import time


class MouseTracker(QtCore.QObject):
    positionChanged = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, widget):
        super().__init__(widget)
        self._widget = widget
        self.widget.setMouseTracking(True)
        self.widget.installEventFilter(self)

    @property
    def widget(self):
        return self._widget

    def eventFilter(self, o, e):
        if o is self.widget and e.type() == QtCore.QEvent.MouseMove:
            self.positionChanged.emit(e.pos())
        return super().eventFilter(o, e)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("PyQt5 Media Player")
        self.resize(rect.width(), rect.height())
        self.setMinimumSize(QtCore.QSize(640, 500))

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")

        self.video_label = QtWidgets.QLabel(self.centralwidget)
        self.video_label.setGeometry(QtCore.QRect(0, 0, rect.width(), rect.height()))
        #self.video_label.setMinimumSize(QtCore.QSize(640, 480))
        self.video_label.setStyleSheet("background-color: darkgray")
        self.video_label.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.video_label.setScaledContents(True)
        self.video_label.setObjectName("video_label")

        self.drag_label1 = QtWidgets.QLabel(self.centralwidget)
        self.drag_label1.setGeometry(QtCore.QRect(100, 50, 30,70))
        frame = cv2.imread("bandeira.png")
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.drag_label1.setPixmap(QtGui.QPixmap.fromImage(image))

        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(110, rect.height() - 60, 340, 20))
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

        self.pushButton_17 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_17.setGeometry(QtCore.QRect(10, 10, 80, 23))
        self.pushButton_17.setObjectName("pushButton_17")

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 40, 41, 344))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_5 = QtWidgets.QPushButton(self.widget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout.addWidget(self.pushButton_5)
        self.pushButton_6 = QtWidgets.QPushButton(self.widget)
        self.pushButton_6.setObjectName("pushButton_6")
        self.verticalLayout.addWidget(self.pushButton_6)
        self.pushButton_8 = QtWidgets.QPushButton(self.widget)
        self.pushButton_8.setObjectName("pushButton_8")
        self.verticalLayout.addWidget(self.pushButton_8)
        self.pushButton_7 = QtWidgets.QPushButton(self.widget)
        self.pushButton_7.setObjectName("pushButton_7")
        self.verticalLayout.addWidget(self.pushButton_7)
        self.pushButton_9 = QtWidgets.QPushButton(self.widget)
        self.pushButton_9.setObjectName("pushButton_9")
        self.verticalLayout.addWidget(self.pushButton_9)
        self.pushButton_11 = QtWidgets.QPushButton(self.widget)
        self.pushButton_11.setObjectName("pushButton_11")
        self.verticalLayout.addWidget(self.pushButton_11)
        self.pushButton_10 = QtWidgets.QPushButton(self.widget)
        self.pushButton_10.setObjectName("pushButton_10")
        self.verticalLayout.addWidget(self.pushButton_10)
        self.pushButton_12 = QtWidgets.QPushButton(self.widget)
        self.pushButton_12.setObjectName("pushButton_12")
        self.verticalLayout.addWidget(self.pushButton_12)
        self.pushButton_13 = QtWidgets.QPushButton(self.widget)
        self.pushButton_13.setObjectName("pushButton_13")
        self.verticalLayout.addWidget(self.pushButton_13)
        self.pushButton_14 = QtWidgets.QPushButton(self.widget)
        self.pushButton_14.setObjectName("pushButton_14")
        self.verticalLayout.addWidget(self.pushButton_14)
        self.pushButton_16 = QtWidgets.QPushButton(self.widget)
        self.pushButton_16.setObjectName("pushButton_16")
        self.verticalLayout.addWidget(self.pushButton_16)
        self.pushButton_15 = QtWidgets.QPushButton(self.widget)
        self.pushButton_15.setObjectName("pushButton_15")
        self.verticalLayout.addWidget(self.pushButton_15)        

        tracker = MouseTracker(self.video_label)
        tracker.positionChanged.connect(self.on_positionChanged)

        self.label_position = QtWidgets.QLabel(self.video_label, alignment=QtCore.Qt.AlignCenter)
        self.label_position.setStyleSheet('background-color: lightgreen; border: 1px solid black')
        self.label_position.setObjectName("label_position")

        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()

        #linkarfunções
        self.pushButton.clicked.connect(self.loadVideo)
        #self.pushButton_2.clicked.connect(self.mouse)
        self.pushButton_3.clicked.connect(self.playPause)
        self.pushButton_4.clicked.connect(self.reiniciar)
        self.pushButton_17.clicked.connect(self.marcar)
        self.pushButton_5.clicked.connect(lambda : self.createMarker((self.pushButton_5.x(), self.pushButton_5.y()), self.pushButton_5.objectName()))
        self.pushButton_6.clicked.connect(lambda : self.createMarker((self.pushButton_6.x(), self.pushButton_6.y()), self.pushButton_6.objectName()))
        self.pushButton_7.clicked.connect(lambda : self.createMarker((self.pushButton_7.x(), self.pushButton_7.y()), self.pushButton_7.objectName()))
        self.pushButton_8.clicked.connect(lambda : self.createMarker((self.pushButton_8.x(), self.pushButton_8.y()), self.pushButton_8.objectName()))

        #desabilitar botões
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)

        self.visibilityButton = False

        self.pushButton_5.setVisible(self.visibilityButton)
        self.pushButton_6.setVisible(self.visibilityButton)
        self.pushButton_7.setVisible(self.visibilityButton)
        self.pushButton_8.setVisible(self.visibilityButton)
        self.pushButton_9.setVisible(self.visibilityButton)
        self.pushButton_10.setVisible(self.visibilityButton)
        self.pushButton_11.setVisible(self.visibilityButton)
        self.pushButton_12.setVisible(self.visibilityButton)
        self.pushButton_13.setVisible(self.visibilityButton)
        self.pushButton_14.setVisible(self.visibilityButton)
        self.pushButton_15.setVisible(self.visibilityButton)
        self.pushButton_16.setVisible(self.visibilityButton)

        QtCore.QMetaObject.connectSlotsByName(self)

        self.started = False

        #Thead
        self.worker = ThreadClass()

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
        self.label_position.setText("(%d, %d)" % (pos.x(), pos.y()))
        self.label_position.adjustSize()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.pushButton.setText(_translate("MainWindow", "Open"))
        self.pushButton_2.setText(_translate("MainWindow", "Save"))
        self.pushButton_3.setText(_translate("MainWindow", "Play"))
        self.pushButton_4.setText(_translate("MainWindow", "Reiniciar"))
        self.pushButton_5.setText(_translate("MainWindow", "CE"))
        self.pushButton_6.setText(_translate("MainWindow", "CD"))
        self.pushButton_8.setText(_translate("MainWindow", "ME"))
        self.pushButton_7.setText(_translate("MainWindow", "MD"))
        self.pushButton_9.setText(_translate("MainWindow", "GAE1"))
        self.pushButton_11.setText(_translate("MainWindow", "GAE2"))
        self.pushButton_10.setText(_translate("MainWindow", "GAD1"))
        self.pushButton_12.setText(_translate("MainWindow", "GAD2"))
        self.pushButton_13.setText(_translate("MainWindow", "PAE1"))
        self.pushButton_14.setText(_translate("MainWindow", "PAE2"))
        self.pushButton_16.setText(_translate("MainWindow", "PAD1"))
        self.pushButton_15.setText(_translate("MainWindow", "PAD2"))
        self.pushButton_17.setText(_translate("MainWindow", "MARCAR"))

    def playPause(self):
        if self.started:
            self.started = False
            self.worker.stop()
            self.pushButton_3.setText("Play")
        else:
            self.started = True
            self.worker.start()
            self.pushButton_3.setText("Pause")

    def resizeImage(self, image):
        #print(image.shape)
        if image.shape[0] < rect.height() or image.shape[1] < rect.width():
            self.video_label.setGeometry(QtCore.QRect(0, 0, image.shape[1], image.shape[0]))
            self.layoutWidget.setGeometry(QtCore.QRect(110, image.shape[0] - 20, 340, 25))
            print("teste", self.video_label.geometry().width(), self.video_label.geometry().height())

    def setPhoto(self, image):
        if image.shape[0] > rect.height() or image.shape[1] > rect.width():
            dim = (rect.width(), rect.height())
            image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.video_label.setPixmap(QtGui.QPixmap.fromImage(image))

    def reiniciar(self):
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
            self.worker.resizeImage = self.resizeImage
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
            ret, frame = self.video.read()
            self.worker.video = self.video
            self.worker.resize = self.resizeImage
            self.worker.setPhoto = self.setPhoto
            self.worker.start()
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            if ret:
                self.resizeImage(frame)
                self.setPhoto(frame)

    def marcar(self):
        self.visibilityButton = ~self.visibilityButton
        self.pushButton_5.setVisible(self.visibilityButton)
        self.pushButton_6.setVisible(self.visibilityButton)
        self.pushButton_7.setVisible(self.visibilityButton)
        self.pushButton_8.setVisible(self.visibilityButton)
        self.pushButton_9.setVisible(self.visibilityButton)
        self.pushButton_10.setVisible(self.visibilityButton)
        self.pushButton_11.setVisible(self.visibilityButton)
        self.pushButton_12.setVisible(self.visibilityButton)
        self.pushButton_13.setVisible(self.visibilityButton)
        self.pushButton_14.setVisible(self.visibilityButton)
        self.pushButton_15.setVisible(self.visibilityButton)
        self.pushButton_16.setVisible(self.visibilityButton)
    
    def createMarker(self, pos, name):
        #print(pos[0], name)
        self.moveObject = MovingObject(pos[0]+50, pos[1], 40)

class ThreadClass(QThread):
    video = None
    resize = None
    setPhoto = None
    def run(self):
        a = 0
        self.is_running = True
        print('Starting thread...', )
        while self.video.isOpened() and self.is_running:
            ret, frame = self.video.read()
            if ret:
                self.setPhoto(frame)
                time.sleep(1/30)
            else:
                break
        print("Fim do video")

    def stop(self):
        self.is_running = False
        print('Stopping thread...')

    def kill(self):
        self.stop()
        time.sleep(0.5)


class MovingObject(QGraphicsEllipseItem):
    def __init__(self, x, y, r):
        super().__init__(0, 0, r, r)
        self.setPos(x, y)
        self.setBrush(Qt.blue)
        self.setAcceptHoverEvents(True)

    # mouse hover event
    def hoverEnterEvent(self, event):
        app.instance().setOverrideCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        app.instance().restoreOverrideCursor()

    # mouse click event
    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))

    def mouseReleaseEvent(self, event):
        print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    screen = app.primaryScreen()
    #print('Screen: %s' % screen.name())
    size = screen.size()
    #print('Size: %d x %d' % (size.width(), size.height()))
    rect = screen.availableGeometry()
    #print('Available: %d x %d' % (rect.width(), rect.height()))
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())