from PyQt5.QtGui import QFont, QColor, QBrush, QIcon
from PyQt5.QtCore import QDateTime, Qt, QTimer, QMargins, QSize
from PyQt5.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QFileDialog, QFrame, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QMainWindow, QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTableWidgetItem, QTabWidget, QTextEdit,
        QTreeWidget, QTreeWidgetItem, QScrollArea, QSlider, QSplitter, QStackedLayout, QStatusBar, QToolButton,
        QVBoxLayout, QWidget)

from Material_assignment.module.Reader.Mechanical_law_reader import global_list_EX, global_list_EY, global_list_EZ, \
                                            global_list_PM, global_list_YS,\
                                            global_list_NUXY, global_list_NUXZ, global_list_NUYZ,\
                                            global_list_GXY, global_list_GXZ, global_list_GYZ

#from MekAnos.Material_assignment.module.Converters.ModifyMechanicalLaw import create_new_mekamesh_from_mekamesh

from Interface.CustomClasses import CustomQToolButton

from Interface.QueueManagement.Waiting_list import Waiting_list


class Simulation_tab(QWidget):
    def __init__(self, parent):
        super(Simulation_tab, self).__init__(parent)

        self.parent = parent
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)

        self.create_material_widget()
        self.create_constitutive_law_groupbox()
        self.create_analysis_groupbox()