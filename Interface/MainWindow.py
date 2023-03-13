from PyQt5.QtCore import Qt, QMargins
from PyQt5.QtWidgets import (QApplication, QFileDialog, QGridLayout, QMainWindow, QPushButton, QStyleFactory, QWidget)
import datetime

import sys

from Interface.QueueManagement.QueueManagement import QueueManagementWindow
from Interface.WorkflowLauncher.WorkflowLauncherWindow import WorkflowLauncherWindow
from Interface.FileVisioner.FileVisioner import FileVisionerWindow
from Interface.ResultAnalyser.ResultsAnalyser import ResultsAnalyserWindow
from Interface.CustomClasses import CustomQToolButton

__version__ = '1.0'


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.originalPalette = QApplication.palette()
        self.setWindowTitle("MekAnOs workflow - " + __version__)
        self.styleName = 'Fusion'
        QApplication.setStyle(QStyleFactory.create(self.styleName))
        QApplication.setPalette(self.originalPalette)
        self.setStyleSheet('QGroupBox{font-size: 11pt;}'
                           'QGroupBox::title{color: #003066;}')

        self.setMinimumSize(600, 600)
        self.centralWidget = QWidget()

        self.setCentralWidget(self.centralWidget)

        # main layout
        self.mainLayout = QGridLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(QMargins(0, 0, 0, 0))

        # choose amongst workflow launcher (from scan to result), queue management window, file visioner, results analysis
        # find front page in mekabone
        # set up gitHub
        # change logo
        # check pyqt5 version stability, the used for Mekabone

        # Workflow launcher
        self.WLButton = CustomQToolButton('Workflow launcher', r'Images/workflow.png', 150)
        self.WLButton.clicked.connect(self.open_WL)

        # Queue management
        self.QMButton = CustomQToolButton('Queue management', r'Images/waiting_list.png', 150)
        self.QMButton.clicked.connect(self.open_QM) # it could be nice to launch a new and independent thread not depending from the main application

        # File visioner
        self.FVButton = CustomQToolButton('File visionner', r'Images/eye-blue.svg', 150)
        self.FVButton.clicked.connect(self.open_FV)

        # Results analyser (with autoplot and saving,  possibility to choose between pyplot and matplotlib)
        self.RAButton = CustomQToolButton('Results analyser', r'Images/poll.svg', 150)
        self.RAButton.clicked.connect(self.open_RA)

        self.mainLayout.addWidget(self.WLButton, 0, 0)
        self.mainLayout.addWidget(self.QMButton, 0, 1)
        self.mainLayout.addWidget(self.FVButton, 1, 0)
        self.mainLayout.addWidget(self.RAButton, 1, 1)

        self.centralWidget.setLayout(self.mainLayout)
        self.mainLayout.setContentsMargins(QMargins())

    def open_WL(self):
        print('Workflow launcher opened at {}'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        WLWindow = WorkflowLauncherWindow(self)
        WLWindow.show()
        pass

    def open_QM(self):
        print('Queue management opened at {}'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        QMWindow = QueueManagementWindow(self)
        QMWindow.show()
        pass

    def open_FV(self):
        print('File visioner opened at {}'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        FVWindow = FileVisionerWindow(self)
        FVWindow.show()
        pass

    def open_RA(self):
        print('Results analyser opened at {}'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        RAWindow = ResultsAnalyserWindow(self)
        RAWindow.show()
        pass

    def open_path_finder(self):
        fileDialog = QFileDialog()
        filename = fileDialog.getOpenFileName()
        self.pathProject = filename[0]
        self.readPath.setText(self.pathProject)


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        app.setAttribute(Qt.AA_UseHighDpiPixmaps)  # for logos with good resolution
        window = MainWindow()
        window.show()
        app.exec_()
    except Exception as e:
        print(e)