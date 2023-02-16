from PyQt5.QtGui import QFont, QColor, QBrush, QIcon
from PyQt5.QtCore import QDateTime, Qt, QTimer, QMargins, QSize
from PyQt5.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QFileDialog, QFrame, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QMainWindow, QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTableWidgetItem, QTabWidget, QTextEdit,
        QTreeWidget, QTreeWidgetItem, QScrollArea, QSlider, QSplitter, QStackedLayout, QStatusBar, QToolButton,
        QVBoxLayout, QWidget)

from module.Reader.Mechanical_law_reader import global_list_EX, global_list_EY, global_list_EZ, \
                                            global_list_PM, global_list_YS,\
                                            global_list_NUXY, global_list_NUXZ, global_list_NUYZ,\
                                            global_list_GXY, global_list_GXZ, global_list_GYZ

from module.Converters.ModifyMechanicalLaw import create_new_mekamesh_from_mekamesh


class WindowModifyMekamesh(QDialog):
    def __init__(self, parent, mesh_list):
        super(WindowModifyMekamesh, self).__init__(parent)

        self.parentWindow = parent
        self.selectedMeshesList = mesh_list
        self.originalPalette = QApplication.palette()
        self.setWindowTitle("Modify mechanical law")
        self.styleName = 'Fusion'
        QApplication.setStyle(QStyleFactory.create(self.styleName))
        QApplication.setPalette(self.originalPalette)

        self.setStyleSheet('QWidget{font-size:11pt;}')

        # second page
        self.second_page = QWidget()
        self.second_pageLayout = QVBoxLayout()
        self.second_page.setLayout(self.second_pageLayout)

        self.materialStepWidget = QWidget()
        self.materialStepLayout = QHBoxLayout()
        self.materialStepWidget.setLayout(self.materialStepLayout)
        self.materialStepLabel = QLabel('Number of materials : ')
        self.materialStepEdit = QLineEdit()
        self.materialStepEdit.setText('100')
        self.materialStepSlider = QSlider(Qt.Horizontal, self)
        self.materialStepSlider.setGeometry(10, 10, 300, 40)
        self.materialStepSlider.setMinimum(1)
        self.materialStepSlider.setMaximum(1000)
        self.materialStepSlider.setValue(100)
        self.materialStepSlider.valueChanged.connect(self.sliderValueChanged)
        self.materialStepEdit.textChanged.connect(self.textValueChanged)
        self.materialStepLayout.addWidget(self.materialStepLabel)
        self.materialStepLayout.addWidget(self.materialStepEdit)
        self.materialStepLayout.addWidget(self.materialStepSlider)
        self.materialStepLayout.addStretch()

        self.materialStepApproxWidget = QWidget()
        self.materialStepApproxLayout = QHBoxLayout()
        self.materialStepApproxWidget.setLayout(self.materialStepApproxLayout)
        self.materialStepApproxLabel = QLabel('Material step approximation = ')
        self.materialStepApproxComboBox = QComboBox()
        self.materialStepApproxComboBox.addItems(['- Choose bound condition -', 'inferior bound', 'middle bound', 'superior bound'])
        self.materialStepApproxComboBox.setCurrentIndex(2)
        self.materialStepApproxComboBox.currentIndexChanged.connect(self.second_page_reaction)
        self.materialStepApproxLayout.addWidget(self.materialStepApproxLabel)
        self.materialStepApproxLayout.addWidget(self.materialStepApproxComboBox)
        self.materialStepApproxLayout.addStretch()

        self.materialSymmetryWidget = QWidget()
        self.materialSymmetryLayout = QHBoxLayout()
        self.materialSymmetryWidget.setLayout(self.materialSymmetryLayout)
        self.materialSymmetryLabel = QLabel('Material Symmetry :')
        self.materialSymmetryComboBox = QComboBox()
        self.materialSymmetryComboBox.addItems(['- Choose material symmetry -', 'isotropic', 'orthotropic'])
        self.materialSymmetryComboBox.setCurrentIndex(1)
        self.materialSymmetryComboBox.currentIndexChanged.connect(self.second_page_reaction)
        self.materialSymmetryLayout.addWidget(self.materialSymmetryLabel)
        self.materialSymmetryLayout.addWidget(self.materialSymmetryComboBox)
        self.materialSymmetryLayout.addStretch()

        self.elasticModelWidget = QWidget()
        self.elasticModelLayout = QHBoxLayout()
        self.elasticModelWidget.setLayout(self.elasticModelLayout)
        self.elasticModelLabel = QLabel('Elastic mechanical properties :')
        self.elasticModelComboBox = QComboBox()
        self.elasticModelComboBox.addItems(['- Choose elastic model -', 'Keller et al. (1994)', 'Kopperdahl et al. (2002)'])
        self.elasticModelComboBox.currentIndexChanged.connect(self.second_page_reaction)
        self.elasticModelLayout.addWidget(self.elasticModelLabel)
        self.elasticModelLayout.addWidget(self.elasticModelComboBox)
        self.elasticModelLayout.addStretch()

        self.plasticModelWidget = QWidget()
        self.plasticModelLayout = QHBoxLayout()
        self.plasticModelWidget.setLayout(self.plasticModelLayout)
        self.plasticModelLabel = QLabel('Elastic mechanical properties :')
        self.plasticModelComboBox = QComboBox()
        self.plasticModelComboBox.addItems(
            ['- Choose plastic model -', 'None', 'Perfectly plastic', 'Plastic (choose plastic modulus)'])
        self.plasticModelComboBox.currentIndexChanged.connect(self.second_page_reaction)
        self.plasticModelLayout.addWidget(self.plasticModelLabel)
        self.plasticModelLayout.addWidget(self.plasticModelComboBox)
        self.plasticModelLayout.addStretch()

        self.second_pageLayout.addWidget(self.materialStepWidget)
        self.second_pageLayout.addWidget(self.materialStepApproxWidget)
        self.second_pageLayout.addWidget(self.materialSymmetryWidget)
        self.second_pageLayout.addWidget(self.elasticModelWidget)
        self.second_pageLayout.addWidget(self.plasticModelWidget)

        # window to choose mechanical laws
        self.mechanicalWindow = QWidget()
        self.mechanicalWindowLayout = QVBoxLayout()
        self.mechanicalWindowLayout.setSpacing(0)
        self.mechanicalWindowLayout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.mechanicalWindow.setLayout(self.mechanicalWindowLayout)
        # Header
        self.mechanicalWindowHeaderWidget = QWidget()
        self.mechanicalWindowHeaderLayout = QHBoxLayout()
        self.mechanicalWindowHeaderWidget.setLayout(self.mechanicalWindowHeaderLayout)
        self.mechanicalWindowTitle = QLabel("Choose new Mechanical laws")  # label for Header
        self.mechanicalWindowHeaderLayout.addWidget(self.mechanicalWindowTitle)
        self.addFieldButton = CustomQToolButton('Add law', r'Images/add 2.svg', 16)
        self.addFieldButton.clicked.connect(self.addField)
        self.mechanicalWindowHeaderLayout.addWidget(self.addFieldButton)
        self.mechanicalWindowHeaderLayout.addStretch()
        # Scroll area for mechanical laws
        self.createMechanicalWindow()
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.mechanicalWindowTable)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setMinimumHeight(200)
        self.scroll.setMinimumWidth(600)
        self.mechanicalWindowLayout.addWidget(self.mechanicalWindowHeaderWidget)
        self.mechanicalWindowLayout.addWidget(self.scroll)
        self.mechanicalWindowLayout.addStretch()

        # buttons to cancel or accept -  stack 2
        self.cancelButton2 = QPushButton('Cancel')
        self.cancelButton2.clicked.connect(self.close)
        self.nextButton2 = QPushButton('Next >>')
        self.nextButton2.setDisabled(True)
        self.nextButton2.clicked.connect(self.next_page)
        self.downButtonsLayout2 = QHBoxLayout()
        self.downButtonsLayout2.addWidget(self.cancelButton2)
        self.downButtonsLayout2.addWidget(self.nextButton2)
        self.downButtonsWidget2 = QWidget()
        self.downButtonsWidget2.setLayout(self.downButtonsLayout2)

        # buttons to cancel or accept -  stack 3
        self.cancelButton3 = QPushButton('Cancel')
        self.cancelButton3.clicked.connect(self.close)
        self.createButton3 = QPushButton('Create Mekameshes')
        self.createButton3.clicked.connect(self.create_mekameshes)
        self.previousButton3 = QPushButton('<< Previous')
        self.previousButton3.clicked.connect(self.previous_page)
        self.downButtonsLayout3 = QHBoxLayout()
        self.downButtonsLayout3.addWidget(self.cancelButton3)
        self.downButtonsLayout3.addWidget(self.previousButton3)
        self.downButtonsLayout3.addWidget(self.createButton3)
        self.downButtonsWidget3 = QWidget()
        self.downButtonsWidget3.setLayout(self.downButtonsLayout3)

        # stacked layout for upper part
        self.upperWidget = QWidget()
        self.upperlayout = QStackedLayout()
        self.upperlayout.addWidget(self.second_page)
        self.upperlayout.addWidget(self.mechanicalWindow)
        self.upperWidget.setLayout(self.upperlayout)

        # stacked layout for bottom part
        self.bottomWidget = QWidget()
        self.bottomlayout = QStackedLayout()
        self.bottomlayout.addWidget(self.downButtonsWidget2)
        self.bottomlayout.addWidget(self.downButtonsWidget3)
        self.bottomWidget.setLayout(self.bottomlayout)

        # main layout
        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.upperWidget)
        self.mainLayout.addWidget(self.bottomWidget)

    def sliderValueChanged(self, value):
        self.materialStepEdit.setText(str(value))
        self.second_page_reaction()

    def textValueChanged(self):
        try:
            self.materialStepSlider.setValue(int(self.materialStepEdit.text()))
        except ValueError:
            self.materialStepSlider.setValue(0)
        self.second_page_reaction()

    def second_page_reaction(self):
        if len(self.materialStepEdit.text()) == 0\
        or self.elasticModelComboBox.currentIndex() == 0\
        or self.materialSymmetryComboBox.currentIndex() == 0\
        or self.materialStepApproxComboBox.currentIndex() == 0:
            self.nextButton2.setDisabled(True)
        else:
            self.nextButton2.setDisabled(False)
        try:
            self.materialStep = int(self.materialStepEdit.text())
        except ValueError:
            self.nextButton2.setDisabled(True)

        if self.materialStepApproxComboBox.currentIndex() == 1:
            self.approximation = 'inf'
        elif self.materialStepApproxComboBox.currentIndex() == 2:
            self.approximation = 'mid'
        elif self.materialStepApproxComboBox.currentIndex() == 3:
            self.approximation = 'sup'

        if self.materialSymmetryComboBox.currentIndex() == 1:
            self.symmetry = 'isotropic'
        elif self.materialSymmetryComboBox.currentIndex() == 2:
            self.symmetry = 'orthotropic'

        if self.elasticModelComboBox.currentIndex() == 2 and self.symmetry == 'orthotropic':
            # clear layoutLaw
            self.propertyFieldList = []
            for i in reversed(range(self.layoutlaw.count())):
                try:
                    self.layoutlaw.itemAt(i).widget().setParent(None)
                except AttributeError:
                    pass
            self.addField(1, 6)
            self.addField(2, 6)
            self.addField(3, 5)
            self.addField(4, 3)
            self.addField(5, 4)
            self.addField(6, 4)
            self.addField(7, 2)
            self.addField(8, 2)
            self.addField(9, 2)
            self.addField(10, 2)
            self.addField(11, 2)
            self.config = 'Kopperdahl2002-EPP-ortho'

        elif self.elasticModelComboBox.currentIndex() == 2 and self.symmetry == 'isotropic':
            # clear layoutLaw
            self.propertyFieldList = []
            for i in reversed(range(self.layoutlaw.count())):
                try:
                    self.layoutlaw.itemAt(i).widget().setParent(None)
                except AttributeError:
                    pass
            self.addField(1, 5)
            self.addField(4, 3)
            self.addField(10, 2)
            self.addField(11, 2)
            self.config = 'Kopperdahl2002-EPP-iso'

        elif self.elasticModelComboBox.currentIndex() == 1 and self.symmetry == 'isotropic':
            # clear layoutLaw
            self.propertyFieldList = []
            for i in reversed(range(self.layoutlaw.count())):
                try:
                    self.layoutlaw.itemAt(i).widget().setParent(None)
                except AttributeError:
                    pass
            self.addField(1, 2)
            self.addField(4, 2)
            self.config = 'Keller1998-EL-iso'


    def createMechanicalWindow(self):
        self.mechanicalLawList = []
        self.chosenPropertyListIndex = set({})
        self.propertyFieldList = []
        self.propertyList = ['EX', 'EY', 'EZ', 'NUXY', 'NUYZ', 'NUXZ', 'GXY', 'GYZ', 'GXZ', 'Yield strength',
                             'Plastic modulus']

        self.mechanicalWindowTable = QWidget()
        self.layoutlaw = QVBoxLayout()
        self.layoutlaw.setSpacing(0)
        self.setContentsMargins(QMargins(0, 0, 0, 0))
        self.mechanicalWindowTable.setLayout(self.layoutlaw)
        self.layoutlaw.addStretch()
        self.addField()

    def addField(self, property_index=None, law_index=None):
        index = len(self.propertyFieldList)
        if property_index and law_index:
            new_field = PropertyField(self, index, property_index, law_index)
        else:
            new_field = PropertyField(self, index)
        # add a new field for choosing a mechanical property
        self.layoutlaw.insertWidget(index, new_field)
        self.propertyFieldList.append(new_field)


    def next_page(self):
        index = self.upperlayout.currentIndex()
        self.upperlayout.setCurrentIndex(index + 1)
        self.bottomlayout.setCurrentIndex(index + 1)

    def previous_page(self):
        index = self.upperlayout.currentIndex()
        self.upperlayout.setCurrentIndex(index - 1)
        self.bottomlayout.setCurrentIndex(index - 1)

    def get_property_list(self):
        return self.propertyList

    def get_chosen_property_list(self):
        return self.chosenPropertyListIndex

    def get_mechanical_law_list(self):
        return self.mechanicalLawList

    def update_properties(self, index):
        count = 0
        for propertyField in self.propertyFieldList:
            if count != index:
                propertyField.update()
            index += 1

    def create_mekameshes(self):
        for propertyField in self.propertyFieldList:
            if propertyField.get_chosen_law():
                self.mechanicalLawList.append(propertyField.get_chosen_law())

        # TODO material step type widget
        self.materialStepType = "material number - equal step"

        for mekamesh in self.selectedMeshesList:
            mekamesh = create_new_mekamesh_from_mekamesh(mekamesh,
                                                     self.config,
                                                     self.mechanicalLawList,
                                                     self.materialStepType, self.materialStep, self.approximation)
            mekamesh.unread()
            mekamesh.read()
        self.parentWindow.update_mesh()
        '''except (ValueError, TypeError, AttributeError) as e:
            self.parentWindow.showMessage(True, e.__str__())
        else:'''
        self.close()

    def remove_field(self, index):
        self.propertyFieldList.pop(index)
        self.layoutlaw.itemAt(index).widget().deleteLater()
        for i in range(len(self.propertyFieldList)):
            self.propertyFieldList[i].update_index(i)


