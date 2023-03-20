from PyQt5.QtCore import Qt, QMargins
from PyQt5.QtWidgets import (QCheckBox, QComboBox, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QScrollArea, QSlider, QVBoxLayout, QWidget)

from Reader.Mechanical_law_reader import global_list_EX, global_list_EY, global_list_EZ, \
                                            global_list_PM, global_list_YS,\
                                            global_list_NUXY, global_list_NUXZ, global_list_NUYZ,\
                                            global_list_GXY, global_list_GXZ, global_list_GYZ

#from MekAnos.Material_assignment.module.Converters.ModifyMechanicalLaw import set_config_meca_for_mekamesh

from Interface.CustomClasses import CustomQToolButton

from Waiting_list.Waiting_list import Waiting_list


class Mekamesh_tab(QWidget):
    def __init__(self, parent):
        super(Mekamesh_tab, self).__init__(parent)

        self.parent = parent
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)

        self.create_material_widget()
        self.create_constitutive_law_groupbox()
        self.create_analysis_groupbox()
        self.mechanical_laws_widget = MechanicalLawsWidget(self)

        self.add_mat_attrib_to_queue_button = QPushButton('Add Material attribution to queue (QCTMA)')
        self.add_mat_attrib_to_queue_button.setDisabled(True)
        self.add_mat_attrib_to_queue_button.clicked.connect(self.add_analysis_to_queue)

        self.add_constitutive_laws_to_queue_button = QPushButton('Add Constitutive laws to queue')
        self.add_constitutive_laws_to_queue_button.setDisabled(True)
        self.add_constitutive_laws_to_queue_button.clicked.connect(self.add_mekameshes_to_queue)

        self.add_analysis_to_queue_button = QPushButton('Add Analysis to queue')
        self.add_analysis_to_queue_button.setDisabled(True)
        self.add_analysis_to_queue_button.clicked.connect(self.add_analysis_to_queue)

        self.main_layout.addWidget(self.material_groupbox, 0, 0)
        self.main_layout.addWidget(self.constitutive_law_groupbox, 0, 1)
        self.main_layout.addWidget(self.mechanical_laws_widget, 1, 0)
        self.main_layout.addWidget(self.mekamesh_analysis_groupbox, 1, 1)
        self.main_layout.addWidget(self.add_mat_attrib_to_queue_button, 2, 0, 1, 2)
        self.main_layout.addWidget(self.add_constitutive_laws_to_queue_button, 3, 0, 1, 2)
        self.main_layout.addWidget(self.add_analysis_to_queue_button, 4, 0, 1, 2)

    def create_material_widget(self):
        # Material widget
        self.material_groupbox = QGroupBox("Material attribution")

        self.material_layout = QVBoxLayout()
        self.material_groupbox.setLayout(self.material_layout)
        self.material_groupbox.setMaximumHeight(300)

        self.material_attribution_widget = QWidget()
        self.material_attribution_layout = QHBoxLayout()
        self.material_attribution_widget.setLayout(self.material_attribution_layout)
        self.material_attribution_label = QLabel('Material attribution type')
        self.material_attribution_type_combobox = QComboBox()
        self.material_attribution_type_combobox.addItems(['Material step (MPa)', 'Number of materials'])
        self.material_attribution_layout.addWidget(self.material_attribution_label)
        self.material_attribution_layout.addWidget(self.material_attribution_type_combobox)
        self.material_attribution_layout.addStretch()

        self.materialMinValueWidget = QWidget()
        self.materialMinValueLayout = QHBoxLayout()
        self.materialMinValueWidget.setLayout(self.materialMinValueLayout)
        self.materialMinValueLabel = QLabel('Minimum value of material (MPa) : ')
        self.materialMinValueEdit = QLineEdit()
        self.materialMinValueEdit.setMaximumWidth(100)
        self.materialMinValueEdit.setText('0.01')
        self.materialMinValueEdit.textChanged.connect(self.textValueChanged)
        self.materialMinValueLayout.addWidget(self.materialMinValueLabel)
        self.materialMinValueLayout.addWidget(self.materialMinValueEdit)
        self.materialMinValueLayout.addStretch()

        self.materialStepWidget = QWidget()
        self.materialStepLayout = QHBoxLayout()
        self.materialStepWidget.setLayout(self.materialStepLayout)
        self.material_step_type = 'Material step'
        self.materialStepLabel = QLabel('Material step (MPa) : ')
        self.materialStepEdit = QLineEdit()
        self.materialStepEdit.setMaximumWidth(100)
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

        self.material_attribution_type_combobox.currentIndexChanged.connect(self.react_material_step_type)
        self.material_attribution_type_combobox.setCurrentIndex(0)

        self.materialStepApproxWidget = QWidget()
        self.materialStepApproxLayout = QHBoxLayout()
        self.materialStepApproxWidget.setLayout(self.materialStepApproxLayout)
        self.materialStepApproxLabel = QLabel('Material step approximation : ')
        self.materialStepApproxComboBox = QComboBox()
        self.materialStepApproxComboBox.addItems(['inferior bound', 'middle bound', 'superior bound'])
        self.materialStepApproxComboBox.setCurrentIndex(1)
        self.materialStepApproxComboBox.currentIndexChanged.connect(self.tab_reaction)
        self.materialStepApproxLayout.addWidget(self.materialStepApproxLabel)
        self.materialStepApproxLayout.addWidget(self.materialStepApproxComboBox)
        self.materialStepApproxLayout.addStretch()

        self.material_layout.addWidget(self.material_attribution_widget)
        self.material_layout.addWidget(self.materialMinValueWidget)
        self.material_layout.addWidget(self.materialStepWidget)
        self.material_layout.addWidget(self.materialStepApproxWidget)

    def react_material_step_type(self):
        if self.material_attribution_type_combobox.currentIndex() == 0:
            self.material_step_type = 'Material step'
            self.materialStepLabel.setText('Material step (MPa) : ')
        elif self.material_attribution_type_combobox.currentIndex() == 1:
            self.material_step_type = 'Material number'
            self.materialStepLabel.setText('Number of materials : ')

    def create_constitutive_law_groupbox(self):
        self.constitutive_law_groupbox = QGroupBox('Constitutive law')
        self.constitutive_law_layout = QVBoxLayout()
        self.constitutive_law_groupbox.setLayout(self.constitutive_law_layout)

        self.materialSymmetryWidget = QWidget()
        self.materialSymmetryLayout = QHBoxLayout()
        self.materialSymmetryWidget.setLayout(self.materialSymmetryLayout)
        self.materialSymmetryLabel = QLabel('Material Symmetry :')
        self.materialSymmetryComboBox = QComboBox()
        self.materialSymmetryComboBox.addItems(['- Choose material symmetry -', 'isotropic', 'orthotropic'])
        self.materialSymmetryComboBox.setCurrentIndex(1)
        self.materialSymmetryComboBox.currentIndexChanged.connect(self.tab_reaction)
        self.materialSymmetryLayout.addWidget(self.materialSymmetryLabel)
        self.materialSymmetryLayout.addWidget(self.materialSymmetryComboBox)
        self.materialSymmetryLayout.addStretch()

        self.elasticModelWidget = QWidget()
        self.elasticModelLayout = QHBoxLayout()
        self.elasticModelWidget.setLayout(self.elasticModelLayout)
        self.elasticModelLabel = QLabel('Elastic mechanical properties :')
        self.elasticModelComboBox = QComboBox()
        self.elasticModelComboBox.addItems(['- Choose elastic model -', 'Keller et al. (1994)', 'Kopperdahl et al. (2002)'])
        self.elasticModelComboBox.currentIndexChanged.connect(self.tab_reaction)
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
        self.plasticModelComboBox.currentIndexChanged.connect(self.tab_reaction)
        self.plasticModelLayout.addWidget(self.plasticModelLabel)
        self.plasticModelLayout.addWidget(self.plasticModelComboBox)
        self.plasticModelLayout.addStretch()

        self.constitutive_law_layout.addWidget(self.materialSymmetryWidget)
        self.constitutive_law_layout.addWidget(self.elasticModelWidget)
        self.constitutive_law_layout.addWidget(self.plasticModelWidget)

    def create_analysis_groupbox(self):
        self.mekamesh_analysis_groupbox = QGroupBox('Mekamesh analysis')
        self.mekamesh_analysis_layout = QVBoxLayout()
        self.mekamesh_analysis_groupbox.setLayout(self.mekamesh_analysis_layout)

        self.mekamesh_BMD = QCheckBox('BMD')
        self.mekamesh_density = QCheckBox('Density')
        self.mekamesh_modulus = QCheckBox("Young's modulus")

        self.mekamesh_analysis_layout.addWidget(self.mekamesh_BMD)
        self.mekamesh_analysis_layout.addWidget(self.mekamesh_density)
        self.mekamesh_analysis_layout.addWidget(self.mekamesh_modulus)

    def sliderValueChanged(self, value):
        self.materialStepEdit.setText(str(value))
        self.tab_reaction()

    def textValueChanged(self):
        try:
            self.materialStepSlider.setValue(int(self.materialStepEdit.text()))
        except ValueError:
            self.materialStepSlider.setValue(0)
        self.tab_reaction()

    def tab_reaction(self):
        if len(self.materialStepEdit.text()) == 0\
        or self.elasticModelComboBox.currentIndex() == 0\
        or self.materialSymmetryComboBox.currentIndex() == 0\
        or self.materialStepApproxComboBox.currentIndex() == 0:
            self.add_constitutive_laws_to_queue_button.setDisabled(True)
        else:
            self.add_constitutive_laws_to_queue_button.setDisabled(False)
            self.add_mat_attrib_to_queue_button.setDisabled(False)
            self.parent
        try:
            self.materialStep = int(self.materialStepEdit.text())
        except ValueError:
            self.add_constitutive_laws_to_queue_button.setDisabled(True)

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
            self.mechanical_laws_widget.clear_layout()

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
            self.mechanical_laws_widget.clear_layout()

            self.addField(1, 5)
            self.addField(4, 3)
            self.addField(10, 2)
            self.addField(11, 2)
            self.config = 'Kopperdahl2002-EPP-iso'

        elif self.elasticModelComboBox.currentIndex() == 1 and self.symmetry == 'isotropic':
            # clear layoutLaw
            self.mechanical_laws_widget.clear_layout()

            self.addField(1, 2)
            self.addField(4, 2)
            self.config = 'Keller1998-EL-iso'

    def addField(self, property_index=None, law_index=None):
        self.mechanical_laws_widget.addField(property_index, law_index)

    def add_mekameshes_to_queue(self):
        self.parent.get_selected_seg()
        if self.material_attribution_type_combobox.currentIndex() == 0:
            self.material_attribution_type = 'material_step'
        elif self.material_attribution_type_combobox.currentIndex() == 1:
            self.material_attribution_type = 'material_number'
        self.min_value = self.materialMinValueEdit.text()
        self.material_step = self.materialStepEdit.text()

        if self.materialStepApproxComboBox.currentIndex() == 0:
            self.material_step_approx = 'inf'
        elif self.materialStepApproxComboBox.currentIndex() == 1:
            self.material_step_approx = 'mid'
        elif self.materialStepApproxComboBox.currentIndex() == 2:
            self.material_step_approx = 'sup'

        self.mechanicalLawList = self.mechanical_laws_widget.get_mechanical_law_list()
        self.datasets = self.parent.datasets
        WL = Waiting_list()
        WL.add_laws_attribution(datasets=self.datasets, meshes=self.parent.get_meshes(),
                             material_step_type=self.material_attribution_type,
                                                  material_step=self.material_step, min_value=self.min_value,
                           mechanical_law_list=self.mechanicalLawList)

        print('added mekameshes to queue')

    def add_analysis_to_queue(self):
        print('add analysis to queue')

    '''def create_mekameshes(self):
        for propertyField in self.propertyFieldList:
            if propertyField.get_chosen_law():
                self.mechanicalLawList.append(propertyField.get_chosen_law())

        # TODO material step type widget
        self.materialStepType = "material number - equal step"

        for mekamesh in self.selectedMeshesList:
            mekamesh = set_config_meca_for_mekamesh(mekamesh,
                                                     self.config,
                                                     self.mechanicalLawList,
                                                     self.materialStepType, self.materialStep, self.approximation)
            mekamesh.unread()
            mekamesh.read()
        self.parentWindow.update_mesh()
        #except (ValueError, TypeError, AttributeError) as e:
        #    self.parentWindow.showMessage(True, e.__str__())
        #else:
        self.close()'''


