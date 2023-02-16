from PyQt5.QtCore import QDateTime, Qt, QTimer, QSize, QMargins, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QFileDialog, QFrame, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QMainWindow, QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTableWidgetItem, QTabWidget, QTextEdit,
        QTreeWidget, QTreeWidgetItem, QScrollArea, QSplitter, QStackedLayout, QTabWidget, QTabBar,
        QToolButton, QVBoxLayout, QWidget)
from PyQt5.QtGui import QIcon, QFont

import sys

from module.Reader.cdb_reader import read_cdbfile
from module.Structure.Mekamesh import Mekamesh
from module.Interface.ModifyMesh import WindowModifyMekamesh
from module.Interface.ObjectInformationBox import ObjectInformationBox


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.originalPalette = QApplication.palette()
        self.setWindowTitle("Material Assignment 1.0")
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

        # read mesh and set path
        self.findPathButton = QPushButton('Find mesh')
        self.findPathButton.clicked.connect(self.open_path_finder)
        self.readButton = QPushButton('Read')
        self.readButton.clicked.connect(self.read_mesh)
        self.readPath = QLineEdit()
        path = "/Users/valentinallard/Mekabone/Projects/Single_vertebra_compression_folder/Patients/01_2007/Mekameshes/mekamesh_01_2007_11_2021-01-26-14-31-00.cdb"
        self.readPath.setPlaceholderText('Enter mesh path')
        self.readPath.setText(path)
        self.pathWidget = QWidget()
        self.pathLayout = QHBoxLayout()
        self.pathWidget.setLayout(self.pathLayout)
        self.pathLayout.addWidget(self.findPathButton)
        self.pathLayout.addWidget(self.readPath)
        self.pathLayout.addWidget(self.readButton)

        self.meshInfo = ObjectInformationBox()
        self.meshInfo.setDisabled(True)
        self.modify = QWidget()
        self.modify.setDisabled(True)
        self.modifyLayout = QVBoxLayout()
        self.modify.setLayout(self.modifyLayout)
        self.button_modify = QPushButton('Assign properties')
        self.button_modify.clicked.connect(self.assign_material)
        self.modifyLayout.addWidget(self.button_modify)
        self.writeButton = QPushButton('Write')
        self.writeButton.clicked.connect(self.write_mesh)
        self.modifyLayout.addWidget(self.writeButton)

        self.mainLayout.addWidget(self.pathWidget, 0, 0)
        self.mainLayout.addWidget(self.meshInfo, 1, 0)
        self.mainLayout.addWidget(self.modify, 2, 0)

        self.centralWidget.setLayout(self.mainLayout)
        self.mainLayout.setContentsMargins(QMargins())

    def open_path_finder(self):
        fileDialog = QFileDialog()
        filename = fileDialog.getOpenFileName()
        self.pathProject = filename[0]
        self.readPath.setText(self.pathProject)

    def update_mesh(self):
        self.meshInfo.fill(self.mekamesh)

    def read_mesh(self):
        path = self.readPath.text()
        ID = path.split('/')[-1]
        self.mekamesh = Mekamesh(ID, path)
        self.mekamesh.read()
        self.meshInfo.setDisabled(False)
        self.modify.setDisabled(False)
        self.meshInfo.fill(self.mekamesh)

    def assign_material(self):
        self.window_modify_mekamesh = WindowModifyMekamesh(self, [self.mekamesh])
        self.window_modify_mekamesh.show()
        self.window_modify_mekamesh.exec_()

    def write_mesh(self):
        self.mekamesh.write()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)  # for logos with good resolution
    window = MainWindow()
    window.show()
    app.exec_()