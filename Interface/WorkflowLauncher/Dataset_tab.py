from PyQt5.QtCore import QDateTime, Qt, QTimer, QSize, QMargins, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QFileDialog, QFrame, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QMainWindow, QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTableWidgetItem, QTabWidget, QTextEdit,
        QTreeWidget, QTreeWidgetItem, QScrollArea, QSplitter, QStackedLayout, QTabWidget, QTabBar,
        QToolButton, QVBoxLayout, QWidget)
from PyQt5.QtGui import QIcon, QFont

from MekAnos.Data.Excel_Reader import read_dataset_info

import numpy as np
import math

import sys

__version__ = '1.0'


class DatasetTab(QWidget):
    def __init__(self, parent=None):
        super(DatasetTab, self).__init__(parent)
        self.parent = parent
        self.datasetTree = DatasetTree(self)
        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setLayout(self.layout)

        self.layout.addWidget(self.datasetTree)

    def get_selected_samples(self):
        for dataset_tree_item in self.datasetTree.dataset_tree_item_list:
            dataset = dataset_tree_item.dataset
            for sample_tree in dataset_tree_item.samples_tree_list:
                if sample_tree.checkState(0) == Qt.Checked:
                    dataset.chosen_sample_ID_list[sample_tree.index_sample] = True
                elif sample_tree.checkState(0) == Qt.Unchecked:
                    dataset.chosen_sample_ID_list[sample_tree.index_sample] = False
            #print(dataset.name, dataset.chosen_sample_ID_list)


class DatasetTree(QTreeWidget):
    def __init__(self, parent=None):
        super(DatasetTree, self).__init__(parent)

        self.parent = parent
        self.setMinimumHeight(150)
        self.setStyleSheet('QTreeWidget{font-size:10pt;}')
        self.properties = ['Sample_ID', 'Age', 'Sex', 'Vertebral_level', 'F_exp(N)', 'Disp_exp(mm)',
                           'Tumour type', 'Primary tumour']
        self.setColumnCount(9)
        self.setHeaderLabels(['Source', 'ID', 'Age', 'Sex', 'Vertebral Level',
                                          'Exp. failure load (N)', 'Exp. failure disp (mm)', 'Tumour type',
                                          'Primary tumour'])
        self.setColumnWidth(0, 200)
        self.setColumnWidth(1, 80)
        self.setColumnWidth(2, 80)
        self.setColumnWidth(3, 80)
        self.setColumnWidth(4, 100)
        self.setColumnWidth(5, 150)
        self.setColumnWidth(6, 150)
        self.setColumnWidth(7, 150)
        self.setColumnWidth(8, 150)
        # self.fill_tree_dataset()

    def fill(self):
        # Get info on datasets
        self.datasets = read_dataset_info(self.parent.parent.datasets_file_path)
        self.clear()

        self.dataset_tree_item_list = []
        index = 0
        for dataset in self.datasets:
            item_tree = DatasetQTreeWidgetItem(self, dataset, index)
            self.dataset_tree_item_list.append(item_tree)
            index += 1

        self.last_tab_index = 0


class DatasetQTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent, dataset, index):
        self.parent = parent
        self.dataset = dataset
        super(DatasetQTreeWidgetItem, self).__init__(self.parent)
        self.setExpanded(True)

        self.index = index
        #self.obj = self.object_list[self.index]
        self.setText(0, self.dataset.get_name())
        self.setText(1, 'N = ' + str(self.dataset.get_size()))
        age_list = self.dataset.get_property_list('Age')
        self.setText(2, "%.1f" % np.mean(age_list) + ' ± ' + "%.1f" % np.std(age_list))
        sex_list = self.dataset.get_property_list('Sex')
        male_number = len([x for x in sex_list if x == 'M'])
        female_number = len([x for x in sex_list if x == 'F'])
        self.setText(3, "{}F / {}M".format(female_number, male_number))

        fexp_list = [x for x in self.dataset.get_property_list('F_exp(N)') if not math.isnan(x)]
        try:
            self.setText(5, "%d" % np.mean(fexp_list) + ' ± ' + "%d" % np.std(fexp_list))
        except ValueError:
            pass

        dexp_list = self.dataset.get_property_list('Disp_exp(mm)')
        self.setText(6, "%.1f" % np.mean(dexp_list) + ' ± ' + "%.1f" % np.std(dexp_list))

        self.setFlags(self.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        self.setCheckState(0, Qt.Checked)
        self.samples_tree_list = []
        index_sample = 0
        for sample_infos in self.dataset.get_samples_infos(self.parent.properties):
            sample_tree = SampleQTreeWidgetItem(self, sample_infos, index_sample)
            self.samples_tree_list.append(sample_tree)
            index_sample += 1

    def get_index(self):
        return self.index

    def get_parent(self):
        return self.parent


class SampleQTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent, sample_infos, index_sample):
        self.parent = parent
        self.samples_infos = sample_infos
        self.index_sample = index_sample
        self.index_obj = self.parent.get_index()
        self.parent_tree = self.parent.parent
        super(SampleQTreeWidgetItem, self).__init__(self.parent)

        self.setFlags(self.flags() | Qt.ItemIsUserCheckable)
        self.setCheckState(0, Qt.Checked)

        for i in range(len(self.samples_infos)):
            self.setText(i+1, str(self.samples_infos[i]))