class MechanicalLawsWidget(QGroupBox):
    def __init__(self, parent=None):
        self.parent = parent

        super(MechanicalLawsWidget, self).__init__(self.parent)

        self.setTitle('Density to mechanical properties relationships')

        self.mechanicalLawList = []
        self.chosenPropertyListIndex = set({})
        self.propertyFieldList = []
        self.propertyList = ['EX', 'EY', 'EZ', 'NUXY', 'NUYZ', 'NUXZ', 'GXY', 'GYZ', 'GXZ', 'Yield strength',
                             'Plastic modulus']

        self.layoutlaw = QVBoxLayout()
        self.layoutlaw.setSpacing(0)
        self.mechanical_table = QWidget()
        self.mechanical_table.setLayout(self.layoutlaw)
        self.layoutlaw.addStretch()
        self.addField()
        self.add_field_button = AddFieldButton(self)
        self.layoutlaw.addWidget(self.add_field_button)

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.mechanical_table)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setMinimumHeight(200)
        self.scroll.setMinimumWidth(600)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.scroll)
        self.main_layout.addStretch()
        self.setLayout(self.main_layout)

    def clear_layout(self):
        self.propertyFieldList = []
        for i in reversed(range(self.layoutlaw.count())):
            try:
                self.layoutlaw.itemAt(i).widget().setParent(None)
            except AttributeError:
                pass
        self.add_field_button = AddFieldButton(self)
        self.layoutlaw.addWidget(self.add_field_button)

    def addField(self, property_index=None, law_index=None):
        index = len(self.propertyFieldList)
        if property_index and law_index:
            new_field = PropertyField(self, index, property_index, law_index)
        else:
            new_field = PropertyField(self, index)
        # add a new field for choosing a mechanical property
        self.layoutlaw.insertWidget(index, new_field)
        self.propertyFieldList.append(new_field)

    def get_property_list(self):
        return self.propertyList

    def get_chosen_property_list(self):
        return self.chosenPropertyListIndex

    def get_mechanical_law_list(self):
        self.mechanicalLawList = []

        for propertyField in self.propertyFieldList:
            if propertyField.get_chosen_law():
                self.mechanicalLawList.append(propertyField.get_chosen_law())

        return self.mechanicalLawList

    def update_properties(self, index):
        count = 0
        for propertyField in self.propertyFieldList:
            if count != index:
                propertyField.update()
            index += 1

    def remove_field(self, index):
        self.propertyFieldList.pop(index)
        self.layoutlaw.itemAt(index).widget().deleteLater()
        for i in range(len(self.propertyFieldList)):
            self.propertyFieldList[i].update_index(i)


class AddFieldButton(QWidget):
    def __init__(self, parent):
        super(AddFieldButton, self).__init__(parent)
        self.parent = parent

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.title = QLabel("Add relationship")
        self.layout.addWidget(self.title)
        self.addFieldButton = CustomQToolButton(None, r'Images/add 2.svg', 16)
        self.addFieldButton.clicked.connect(self.parent.addField)
        self.layout.addWidget(self.addFieldButton)
        self.layout.addStretch()


class PropertyField(QWidget):
    def __init__(self, parent, index, property_index=None, law_index=None):
        super(PropertyField, self).__init__(parent)

        self.parent = parent
        self.index = index

        #self.setStyleSheet('QWidget{font-size:11pt;}')
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

