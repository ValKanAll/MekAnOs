from PyQt5.QtCore import Qt, QMargins
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QStyleFactory, QTableWidget, QTableWidgetItem, QScrollArea, QTabWidget,
                             QVBoxLayout, QWidget)
from PyQt5.QtGui import QFont, QColor, QBrush

from Waiting_list.Waiting_list import Waiting_list
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

        self.setMinimumSize(800, 500)

        self.properties = ['Time', 'Action', 'Dataset', 'Sample', 'Segmentation', 'Mesh',
                                                  'Mesh analysis', 'Material step (MPa)', 'Min value material (MPa)',
                                                  'Constitutive laws', 'Mekamesh analysis']


        # main layout
        self.mainLayout = QGridLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setLayout(self.mainLayout)

        self.tab_widget = QTabWidget()
        self.mainLayout.addWidget(self.tab_widget)

        self.create_tables()
        self.create_filter_tab()

        self.tab_widget.addTab(self.all_tab_widget, 'Waiting list')
        self.tab_widget.addTab(self.filter_widget, 'Filter')
        self.tab_widget.addTab(self.in_progress_tab_widget, 'In progress')

        self.fill_table(self.all_table)

        def is_in_progress(action):
            if action[-1] == 'in_progress':
                return True

        self.fill_table(self.in_progress_table, is_in_progress)

    def create_filter_tab(self):
        self.filter_widget = QWidget()
        self.filter_layout = QHBoxLayout()
        self.filter_widget.setLayout(self.filter_layout)

        self.filter_button = QPushButton('Filter')
        self.filter_button.clicked.connect(self.filter)

        self.filter_scroll = QScrollArea(self)
        self.filter_scroll_widget = QWidget()
        self.filter_scroll_layout = QVBoxLayout()
        self.filter_scroll_widget.setLayout(self.filter_scroll_layout)
        self.filter_scroll.setWidget(self.filter_scroll_widget)

        self.filter_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.filter_scroll.setWidgetResizable(True)
        self.filter_scroll.setMinimumHeight(200)
        self.filter_scroll.setMinimumWidth(500)

        self.filter_layout.addWidget(self.filter_scroll)
        self.filter_layout.addWidget(self.filter_button)

        self.filterFieldList = []

        self.addField()

        self.filter_scroll_layout.addStretch()

        self.addFieldButton = CustomQToolButton(None, r'Images/add 2.svg', 16)
        self.addFieldButton.clicked.connect(self.addField)
        self.filter_scroll_layout.addWidget(self.addFieldButton)

    def filter(self):
        self.criteriaList = []
        for filter_field in self.filterFieldList:
            self.criteriaList.append(filter_field.get_criteria())

        def global_criteria(action):
            for criteria in self.criteriaList:
                if not criteria(action):
                    return False
            else:
                return True
        if self.criteriaList == []:
            self.fill_table(self.all_table)
        else:
            self.fill_table(self.all_table, global_criteria)

    def addField(self):
        index = len(self.filterFieldList)
        new_field = FilterField(self, index)
        # add a new field for choosing a mechanical property
        self.filter_scroll_layout.insertWidget(index, new_field)
        self.filterFieldList.append(new_field)

    def remove_field(self, index):
        self.filterFieldList.pop(index)
        self.filter_scroll_layout.itemAt(index).widget().deleteLater()
        for i in range(len(self.filterFieldList)):
            self.filterFieldList[i].update_index(i)

    def create_tables(self):
        self.all_tab_widget = QWidget()
        self.all_tab_layout = QVBoxLayout()
        self.all_tab_widget.setLayout(self.all_tab_layout)
        self.all_table = QTableWidget()
        self.all_table.setColumnCount(15)
        font = QFont()
        font.setPointSize(10)
        self.all_table.setFont(font)
        self.all_table.setHorizontalHeaderLabels(self.properties)
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
        font = QFont()
        font.setPointSize(10)
        self.in_progress_table.setFont(font)
        self.in_progress_table.setColumnCount(15)
        self.in_progress_table.setHorizontalHeaderLabels(self.properties)
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
                table.setRowHeight(rowPosition, 16)
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

        self.filterList = self.parent.filterFieldList

        # Remove button

        self.removeButton = CustomQToolButton('', r'Images/remove.svg', 16)
        self.removeButton.clicked.connect(self.remove_field)

        # Choose property
        self.comboBoxProperty = QComboBox()
        self.comboBoxProperty.addItem('- Choose a property -')
        self.comboBoxProperty.addItems(self.parent.properties)
        self.comboBoxProperty.currentIndexChanged.connect(self.property_changed)
        # Choose law
        self.comboBoxOperation = QComboBox()
        self.comboBoxOperation.setMinimumWidth(200)
        self.comboBoxOperation.setDisabled(True)

        # add to layout
        # widget for value
        self.labelValue = QLineEdit()
        self.labelValue.setPlaceholderText('enter value')
        self.labelValue.setDisabled(True)

        # widget for choosing
        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.layout.addWidget(self.removeButton)
        self.layout.addWidget(self.comboBoxProperty)
        self.layout.addWidget(self.comboBoxOperation)
        self.layout.addWidget(self.labelValue)
        self.setLayout(self.layout)
        self.layout.addStretch()

    def remove_field(self):
        self.comboBoxProperty.setCurrentIndex(0)
        self.parent.remove_field(self.index)

    def property_changed(self):
        self.comboBoxOperation.setCurrentIndex(0)
        self.currentPropertyIndexChosen = self.comboBoxProperty.currentIndex()
        self.chosenProperty = self.comboBoxProperty.itemText(self.currentPropertyIndexChosen)
        if self.currentPropertyIndexChosen != 0:
            self.comboBoxOperation.setDisabled(False)
            self.labelValue.setDisabled(False)
            if self.currentPropertyIndexChosen in [1]:
                self.comboBoxOperation.clear()
                self.comboBoxOperation.addItems(['contains', '=', '<', '>', '<=', '>='])
            if self.currentPropertyIndexChosen in [8, 9]:
                self.comboBoxOperation.clear()
                self.comboBoxOperation.addItems(['=', '<', '>', '<=', '>='])
            else:
                self.comboBoxOperation.clear()
                self.comboBoxOperation.addItems(['contains', '='])

        else:
            self.comboBoxOperation.setDisabled(True)

    def update_index(self, new_index):
        self.index = new_index

    def get_criteria(self):
        self.currentPropertyIndexChosen = self.comboBoxProperty.currentIndex()
        self.chosenProperty = self.comboBoxProperty.itemText(self.currentPropertyIndexChosen)

        self.currentOperationIndexChosen = self.comboBoxOperation.currentIndex()
        self.chosenOperation = self.comboBoxOperation.itemText(self.currentOperationIndexChosen)

        self.chosenValue = self.labelValue.text()

        def criteria(action):
            if self.chosenOperation == 'contains':
                if self.chosenValue in action[self.currentPropertyIndexChosen-1]:
                    return True
                else:
                    return False
            elif self.chosenOperation == '=':
                if self.chosenValue == action[self.currentPropertyIndexChosen-1]:
                    return True
                else:
                    return False
            elif self.chosenOperation == '<':
                if self.chosenValue < action[self.currentPropertyIndexChosen-1]:
                    return True
                else:
                    return False

            elif self.chosenOperation == '<=':
                if self.chosenValue <= action[self.currentPropertyIndexChosen-1]:
                    return True
                else:
                    return False

            elif self.chosenOperation == '>':
                if self.chosenValue > action[self.currentPropertyIndexChosen-1]:
                    return True
                else:
                    return False

            elif self.chosenOperation == '>=':
                if self.chosenValue >= action[self.currentPropertyIndexChosen-1]:
                    return True
                else:
                    return False

        return criteria

    def create_new_law(self):
        pass





if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)  # for logos with good resolution
    window = QueueManagementWindow()
    window.show()
    app.exec_()