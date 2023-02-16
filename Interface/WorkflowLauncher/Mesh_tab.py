from PyQt5.QtCore import QDateTime, Qt, QTimer, QSize, QMargins, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QFileDialog, QFrame, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QMainWindow, QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTableWidgetItem, QTabWidget, QTextEdit,
        QTreeWidget, QTreeWidgetItem, QScrollArea, QSplitter, QStackedLayout, QTabWidget, QTabBar,
        QToolButton, QVBoxLayout, QWidget)
from PyQt5.QtGui import QIcon, QFont

from MekAnos.Data.Excel_Reader import read_dataset_info
from MekAnos.Interface.CustomClasses import CustomQTreeWidget, CustomQTreeWidgetItem

import numpy as np
import math

import sys

__version__ = '1.0'


class MeshTab(QWidget):
    def __init__(self, parent=None):
        super(MeshTab, self).__init__(parent)
        self.parent = parent

        self.mesh_type_layout = QGridLayout()
        self.setLayout(self.mesh_type_layout)
        self.setMaximumHeight(200)

        self.mesh_type_layout.addWidget(QLabel('Tetrahedron'), 1, 1)
        self.mesh_type_layout.addWidget(QLabel('Hexahedron'), 2, 1)
        self.mesh_type_layout.addWidget(QLabel('Hexahedron (voxel_based)'), 3, 1)
        self.mesh_type_layout.addWidget(QLabel('Order'), 0, 2, Qt.AlignCenter)
        self.mesh_type_layout.addWidget(QLabel('Method'), 0, 3)
        self.mesh_type_layout.addWidget(QLabel("Parameter (for several parameters, separate them with ';')"), 0, 4)

        self.is_tetra = QCheckBox()
        self.is_hexa = QCheckBox()
        self.is_voxel = QCheckBox()
        self.mesh_type_layout.addWidget(self.is_tetra, 1, 0)
        self.mesh_type_layout.addWidget(self.is_hexa, 2, 0)
        self.mesh_type_layout.addWidget(self.is_voxel, 3, 0)

        self.tetra_order_widget = QComboBox()
        self.hexa_order_widget = QComboBox()
        self.voxel_order_widget = QComboBox()
        self.tetra_order_widget.addItems(['Quadratic', 'Linear'])
        self.hexa_order_widget.addItems(['Quadratic', 'Linear'])
        self.voxel_order_widget.addItems(['Quadratic', 'Linear'])
        self.mesh_type_layout.addWidget(self.tetra_order_widget, 1, 2)
        self.mesh_type_layout.addWidget(self.hexa_order_widget, 2, 2)
        self.mesh_type_layout.addWidget(self.voxel_order_widget, 3, 2)

        self.tetra_method_widget = QComboBox()
        self.tetra_method_widget.addItems(['Element volume (cube mm)', 'Number of elements', 'Element size (mm)'])
        self.hexa_method_widget = QComboBox()
        self.hexa_method_widget.addItems(['Number of divisions', 'Element size (mm)'])
        self.voxel_method_widget = QComboBox()
        self.voxel_method_widget.addItems(['Number of divisions', 'Element size (mm)'])
        self.mesh_type_layout.addWidget(self.tetra_method_widget, 1, 3)
        self.mesh_type_layout.addWidget(self.hexa_method_widget, 2, 3)
        self.mesh_type_layout.addWidget(self.voxel_method_widget, 3, 3)
        self.tetra_parameter = QTextEdit('Enter parameter')
        self.hexa_parameter = QTextEdit('Enter parameter')
        self.voxel_parameter = QTextEdit('Enter parameter')
        self.mesh_type_layout.addWidget(self.tetra_parameter, 1, 4)
        self.mesh_type_layout.addWidget(self.hexa_parameter, 2, 4)
        self.mesh_type_layout.addWidget(self.voxel_parameter, 3, 4)


