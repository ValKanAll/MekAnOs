from PyQt5.QtCore import QDateTime, Qt, QTimer, QSize, QMargins, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QFileDialog, QFrame, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QMainWindow, QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTableWidgetItem, QTabWidget, QTextEdit,
        QTreeWidget, QTreeWidgetItem, QScrollArea, QSplitter, QStackedLayout, QTabWidget, QTabBar,
        QToolButton, QVBoxLayout, QWidget)
from PyQt5.QtGui import QIcon, QFont

from Data.Excel_Reader import read_dataset_info

import numpy as np
import math

import sys

__version__ = '1.0'


class CustomQTreeWidget(QTreeWidget):
    itemChecked = pyqtSignal(object, int)

    def __init__(self, parent=None):
        self.parent = parent
        super(CustomQTreeWidget, self).__init__(self.parent)

        self.itemChecked.connect(self.handleItemChecked)

    def handleItemChecked(self, item, column):
        print('ItemChecked', int(item.checkState(column)))


class CustomQTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent=None):
        self.parent = parent
        super(CustomQTreeWidgetItem, self).__init__(self.parent)

    def setData(self, column: int, role: int, value) -> None:
        state = self.checkState(column)
        QTreeWidgetItem.setData(self, column, role, value)
        if (role == Qt.CheckStateRole and state != self.checkState(column)):
            treewidget = self.treeWidget()
            if treewidget is not None:
                treewidget.itemChecked.emit(self, column)

CustomQTreeWidgetItem()


class CustomQToolButton(QToolButton):
    def __init__(self, text, icon_path, size=60, parent=None):
        super(CustomQToolButton, self).__init__(parent)

        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        #self.setStyleSheet('QToolButton{border: none;}')
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(size, size))
        if text:
            self.setText(text)
            self.setFixedWidth(size*5/3)
            self.setFixedHeight(size*5/3)

        else:
            self.setFixedHeight(size*5/3)