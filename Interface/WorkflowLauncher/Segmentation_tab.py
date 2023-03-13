from PyQt5.QtCore import QDateTime, Qt, QTimer, QSize, QMargins, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QFileDialog, QFrame, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QMainWindow, QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTableWidgetItem, QTabWidget, QTextEdit,
        QTreeWidget, QTreeWidgetItem, QScrollArea, QSplitter, QStackedLayout, QTabWidget, QTabBar,
        QToolButton, QVBoxLayout, QWidget)
from PyQt5.QtGui import QIcon, QFont

from Data.Excel_Reader import read_dataset_info
from Interface.CustomClasses import CustomQTreeWidget, CustomQTreeWidgetItem

import numpy as np
import math

import sys

__version__ = '1.0'


class SegmentationTab(QWidget):
    def __init__(self, parent=None):
        super(SegmentationTab, self).__init__(parent)
        self.parent = parent
        self.segTree = SegmentationTree(self.parent)
        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setLayout(self.layout)

        self.layout.addWidget(self.segTree)

    def get_selected_segmentations(self):
        for dataset_tree in self.segTree.dataset_tree_list:
            dataset = dataset_tree.dataset
            chosen_segmentation_list = dataset.get_chosen_segmentation_list()
            for scan_tree in dataset_tree.scan_tree_list:
                scan_name = scan_tree.scan_name
                for seg_item_tree in scan_tree.seg_item_tree_list:
                    seg_name = seg_item_tree.seg_name
                    if seg_item_tree.is_checked():
                        chosen_segmentation_list.append(scan_name + '_' + seg_name)


class SegmentationTree(CustomQTreeWidget):
    def __init__(self, parent=None):
        super(SegmentationTree, self).__init__(parent)
        self.parent = parent # parent here is the main window

        self.setMinimumHeight(150)
        self.setStyleSheet('QTreeWidget{font-size:10pt;}')
        self.setColumnCount(4)
        self.setHeaderLabels(['Dataset', 'Scan', '', 'Segmentation'])
        self.setColumnWidth(0, 200)
        self.setColumnWidth(1, 100)
        self.setColumnWidth(2, 30)
        self.setColumnWidth(3, 100)

    def fill(self):
        self.filled = False
        self.clear()
        self.dataset_tree_list = []
        for dataset in self.parent.datasets:
            count = 0
            for chosen in dataset.chosen_sample_ID_list:
                if chosen:
                    count += 1
            if count == 0:
                continue
            item_dataset = DatasetQTreeWidgetItem(self, dataset, count)
            item_dataset.setExpanded(True)
            self.dataset_tree_list.append(item_dataset)
            '''index = 0
            for scan in dataset.scans_list:
                item_scan = QTreeWidgetItem(item_dataset)
                item_scan.setCheckState(1, Qt.Checked)
                item_scan.setText(1, scan[0])
                item_scan.setExpanded(True)
                index += 1
                for seg in scan[1]:
                    item_seg = QTreeWidgetItem(item_scan)
                    item_seg.setCheckState(2, Qt.Checked)
                    item_seg.setText(2, seg)'''
        self.filled = True

    def handleItemChecked(self, item, column):
        if self.filled: # filling will create a problem as children widgetItems are not yet created
            if type(item) == ScanQTreeWidgetItem:
                if item.checkState(column) == 0:
                    for seg_item in item.seg_item_tree_list:
                        seg_item.setCheckState(3, Qt.Unchecked)
                        #seg_item.uncheck()
                elif item.checkState(column) == 2:
                    for seg_item in item.seg_item_tree_list:
                        seg_item.setCheckState(3, Qt.Checked)


class DatasetQTreeWidgetItem(CustomQTreeWidgetItem):
    def __init__(self, parent, dataset, index):
        self.parent = parent
        self.dataset = dataset
        super(DatasetQTreeWidgetItem, self).__init__(self.parent)
        self.setExpanded(True)

        self.index = index
        self.name = self.dataset.get_name()
        #self.obj = self.object_list[self.index]
        self.setText(0, self.name)

        #self.setFlags(self.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        self.scan_tree_list = []
        index_scan = 0
        for scan_infos in self.dataset.scans_list:
            scan_tree = ScanQTreeWidgetItem(self, scan_infos[0], scan_infos[1], index_scan)
            self.scan_tree_list.append(scan_tree)
            index_scan += 1

    def get_index(self):
        return self.index

    def get_parent(self):
        return self.parent


class ScanQTreeWidgetItem(CustomQTreeWidgetItem):
    def __init__(self, parent, scan_infos, seg_list, index_scan):
        self.parent = parent
        self.scan_infos = scan_infos
        self.scan_name = scan_infos
        self.index_scan = index_scan
        self.seg_list = seg_list
        self.parent_tree = self.parent.parent
        super(ScanQTreeWidgetItem, self).__init__(self.parent)

        self.setCheckState(1, Qt.Checked)

        #self.setFlags(self.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)

        self.setExpanded(True)

        self.setText(1, str(self.scan_infos))

        self.seg_item_tree_list = []
        index_seg = 0
        for seg in self.seg_list:
            seg_tree = SegQTreeWidgetItem(self, seg, index_seg)
            self.seg_item_tree_list.append(seg_tree)
            index_scan += 1


class SegQTreeWidgetItem(CustomQTreeWidgetItem):
    def __init__(self, parent, seg, index_seg):
        self.parent = parent
        self.seg_infos = seg
        self.seg_name = seg
        self.index_seg = index_seg
        self.parent_tree = self.parent.parent.parent
        super(SegQTreeWidgetItem, self).__init__(self.parent)

        self.setCheckState(3, Qt.Checked)
        self.setFlags(self.flags() | Qt.ItemIsUserCheckable)


        self.setText(3, str(self.seg_infos))

    def is_checked(self):
        if self.checkState(3) == 2:
            return True
        else:
            return False

    def uncheck(self):
        print(self.seg_infos)
        self.setCheckState(3, Qt.Unchecked)
