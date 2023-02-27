from PyQt5.QtCore import QDateTime, Qt, QTimer, QSize, QMargins, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QFileDialog, QFrame, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QMainWindow, QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTableWidgetItem, QTabWidget, QTextEdit,
        QTreeWidget, QTreeWidgetItem, QScrollArea, QSplitter, QStackedLayout, QTabWidget, QTabBar,
        QToolButton, QVBoxLayout, QWidget)
from PyQt5.QtGui import QIcon, QFont, QColor, QBrush

from Interface.QueueManagement.Waiting_list import Waiting_list
from Interface.CustomClasses import CustomQToolButton

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

        self.tab_widget = QTabWidget()
        self.mainLayout.addWidget(self.tab_widget)

        self.create_tables()
        #self.create_filter_tab()

        self.tab_widget.addTab(self.all_tab_widget, 'Waiting list')
        #self.tab_widget.addTab(self.filter_widget, 'Filter')
        self.tab_widget.addTab(self.in_progress_tab_widget, 'In progress')

        self.fill_table(self.all_table)

        def is_in_progress(action):
            if action[-1] == 'in_progress':
                return True

        self.fill_table(self.in_progress_table, is_in_progress)

    def create_filter_tab(self):
        self.filter_widget = QWidget()
        self.filter_layout = QVBoxLayout()
        self.filter_widget.setLayout(self.filter_layout)

        self.filter_scroll = QScrollArea(self)
        self.filter_scroll_layout = QVBoxLayout()
        self.filter_scroll.setLayout(self.filter_scroll_layout)

    def create_tables(self):
        self.all_tab_widget = QWidget()
        self.all_tab_layout = QVBoxLayout()
        self.all_tab_widget.setLayout(self.all_tab_layout)
        self.all_table = QTableWidget()
        self.all_table.setColumnCount(15)
        self.all_table.setHorizontalHeaderLabels(['Time', 'Action', 'Dataset', 'Sample', 'Segmentation', 'Mesh',
                                                  'Mesh analysis', 'Material step (MPa)', 'Min value material (MPa)',
                                                  'Constitutive laws', 'Mekamesh analysis'])
        self.all_table.setColumnWidth(0, 150)
        self.all_table.setColumnWidth(1, 100)
        self.all_table.setColumnWidth(2, 150)
        self.all_table.setColumnWidth(3, 100)
        self.all_table.setColumnWidth(4, 100)
        self.all_table.setColumnWidth(5, 100)
        self.all_table.setColumnWidth(6, 150)
        self.all_table.setColumnWidth(7, 120)
        self.all_table.setColumnWidth(8, 150)
        self.all_table.setColumnWidth(9, 300)
        self.all_table.setColumnWidth(10, 150)

        self.all_tab_layout.addWidget(self.all_table)

        self.in_progress_tab_widget = QWidget()
        self.in_progress_tab_layout = QVBoxLayout()
        self.in_progress_tab_widget.setLayout(self.in_progress_tab_layout)
        self.in_progress_table = QTableWidget()
        self.in_progress_table.setColumnCount(15)
        self.in_progress_table.setHorizontalHeaderLabels(['Time', 'Action', 'Dataset', 'Sample', 'Segmentation', 'Mesh',
                                                  'Mesh analysis', 'Material step (MPa)', 'Min value material (MPa)',
                                                  'Constitutive laws', 'Mekamesh analysis'])
        self.in_progress_table.setColumnWidth(0, 150)
        self.in_progress_table.setColumnWidth(1, 100)
        self.in_progress_table.setColumnWidth(2, 150)
        self.in_progress_table.setColumnWidth(3, 100)
        self.in_progress_table.setColumnWidth(4, 100)
        self.in_progress_table.setColumnWidth(5, 100)
        self.in_progress_table.setColumnWidth(6, 150)
        self.in_progress_table.setColumnWidth(7, 120)
        self.in_progress_table.setColumnWidth(8, 150)
        self.in_progress_table.setColumnWidth(9, 300)
        self.in_progress_table.setColumnWidth(10, 150)

        self.in_progress_tab_layout.addWidget(self.in_progress_table)

    def fill_table(self, table, criteria=lambda x: True):
        table.setRowCount(0)
        WL = Waiting_list()
        self.waiting_list = WL.safe_read()
        for action in self.waiting_list:
            if criteria(action):
                rowPosition = table.rowCount()
                table.insertRow(rowPosition)
                numRows = table.rowCount()
                index = 0
                if action[-1] == 'waiting':
                    color = "#f7d197"
                elif action[-1] == 'failed':
                    color = '#f7a597'
                elif action[-1] == 'done':
                    color = '#baf797'
                elif action[-1] == 'in_progress':
                    color = '#97e1f7'
                for info in action[:-1]:
                    table.setItem(numRows - 1, index, QTableWidgetItem(info))
                    table.item(numRows - 1, index).setBackground(QBrush(QColor(color)))
                    index += 1


