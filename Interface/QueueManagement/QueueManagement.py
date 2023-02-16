from PyQt5.QtCore import QDateTime, Qt, QTimer, QSize, QMargins, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QFileDialog, QFrame, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QMainWindow, QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTableWidgetItem, QTabWidget, QTextEdit,
        QTreeWidget, QTreeWidgetItem, QScrollArea, QSplitter, QStackedLayout, QTabWidget, QTabBar,
        QToolButton, QVBoxLayout, QWidget)
from PyQt5.QtGui import QIcon, QFont

import sys

__version__ = '1.0'


class QueueManagementWindow(QDialog):
    def __init__(self, parent=None):
        super(QueueManagementWindow, self).__init__(parent)

        self.parentWindow = parent
        self.originalPalette = QApplication.palette()
        self.setWindowTitle("Queue Management - " + __version__)
        self.styleName = 'Fusion'
        QApplication.setStyle(QStyleFactory.create(self.styleName))
        QApplication.setPalette(self.originalPalette)
        self.setStyleSheet('QGroupBox{font-size: 11pt;}'
                           'QGroupBox::title{color: #003066;}')

        self.setMinimumSize(600, 600)


        # main layout
        self.mainLayout = QGridLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setLayout(self.mainLayout)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)  # for logos with good resolution
    window = QueueManagementWindow()
    window.show()
    app.exec_()