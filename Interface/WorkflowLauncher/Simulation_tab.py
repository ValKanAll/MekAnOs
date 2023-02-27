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

        # window to choose loading parameters
        # window to choose mechanical laws
        self.loadingParametersWindow = QWidget()
        self.loadingParametersWindowLayout = QVBoxLayout()
        self.loadingParametersWindow.setLayout(self.loadingParametersWindowLayout)
        # Header
        self.loadingParametersWindowHeaderWidget = QWidget()
        self.loadingParametersWindowHeaderLayout = QHBoxLayout()
        self.loadingParametersWindowHeaderWidget.setLayout(self.loadingParametersWindowHeaderLayout)
        self.loadingParametersWindowTitle = QLabel("Choose loading parameters")  # label for Header
        self.loadingParametersWindowHeaderLayout.addWidget(self.loadingParametersWindowTitle)
        self.addFieldButton = QPushButton('Add constraint')  # button to add field
        self.addFieldButton.clicked.connect(self.addField)
        self.loadingParametersWindowHeaderLayout.addWidget(self.addFieldButton)
        self.loadingParametersWindowHeaderLayout.addStretch()

        # table of loadings
        self.createLoadingParametersWindow()
        self.createResultsParametersWindow()

        # possibility to scroll through displacement fields
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.loadingParametersWindowTable)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)

        self.loadingParametersWindowLayout.addWidget(self.loadingParametersWindowHeaderWidget)
        self.loadingParametersWindowLayout.addWidget(self.scroll)
        self.loadingParametersWindowLayout.addStretch()

        # main layout
        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.loadingParametersWindow)
        self.mainLayout.addWidget(self.ResultsParametersWindow)

    def createLoadingParametersWindow(self):
        self.loadingParametersWindowTable = QWidget()
        self.constraintList = []
        self.constraintFieldList = []

        self.layoutConstraint = QVBoxLayout()
        self.loadingParametersWindowTable.setLayout(self.layoutConstraint)
        self.addField()

    def createResultsParametersWindow(self):
        self.ResultsParametersWindow = QWidget()
        self.ResultsParametersLayout = QVBoxLayout()
        self.ResultsParametersWindow.setLayout(self.ResultsParametersLayout)
        self.ResultsParametersLabel = QLabel('Choose results')
        self.ResultsCheckBoxWidget = QFrame()
        self.ResultsCheckBoxLayout = QHBoxLayout()
        self.ResultsCheckBoxWidget.setLayout(self.ResultsCheckBoxLayout)
        self.ResultsCheckBoxWidget.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.ResultsParametersLayout.addWidget(self.ResultsParametersLabel)
        self.ResultsParametersLayout.addWidget(self.ResultsCheckBoxWidget)
        self.ResultsParametersLayout.addStretch()

        # strain check layout
        self.ResultsStrainWidget = QWidget()
        self.ResultsStrainLayout = QVBoxLayout()
        self.ResultsStrainWidget.setLayout(self.ResultsStrainLayout)
        self.ResultsStrainLabel = QLabel("Strain:")
        self.elasticStrainCheckBox = QCheckBox('equivalent elastic strain')
        self.plasticStrainCheckBox = QCheckBox('equivalent plastic strain')
        self.totalStrainCheckBox = QCheckBox('total strain')
        self.ResultsStrainLayout.addWidget(self.ResultsStrainLabel)
        self.ResultsStrainLayout.addWidget(self.elasticStrainCheckBox)
        self.ResultsStrainLayout.addWidget(self.plasticStrainCheckBox)
        self.ResultsStrainLayout.addWidget(self.totalStrainCheckBox)

        # stress check layout
        self.ResultsStressWidget = QWidget()
        self.ResultsStressLayout = QVBoxLayout()
        self.ResultsStressWidget.setLayout(self.ResultsStressLayout)
        self.ResultsStressLabel = QLabel("Stress:")
        self.elasticStressCheckBox = QCheckBox('equivalent elastic stress (Von-Mises)')
        self.principalVectorStressCheckBox = QCheckBox('principal vector stress')
        self.ResultsStressLayout.addWidget(self.ResultsStressLabel)
        self.ResultsStressLayout.addWidget(self.elasticStressCheckBox)
        self.ResultsStressLayout.addWidget(self.principalVectorStressCheckBox)

        # other check layout
        self.ResultsOtherWidget = QWidget()
        self.ResultsOtherLayout = QVBoxLayout()
        self.ResultsOtherWidget.setLayout(self.ResultsOtherLayout)
        self.ResultsOtherLabel = QLabel("Other:")
        self.reactionCheckBox = QCheckBox('reaction force')
        self.volumeCheckBox = QCheckBox('elemental volume')
        self.totalDeformationCheckBox = QCheckBox('total deformation')
        self.zDeformationCheckBox = QCheckBox('Z directional deformation')
        self.ResultsOtherLayout.addWidget(self.ResultsOtherLabel)
        self.ResultsOtherLayout.addWidget(self.reactionCheckBox)
        self.ResultsOtherLayout.addWidget(self.volumeCheckBox)
        self.ResultsOtherLayout.addWidget(self.totalDeformationCheckBox)
        self.ResultsOtherLayout.addWidget(self.zDeformationCheckBox)

        self.ResultsCheckBoxLayout.addWidget(self.ResultsStrainWidget)
        self.ResultsCheckBoxLayout.addWidget(self.ResultsStressWidget)
        self.ResultsCheckBoxLayout.addWidget(self.ResultsOtherWidget)
        #self.ResultsCheckBoxLayout.addStretch()

    def addField(self):
        index = len(self.constraintFieldList)
        new_field = ConstraintField(self, index)
        # add a new field  for choosing a mechanical property
        self.layoutConstraint.addWidget(new_field)
        #self.layoutConstraint.addStretch()
        self.constraintFieldList.append(new_field)

    def create_simulation_script(self):
        '''# Create result list
        result_list = []
        if self.reactionCheckBox.checkState():
            result_list.append(Result('reaction_force'))
        if self.volumeCheckBox.checkState():
            result_list.append(Result('volume'))
        if self.totalDeformationCheckBox.checkState():
            result_list.append(Result('total_defomation'))
        if self.zDeformationCheckBox.checkState():
            result_list.append(Result('z_directional_defomation'))

        if self.elasticStressCheckBox.checkState():
            result_list.append(Result('equivalent_elastic_stress'))
        if self.principalVectorStressCheckBox.checkState():
            result_list.append(Result('principal_vector_stress'))

        if self.elasticStrainCheckBox.checkState():
            result_list.append(Result('equivalent_elastic_strain'))
        if self.plasticStrainCheckBox.checkState():
            result_list.append(Result('equivalent_plastic_strain'))
        if self.totalStrainCheckBox.checkState():
            result_list.append(Result('total_Strain'))'''

        # Create simulation for each selected mekamesh
        for field in self.constraintFieldList:
            constraint = field.get_constraint()
            if constraint:
                if field.get_constraint()[0] == 'Imposed Displacement':
                    if field.get_constraint()[1] == '% height':
                        print('translation', '{} %height'.format(str(field.get_constraint()[1])))
                    else:
                        print('translation', field.get_constraint()[1], field.get_constraint()[2])
                elif field.get_constraint()[0] == 'Imposed Load':
                    print('force', field.get_constraint()[1], field.get_constraint()[2])

    def remove_field(self, index):
        self.constraintFieldList.pop(index)
        self.layoutConstraint.itemAt(index).widget().deleteLater()
        for i in range(len(self.constraintFieldList)):
            self.constraintFieldList[i].update_index(i)


