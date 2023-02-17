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


        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)

        self.create_mesh_method_groupbox()
        self.create_mesh_analysis_groupbox()

        self.add_meshes_to_queue_button = QPushButton('Add meshes to queue')
        self.add_meshes_to_queue_button.clicked.connect(self.add_meshes_to_queue)
        self.add_meshes_to_queue_button.setDisabled(True)

        self.add_analysis_to_queue_button = QPushButton('Add analysis to queue')
        self.add_analysis_to_queue_button.clicked.connect(self.add_analysis_to_queue)
        self.add_analysis_to_queue_button.setDisabled(True)

        self.main_layout.addWidget(self.mesh_method_groupbox, 0, 0)
        self.main_layout.addWidget(self.mesh_analysis_groupbox, 1, 0)
        self.main_layout.addWidget(self.add_meshes_to_queue_button, 2, 0, 1, 2)
        self.main_layout.addWidget(self.add_analysis_to_queue_button, 3, 0, 1, 2)

    def create_mesh_method_groupbox(self):
        self.mesh_method_groupbox = QGroupBox('Meshing parameters')
        self.mesh_type_layout = QGridLayout()
        self.mesh_method_groupbox.setLayout(self.mesh_type_layout)
        self.mesh_method_groupbox.setMaximumHeight(200)

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
        self.tetra_parameter = QTextEdit()
        self.tetra_parameter.placeHolderText = 'Enter parameter'
        self.hexa_parameter = QTextEdit()
        self.hexa_parameter.placeHolderText = 'Enter parameter'
        self.voxel_parameter = QTextEdit()
        self.voxel_parameter.placeHolderText = 'Enter parameter'
        self.mesh_type_layout.addWidget(self.tetra_parameter, 1, 4)
        self.mesh_type_layout.addWidget(self.hexa_parameter, 2, 4)
        self.mesh_type_layout.addWidget(self.voxel_parameter, 3, 4)

    def create_mesh_analysis_groupbox(self):
        self.mesh_analysis_groupbox = QGroupBox('Mesh analysis')
        self.mesh_analysis_layout = QVBoxLayout()
        self.mesh_analysis_groupbox.setLayout(self.mesh_analysis_layout)

        self.mesh_elemental_volume = QCheckBox('Element volume')
        self.mesh_quality_1 = QCheckBox('Mesh Quality 1')
        self.mesh_quality_2 = QCheckBox('Mesh Quality 2')
        self.mesh_quality_3 = QCheckBox('Mesh Quality 3')

        self.mesh_analysis_layout.addWidget(self.mesh_elemental_volume)
        self.mesh_analysis_layout.addWidget(self.mesh_quality_1)
        self.mesh_analysis_layout.addWidget(self.mesh_quality_2)
        self.mesh_analysis_layout.addWidget(self.mesh_quality_3)

    def add_meshes_to_queue(self):
        print('add meshes to queue')

    def add_analysis_to_queue(self):
        print('add analysis to queue')


