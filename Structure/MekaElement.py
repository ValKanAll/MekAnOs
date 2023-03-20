from .Element import Element


class MekaElement(Element):
    def __init__(self, ID_element, ID_element_type, node_list, ID_material):
        # Inherit definition from Element
        Element.__init__(self, ID_element, ID_element_type, node_list)
        self.ID_material = ID_material

    def modify_material(self, new_ID_material):
        self.ID_material = new_ID_material
        return self.ID_material

    def get_ID_material(self):
        return self.ID_material



