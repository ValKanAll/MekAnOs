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
        self.main_layout.addWidget(self.mesh_analysis_groupbox, 0, 1)
        self.main_layout.addWidget(self.add_meshes_to_queue_button, 1, 0, 1, 2)
        self.main_layout.addWidget(self.add_analysis_to_queue_button, 2, 0, 1, 2)

        self.tab_reaction()

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
        self.tetra_parameter = QLineEdit()
        self.tetra_parameter.placeHolderText = 'Enter parameter'
        self.hexa_parameter = QLineEdit()
        self.hexa_parameter.placeHolderText = 'Enter parameter'
        self.voxel_parameter = QLineEdit()
        self.voxel_parameter.placeHolderText = 'Enter parameter'
        self.mesh_type_layout.addWidget(self.tetra_parameter, 1, 4)
        self.mesh_type_layout.addWidget(self.hexa_parameter, 2, 4)
        self.mesh_type_layout.addWidget(self.voxel_parameter, 3, 4)

        self.is_tetra.clicked.connect(self.tab_reaction)
        self.is_hexa.clicked.connect(self.tab_reaction)
        self.is_voxel.clicked.connect(self.tab_reaction)
        self.tetra_method_widget.currentIndexChanged.connect(self.tab_reaction)
        self.hexa_method_widget.currentIndexChanged.connect(self.tab_reaction)
        self.voxel_method_widget.currentIndexChanged.connect(self.tab_reaction)
        self.tetra_order_widget.currentIndexChanged.connect(self.tab_reaction)
        self.hexa_order_widget.currentIndexChanged.connect(self.tab_reaction)
        self.voxel_order_widget.currentIndexChanged.connect(self.tab_reaction)
        self.tetra_parameter.textChanged.connect(self.tab_reaction)
        self.hexa_parameter.textChanged.connect(self.tab_reaction)
        self.voxel_parameter.textChanged.connect(self.tab_reaction)

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

        self.mesh_elemental_volume.clicked.connect(self.tab_reaction)
        self.mesh_quality_1.clicked.connect(self.tab_reaction)
        self.mesh_quality_2.clicked.connect(self.tab_reaction)
        self.mesh_quality_3.clicked.connect(self.tab_reaction)

    def tab_reaction(self):
        if self.is_tetra.checkState() == 0:
            self.tetra_method_widget.setDisabled(True)
            self.tetra_parameter.setDisabled(True)
            self.tetra_order_widget.setDisabled(True)
        elif self.is_tetra.checkState() == 2:
            self.tetra_method_widget.setDisabled(False)
            self.tetra_parameter.setDisabled(False)
            self.tetra_order_widget.setDisabled(False)

        if self.is_hexa.checkState() == 0:
            self.hexa_method_widget.setDisabled(True)
            self.hexa_parameter.setDisabled(True)
            self.hexa_order_widget.setDisabled(True)
        elif self.is_hexa.checkState() == 2:
            self.hexa_method_widget.setDisabled(False)
            self.hexa_parameter.setDisabled(False)
            self.hexa_order_widget.setDisabled(False)

        if self.is_voxel.checkState() == 0:
            self.voxel_method_widget.setDisabled(True)
            self.voxel_parameter.setDisabled(True)
            self.voxel_order_widget.setDisabled(True)
        elif self.is_voxel.checkState() == 2:
            self.voxel_method_widget.setDisabled(False)
            self.voxel_parameter.setDisabled(False)
            self.voxel_order_widget.setDisabled(False)

        if (self.is_tetra.checkState() == 2 and self.tetra_parameter.text() != "")\
                or (self.is_hexa.checkState() == 2 and self.hexa_parameter.text() != "")\
                or (self.is_voxel.checkState() == 2 and self.voxel_parameter.text() != ""):
            self.add_meshes_to_queue_button.setDisabled(False)
            self.mesh_analysis_groupbox.setDisabled(False)
            self.parent.get_meshes()
        else:
            self.add_meshes_to_queue_button.setDisabled(True)
            self.meshes = []
            self.mesh_analysis_groupbox.setDisabled(True)

        if self.mesh_elemental_volume.checkState() == 0\
            and self.mesh_quality_1.checkState() == 0\
            and self.mesh_quality_2.checkState() == 0\
            and self.mesh_quality_3.checkState() == 0:
            self.add_analysis_to_queue_button.setDisabled(True)
        else:
            self.add_analysis_to_queue_button.setDisabled(False)

    def add_meshes_to_queue(self):
        self.parent.get_selected_seg()
        if self.is_tetra.checkState() == 2:
            if self.tetra_order_widget.currentIndex() == 0:
                self.tetra_element_type = 'QT'
            elif self.tetra_order_widget.currentIndex() == 1:
                self.tetra_element_type = 'LT'
            self.tetra_method = self.tetra_method_widget.currentIndex()
            if self.tetra_method == 0:
                self.tetra_element_type += 'V'  # element volume
            elif self.tetra_method == 1:
                self.tetra_element_type += 'N'  # number of element
            elif self.tetra_method == 2:
                self.tetra_element_type += 'S'  # element size
            self.tetra_params = self.tetra_parameter.text().split(';')
            WL = Waiting_list()
            self.datasets = self.parent.datasets
            WL.add_meshing(datasets=self.datasets, element_type=self.tetra_element_type,
                             params=self.tetra_params)

        if self.is_hexa.checkState() == 2:
            if self.hexa_order_widget.currentIndex() == 0:
                self.hexa_element_type = 'QH'
            elif self.hexa_order_widget.currentIndex() == 1:
                self.hexa_element_type = 'LH'
            self.hexa_method = self.hexa_method_widget.itemText(self.hexa_method_widget.currentIndex())
            if self.hexa_method == 0:
                self.hexa_element_type += 'D'  # number of divisions
            elif self.hexa_method == 1:
                self.hexa_element_type += 'S'  # element size
            self.hexa_params = self.hexa_parameter.text().split(';')
            WL = Waiting_list()
            self.datasets = self.parent.datasets
            WL.add_meshing(datasets=self.datasets, element_type=self.hexa_element_type,
                             params=self.hexa_params)

        if self.is_voxel.checkState() == 2:
            if self.voxel_order_widget.currentIndex() == 0:
                self.voxel_element_type = 'QV'
            elif self.voxel_order_widget.currentIndex() == 1:
                self.voxel_element_type = 'LV'
            self.voxel_method = self.voxel_method_widget.itemText(self.voxel_method_widget.currentIndex())
            if self.voxel_method == 0:
                self.voxel_element_type += 'D'  # number of divisions
            elif self.voxel_method == 1:
                self.voxel_element_type += 'S'  # element size
            self.voxel_params = self.voxel_parameter.text().split(';')
            WL = Waiting_list()
            self.datasets = self.parent.datasets
            WL.add_meshing(datasets=self.datasets, element_type=self.voxel_element_type,
                             params=self.voxel_params)



        print('added meshes to queue')

    def get_meshes(self):
        self.selected_meshes = []
        if self.is_tetra.checkState() == 2:
            if self.tetra_order_widget.currentIndex() == 0:
                self.tetra_element_type = 'QT'
            elif self.tetra_order_widget.currentIndex() == 1:
                self.tetra_element_type = 'LT'
            self.tetra_method = self.tetra_method_widget.currentIndex()
            if self.tetra_method == 0:
                self.tetra_element_type += 'V'  # element volume
            elif self.tetra_method == 1:
                self.tetra_element_type += 'N'  # number of element
            elif self.tetra_method == 2:
                self.tetra_element_type += 'S'  # element size
            self.tetra_params = self.tetra_parameter.text().split(';')

            for param in self.tetra_params:
                self.selected_meshes.append(self.tetra_element_type + '_' + param)

        if self.is_hexa.checkState() == 2:
            if self.hexa_order_widget.currentIndex() == 0:
                self.hexa_element_type = 'QH'
            elif self.hexa_order_widget.currentIndex() == 1:
                self.hexa_element_type = 'LH'
            self.hexa_method = self.hexa_method_widget.itemText(self.hexa_method_widget.currentIndex())
            if self.hexa_method == 0:
                self.hexa_element_type += 'D'  # number of divisions
            elif self.hexa_method == 1:
                self.hexa_element_type += 'S'  # element size
            self.hexa_params = self.hexa_parameter.text().split(';')

            for param in self.hexa_params:
                self.selected_meshes.append(self.hexa_element_type + '_' + param)

        if self.is_voxel.checkState() == 2:
            if self.voxel_order_widget.currentIndex() == 0:
                self.voxel_element_type = 'QV'
            elif self.voxel_order_widget.currentIndex() == 1:
                self.voxel_element_type = 'LV'
            self.voxel_method = self.voxel_method_widget.itemText(self.voxel_method_widget.currentIndex())
            if self.voxel_method == 0:
                self.voxel_element_type += 'D'  # number of divisions
            elif self.voxel_method == 1:
                self.voxel_element_type += 'S'  # element size
            self.voxel_params = self.voxel_parameter.text().split(';')

            for param in self.voxel_params:
                self.selected_meshes.append(self.voxel_element_type + '_' + param)

        return self.selected_meshes

    def add_analysis_to_queue(self):
        self.parent.get_selected_seg()
        self.mesh_analysis = []
        if self.mesh_elemental_volume.checkState() == 2:
            self.mesh_analysis.append('element_volume')
        if self.mesh_quality_1.checkState() == 2:
            self.mesh_analysis.append('mesh_quality_1')
        if self.mesh_quality_2.checkState() == 2:
            self.mesh_analysis.append('mesh_quality_2')
        if self.mesh_quality_3.checkState() == 2:
            self.mesh_analysis.append('mesh_quality_3')

        if self.is_tetra.checkState() == 2:
            if self.tetra_order_widget.currentIndex() == 0:
                self.tetra_element_type = 'QT'
            elif self.tetra_order_widget.currentIndex() == 1:
                self.tetra_element_type = 'LT'
            self.tetra_method = self.tetra_method_widget.currentIndex()
            if self.tetra_method == 0:
                self.tetra_element_type += 'V'  # element volume
            elif self.tetra_method == 1:
                self.tetra_element_type += 'N'  # number of element
            elif self.tetra_method == 2:
                self.tetra_element_type += 'S'  # element size
            self.tetra_params = self.tetra_parameter.text().split(';')
            WL = Waiting_list()
            self.datasets = self.parent.datasets
            WL.add_mesh_analysis(datasets=self.datasets, element_type=self.tetra_element_type,
                             params=self.tetra_params, mesh_analysis=self.mesh_analysis)

        if self.is_hexa.checkState() == 2:
            if self.hexa_order_widget.currentIndex() == 0:
                self.hexa_element_type = 'QH'
            elif self.hexa_order_widget.currentIndex() == 1:
                self.hexa_element_type = 'LH'
            self.hexa_method = self.hexa_method_widget.currentIndex()
            if self.hexa_method == 0:
                self.hexa_element_type += 'D'  # number of divisions
            elif self.hexa_method == 1:
                self.hexa_element_type += 'S'  # element size
            self.hexa_params = self.hexa_parameter.text().split(';')
            WL = Waiting_list()
            self.datasets = self.parent.datasets
            WL.add_mesh_analysis(datasets=self.datasets, element_type=self.hexa_element_type,
                             params=self.hexa_params, mesh_analysis=self.mesh_analysis)

        if self.is_voxel.checkState() == 2:
            if self.voxel_order_widget.currentIndex() == 0:
                self.voxel_element_type = 'QV'
            elif self.voxel_order_widget.currentIndex() == 1:
                self.voxel_element_type = 'LV'
            self.voxel_method = self.voxel_method_widget.currentIndex()
            if self.voxel_method == 0:
                self.voxel_element_type += 'D'  # number of divisions
            elif self.voxel_method == 1:
                self.voxel_element_type += 'S'  # element size
            self.voxel_params = self.voxel_parameter.text().split(';')
            WL = Waiting_list()
            self.datasets = self.parent.datasets
            WL.add_mesh_analysis(datasets=self.datasets, element_type=self.voxel_element_type,
                             params=self.voxel_params, mesh_analysis=self.mesh_analysis)

        print('added mesh analysis to queue')