class FilterField(QWidget):
    def __init__(self, parent, index):
        super(FilterField, self).__init__(parent)

        self.parent = parent
        self.index = index

        self.setStyleSheet('QWidget{font-size:10pt;}')
        self.setMaximumHeight(65)

        self.propertyList = self.parent.get_property_list()
        self.chosenIndexList = self.parent.get_chosen_property_list()

        # Label
        self.labelWidget = QWidget()
        self.labelLayout = QHBoxLayout()
        self.labelLayout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.labelWidget.setLayout(self.labelLayout)
        self.removeButton = CustomQToolButton('', r'Images/remove.svg', 16)
        self.removeButton.clicked.connect(self.remove_field)
        self.labelLayout.addWidget(self.removeButton)
        self.labelLayout.addStretch()
        # Choose property
        self.firstComboWidget = QWidget()
        self.firstComboLayout = QVBoxLayout()
        self.comboBoxProperty = QComboBox()
        self.comboBoxProperty.addItem('- Choose a property -')
        self.comboBoxProperty.addItems(self.propertyList)
        self.comboBoxProperty.currentIndexChanged.connect(self.property_changed)
        self.currentIndexChosen = 0
        self.comboBoxProperty.setCurrentIndex(0)
        self.firstComboWidget.setLayout(self.firstComboLayout)
        self.firstComboLayout.addWidget(self.comboBoxProperty)
        self.firstComboLayout.addStretch()
        # Choose law
        self.comboBoxOperation = QComboBox()
        self.comboBoxOperation.currentIndexChanged.connect(self.operation_changed)
        self.comboBoxOperation.setDisabled(True)

        # add to layout
        # widget for value
        self.widgetValue = QWidget()
        self.layoutValue = QHBoxLayout()
        self.layoutValue.setSpacing(0)
        self.layoutValue.setContentsMargins(QMargins(0, 0, 0, 0))
        self.widgetValue.setLayout(self.layoutValue)

        self.labelValue = QLineEdit()
        self.labelValue.setPlaceholderText('enter value')
        self.labelValue.textChanged.connect(self.value_changed)

        self.layoutValue.addWidget(self.labelValue)

        # widget for choosing
        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.layout.addWidget(self.labelWidget)
        self.layout.addWidget(self.firstComboWidget)
        self.layout.addWidget(self.widgetValue)
        self.setLayout(self.layout)
        self.layout.addStretch()

    def remove_field(self):
        self.comboBoxProperty.setCurrentIndex(0)
        self.parent.remove_field(self.index)

    def property_changed(self):
        self.comboBoxOperation.setCurrentIndex(0)
        self.currentIndexChosen = self.comboBoxProperty.currentIndex()
        if self.currentIndexChosen != 0:
            self.chosenProperty = self.comboBoxProperty.itemText(self.currentIndexChosen)
            self.comboBoxOperation.setDisabled(False)
            if self.chosenProperty in ['']:
                self.comboBoxOperation.clear()
                self.comboBoxOperation.addItems(['contains', '='])
            if self.chosenProperty in ['']:
                self.comboBoxOperation.clear()
                self.comboBoxOperation.addItems(['=', '<', '>', '<=', '>='])

        else:
            self.comboBoxOperation.setDisabled(True)
        self.parent.update_properties(self.index)

    def value_changed(self):
        # get chosen law
        lawIndex = self.comboBoxLaw.currentIndex()
        if lawIndex > 0:
            self.labelLawPropertyName.setText(self.chosenProperty)
            if lawIndex > 1:
                self.newLawButton.hide()
                self.chosenLawName = self.comboBoxLaw.itemText(lawIndex)
                # show law
                self.widgetLawCreation.show()
                for law in self.law_list:
                    if law.get_law_name() == self.chosenLawName:
                        self.chosenLaw = law
                        self.a, self.b, self.c = self.chosenLaw.get_coefficients()
                        self.labelLawCoeff_a.setText(str(self.a))
                        self.labelLawCoeff_b.setText(str(self.b))
                        self.labelLawCoeff_c.setText(str(self.c))
                        self.labelLawCoeff_a.setDisabled(True)
                        self.labelLawCoeff_b.setDisabled(True)
                        self.labelLawCoeff_c.setDisabled(True)

            if lawIndex == 1:
                self.labelLawCoeff_a.setDisabled(False)
                self.labelLawCoeff_b.setDisabled(False)
                self.labelLawCoeff_c.setDisabled(False)
                self.newLawButton.show()
                self.newLawButton.setDisabled(False)
                self.widgetLawCreation.show()

        else:
            self.labelLawCoeff_a.setDisabled(True)
            self.labelLawCoeff_b.setDisabled(True)
            self.labelLawCoeff_c.setDisabled(True)
            self.newLawButton.hide()
            self.widgetLawCreation.show()
            self.chosenLaw = None

    def update(self):
        for i in range(len(self.propertyList)-1):
            if i in self.chosenIndexList and i != self.currentIndexChosen:
                self.comboBoxProperty.model().item(i).setEnabled(False)
            else:
                self.comboBoxProperty.model().item(i).setEnabled(True)

    def update_index(self, new_index):
        self.index = new_index
        #self.lineTitle.setText('Mechanical Law {}'.format(self.index + 1))

    def get_chosen_law(self):
        return self.chosenLaw

    def create_new_law(self):
        pass





if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)  # for logos with good resolution
    window = QueueManagementWindow()
    window.show()
    app.exec_()