class PropertyField(QWidget):
    def __init__(self, parent, index, property_index=None, law_index=None):
        super(PropertyField, self).__init__(parent)

        self.parent = parent
        self.index = index

        self.setStyleSheet('QWidget{font-size:11pt;}')
        self.setMaximumHeight(65)

        self.propertyList = self.parent.get_property_list()
        self.chosenIndexList = self.parent.get_chosen_property_list()

        # Label
        self.labelWidget = QWidget()
        self.labelLayout = QHBoxLayout()
        self.labelLayout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.labelWidget.setLayout(self.labelLayout)
        #self.lineTitle = QLabel('Mechanical Law {}'.format(self.index + 1))
        self.removeButton = CustomQToolButton('', r'Images/remove.svg', 16)
        self.removeButton.clicked.connect(self.remove_field)
        self.labelLayout.addWidget(self.removeButton)
        #self.labelLayout.addWidget(self.lineTitle)
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
        self.comboBoxLaw = QComboBox()
        self.comboBoxLaw.addItem('- Choose a law -')
        self.comboBoxLaw.addItem('Other law (enter manually)')
        self.comboBoxLaw.currentIndexChanged.connect(self.law_changed)
        self.comboBoxLaw.setDisabled(True)

        # Prevent choosing a property already chosen
        for chosen_index in self.chosenIndexList:
            self.comboBoxProperty.model().item(chosen_index).setEnabled(False)

        # add to layout
        # widget for law creation
        self.widgetLawCreation = QWidget()
        self.layoutLawCreation = QHBoxLayout()
        self.layoutLawCreation.setSpacing(0)
        self.layoutLawCreation.setContentsMargins(QMargins(0, 0, 0, 0))
        self.widgetLawCreation.setLayout(self.layoutLawCreation)
        #self.widgetLawCreation.hide()
        self.labelLawPropertyName = QLabel('Property')
        self.labelLawCreation1 = QLabel(' = ')
        self.labelLawCoeff_a = QLineEdit()
        self.labelLawCoeff_a.setPlaceholderText('a')
        self.labelLawCreation2 = QLabel(' + ')
        self.labelLawCoeff_b = QLineEdit()
        self.labelLawCoeff_b.setPlaceholderText('b')
        self.labelLawCreation3 = QLabel(' * density ^ ')
        self.labelLawCoeff_c = QLineEdit()
        self.labelLawCoeff_c.setPlaceholderText('c')
        self.layoutLawCreation.addWidget(self.labelLawPropertyName)
        self.layoutLawCreation.addWidget(self.labelLawCreation1)
        self.layoutLawCreation.addWidget(self.labelLawCoeff_a)
        self.layoutLawCreation.addWidget(self.labelLawCreation2)
        self.layoutLawCreation.addWidget(self.labelLawCoeff_b)
        self.layoutLawCreation.addWidget(self.labelLawCreation3)
        self.layoutLawCreation.addWidget(self.labelLawCoeff_c)
        # button to create new law
        self.newLawButton = QPushButton('Create new law')
        self.layoutLawCreation.addWidget(self.newLawButton)
        self.newLawButton.clicked.connect(self.create_new_law)
        self.newLawButton.hide()

        # widget for law
        self.widgetLaw = QWidget()
        self.layoutLaw = QVBoxLayout()
        self.layoutLaw.setSpacing(0)
        self.widgetLaw.setLayout(self.layoutLaw)
        self.layoutLaw.addWidget(self.comboBoxLaw)
        self.layoutLaw.addWidget(self.widgetLawCreation)
        # widget for choosing
        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.layout.addWidget(self.labelWidget)
        self.layout.addWidget(self.firstComboWidget)
        self.layout.addWidget(self.widgetLaw)
        self.setLayout(self.layout)
        self.layout.addStretch()

        if property_index:
            self.comboBoxProperty.setCurrentIndex(property_index)
        if law_index:
            self.comboBoxLaw.setCurrentIndex(law_index)

    def remove_field(self):
        self.comboBoxProperty.setCurrentIndex(0)
        self.parent.remove_field(self.index)

    def property_changed(self):
        self.comboBoxLaw.setCurrentIndex(0)
        # previous index to put back in choose-able list
        if self.currentIndexChosen != 0:
            self.chosenIndexList.remove(self.currentIndexChosen)
            for i in range(2, self.comboBoxLaw.count()):
                self.comboBoxLaw.removeItem(i)
        self.currentIndexChosen = self.comboBoxProperty.currentIndex()
        if self.currentIndexChosen != 0:
            self.chosenIndexList.add(self.currentIndexChosen)
            self.chosenProperty = self.comboBoxProperty.itemText(self.currentIndexChosen)
            self.comboBoxLaw.setDisabled(False)
            if self.chosenProperty == 'EX':
                self.comboBoxLaw.addItems([law.get_law_name() for law in global_list_EX])
                self.law_list = global_list_EX
            if self.chosenProperty == 'EY':
                self.comboBoxLaw.addItems([law.get_law_name() for law in global_list_EY])
                self.law_list = global_list_EY
            if self.chosenProperty == 'EZ':
                self.comboBoxLaw.addItems([law.get_law_name() for law in global_list_EZ])
                self.law_list = global_list_EZ

            if self.chosenProperty == 'NUXY':
                self.comboBoxLaw.addItems([law.get_law_name() for law in global_list_NUXY])
                self.law_list = global_list_NUXY
            if self.chosenProperty == 'NUYZ':
                self.comboBoxLaw.addItems([law.get_law_name() for law in global_list_NUYZ])
                self.law_list = global_list_NUYZ
            if self.chosenProperty == 'NUXZ':
                self.comboBoxLaw.addItems([law.get_law_name() for law in global_list_NUXZ])
                self.law_list = global_list_NUXZ

            if self.chosenProperty == 'GXY':
                self.comboBoxLaw.addItems([law.get_law_name() for law in global_list_GXY])
                self.law_list = global_list_GXY
            if self.chosenProperty == 'GYZ':
                self.comboBoxLaw.addItems([law.get_law_name() for law in global_list_GYZ])
                self.law_list = global_list_GYZ
            if self.chosenProperty == 'GXZ':
                self.comboBoxLaw.addItems([law.get_law_name() for law in global_list_GXZ])
                self.law_list = global_list_GXZ

            if self.chosenProperty == 'Yield strength':
                self.comboBoxLaw.addItems([law.get_law_name() for law in global_list_YS])
                self.law_list = global_list_YS
            if self.chosenProperty == 'Plastic modulus':
                self.comboBoxLaw.addItems([law.get_law_name() for law in global_list_PM])
                self.law_list = global_list_PM
        else:
            self.comboBoxLaw.setDisabled(True)
        self.parent.update_properties(self.index)

    def law_changed(self):
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


class CustomQToolButton(QToolButton):
    def __init__(self, text, icon_path, size=60, parent=None):
        super(CustomQToolButton, self).__init__(parent)

        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setStyleSheet('QToolButton{border: none;}')
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(size, size))
        if text:
            self.setText(text)
            self.setFixedWidth(size*5/3)
            self.setFixedHeight(size*5/3)

        else:
            self.setFixedHeight(size*5/3)