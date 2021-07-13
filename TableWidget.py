from PyQt5.QtWidgets import QApplication, QWidget, QHeaderView, QAbstractItemView, QPushButton, QTableWidget, \
                            QTableWidgetItem, QVBoxLayout, QHBoxLayout
class TableWidget(QTableWidget):
    def __init__(self):
        super().__init__(1, 2)
        self.setHorizontalHeaderLabels(list('XY'))
        self.verticalHeader().setDefaultSectionSize(15)
        self.horizontalHeader().setDefaultSectionSize(50)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

    def _addRow(self):
        rowCount = self.rowCount()
        self.insertRow(rowCount )

    def _removeRow(self):
        if self.rowCount() > 0:
            self.removeRow(self.rowCount()-1)

    def _copyRow(self):
        self.insertRow(self.rowCount())
        rowCount = self.rowCount()
        columnCount = self.columnCount()

        for j in range(columnCount):
            if not self.item(rowCount-2, j) is None:
                self.setItem(rowCount-1, j, QTableWidgetItem(self.item(rowCount-2, j).text()))