class ConstraintField(QWidget):
    def __init__(self, parent, index):
        super(ConstraintField, self).__init__(parent)

        self.parent = parent
        self.index = index

        # Label
        self.labelWidget = QWidget()
        self.labelLayout = QHBoxLayout()
        self.labelWidget.setLayout(self.labelLayout)
        self.lineTitle = QLabel('Constraint {}'.format(self.index + 1))
        self.removeButton = QPushButton('Remove law')
        self.removeButton.clicked.connect(self.remove_field)
        self.labelLayout.addWidget(self.lineTitle)
        self.labelLayout.addWidget(self.removeButton)
        self.labelLayout.addStretch()

        # First comboBox
        self.firstComboBoxWidget = QWidget()
        self.firstComboBoxLayout = QVBoxLayout()
        self.firstComboBoxWidget.setLayout(self.firstComboBoxLayout)
        self.comboBoxConstraint = QComboBox()
        self.comboBoxConstraint.addItems(['- Choose a constraint -', 'Imposed Load', 'Imposed Displacement'])
        self.comboBoxConstraint.currentIndexChanged.connect(self.constraint_changed)
        self.comboBoxConstraint.setCurrentIndex(0)
        self.firstComboBoxLayout.addWidget(self.comboBoxConstraint)
        self.firstComboBoxLayout.addStretch()

        # Second comboBox
        # Either disp or force
        # Choose displacement
        self.comboBoxDisplacement = QComboBox()
        self.comboBoxDisplacement.addItem('- Choose a displacement -')
        self.comboBoxDisplacement.addItems(['Enter manually', '1.9% height'])
        self.comboBoxDisplacement.currentIndexChanged.connect(self.displacement_changed)
        # Choose force
        self.comboBoxForce = QComboBox()
        self.comboBoxForce.addItem('- Choose a force -')
        self.comboBoxForce.addItems(['Enter manually'])
        self.comboBoxForce.currentIndexChanged.connect(self.force_changed)
        # Assembled in stacked layout for second combobox
        self.secondComboBoxWidget = QWidget()
        self.secondComboBoxStackedLayout = QStackedLayout()
        self.secondComboBoxWidget.setLayout(self.secondComboBoxStackedLayout)
        self.secondComboBoxStackedLayout.addWidget(self.comboBoxDisplacement)
        self.secondComboBoxStackedLayout.addWidget(self.comboBoxForce)

        # add to layout
        # widget for Constraint creation
        self.widgetConstraintCreation = QWidget()
        self.layoutConstraintCreation = QHBoxLayout()
        self.widgetConstraintCreation.setLayout(self.layoutConstraintCreation)
        self.widgetConstraintCreation.hide()
        self.labelConstraintName = QLabel('Constraint')
        self.labelConstraintCreation1 = QLabel(' = ')
        # Create vector of 3 line edit
        self.labelConstraintValueWidget = QWidget()
        self.labelConstraintValueLayout = QVBoxLayout()
        self.labelConstraintValueWidget.setLayout(self.labelConstraintValueLayout)
        self.valueXConstraint = QLineEdit()
        self.valueYConstraint = QLineEdit()
        self.valueZConstraint = QLineEdit()
        self.labelConstraintValueLayout.addWidget(self.valueXConstraint)
        self.labelConstraintValueLayout.addWidget(self.valueYConstraint)
        self.labelConstraintValueLayout.addWidget(self.valueZConstraint)
        self.labelConstraintUnit = QComboBox()
        self.labelConstraintUnit.addItems(['mm', '% height', 'N'])
        self.labelConstraintUnit.setCurrentIndex(0)
        self.layoutConstraintCreation.addWidget(self.labelConstraintName)
        self.layoutConstraintCreation.addWidget(self.labelConstraintCreation1)
        self.layoutConstraintCreation.addWidget(self.labelConstraintValueWidget)
        self.layoutConstraintCreation.addWidget(self.labelConstraintUnit)

        # widget for constraint
        self.widgetConstraint = QWidget()
        self.layoutConstraint = QVBoxLayout()
        self.widgetConstraint.setLayout(self.layoutConstraint)
        self.layoutConstraint.addWidget(self.secondComboBoxWidget)
        self.layoutConstraint.addWidget(self.widgetConstraintCreation)
        self.widgetConstraint.hide()
        # widget for choosing
        self.layoutChoose = QHBoxLayout()
        self.layoutChoose.addWidget(self.firstComboBoxWidget)
        self.layoutChoose.addWidget(self.widgetConstraint)
        self.widgetChoose = QWidget()
        self.widgetChoose.setLayout(self.layoutChoose)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.labelWidget)
        self.layout.addWidget(self.widgetChoose)
        self.setLayout(self.layout)
        self.layout.addStretch()

    def constraint_changed(self):
        if self.comboBoxConstraint.currentText() == 'Imposed Displacement':
            self.widgetConstraint.show()
            self.labelConstraintName.setText('Displacement')
            self.secondComboBoxStackedLayout.setCurrentIndex(0)
            self.labelConstraintUnit.model().item(0).setEnabled(True)
            self.labelConstraintUnit.model().item(1).setEnabled(True)
            self.labelConstraintUnit.model().item(2).setEnabled(False)
            self.labelConstraintUnit.setCurrentIndex(0)

        elif self.comboBoxConstraint.currentText() == 'Imposed Load':
            self.widgetConstraint.show()
            self.labelConstraintName.setText('Force')
            self.secondComboBoxStackedLayout.setCurrentIndex(1)
            self.labelConstraintUnit.model().item(0).setEnabled(False)
            self.labelConstraintUnit.model().item(1).setEnabled(False)
            self.labelConstraintUnit.model().item(2).setEnabled(True)
            self.labelConstraintUnit.setCurrentIndex(2)

        else:
            self.widgetConstraint.hide()

    def displacement_changed(self):
        if self.comboBoxDisplacement.currentText() == '1.9% height':
            self.valueXConstraint.setText('0')
            self.valueYConstraint.setText('0')
            self.valueZConstraint.setText('1.9')
            self.labelConstraintUnit.setCurrentIndex(1)
            self.widgetConstraintCreation.setDisabled(True)
            self.widgetConstraintCreation.show()
        elif self.comboBoxDisplacement.currentText() == 'Enter manually':
            self.widgetConstraintCreation.setDisabled(False)
            self.widgetConstraintCreation.show()
            self.valueXConstraint.setPlaceholderText('Disp_X')
            self.valueYConstraint.setPlaceholderText('Disp_Y')
            self.valueZConstraint.setPlaceholderText('Disp_Z')
            self.labelConstraintUnit.setCurrentIndex(0)
        else:
            self.widgetConstraintCreation.setDisabled(True)
            self.widgetConstraintCreation.hide()

    def force_changed(self):
        if self.comboBoxForce.currentText() == 'Enter manually':
            self.widgetConstraintCreation.setDisabled(False)
            self.widgetConstraintCreation.show()
            self.valueXConstraint.setPlaceholderText('Force_X')
            self.valueYConstraint.setPlaceholderText('Force_Y')
            self.valueZConstraint.setPlaceholderText('Force_Z')
        else:
            self.widgetConstraintCreation.setDisabled(True)
            self.widgetConstraintCreation.hide()

    def get_constraint(self):
        if self.comboBoxConstraint.currentText() == "Imposed Load":
            return ['Imposed Load', '', 'N']
        if self.comboBoxConstraint.currentText() == "Imposed Displacement" and\
                self.comboBoxDisplacement.currentText() == 'Experimental displacement':
            return ['Imposed Displacement', 'Experimental displacement', 'mm']
        else:
            return [self.comboBoxConstraint.currentText(),
                        [float(self.valueXConstraint.text()),
                         float(self.valueYConstraint.text()),
                         float(self.valueZConstraint.text())],
                    self.labelConstraintUnit.currentText()]

    def update_index(self, new_index):
        self.index = new_index
        self.lineTitle.setText('Constraint {}'.format(self.index + 1))

    def remove_field(self):
        self.parent.remove_field(self.index)