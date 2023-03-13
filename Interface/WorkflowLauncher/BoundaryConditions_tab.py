from PyQt5.QtWidgets import (QGridLayout, QWidget)


#from MekAnos.Material_assignment.module.Converters.ModifyMechanicalLaw import create_new_mekamesh_from_mekamesh


class BoundaryConditions_tab(QWidget):
    def __init__(self, parent):
        super(BoundaryConditions_tab, self).__init__(parent)

        self.parent = parent
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)

