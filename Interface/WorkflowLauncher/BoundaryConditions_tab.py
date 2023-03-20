from PyQt5.QtWidgets import (QGridLayout, QWidget)


#from MekAnos.Material_assignment.module.Converters.ModifyMechanicalLaw import set_config_meca_for_mekamesh


class BoundaryConditions_tab(QWidget):
    def __init__(self, parent):
        super(BoundaryConditions_tab, self).__init__(parent)

        self.parent = parent
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)

