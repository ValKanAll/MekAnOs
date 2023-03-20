import numpy as np


class Element:
    def __init__(self, ID_element, ID_element_type, node_list):
        # Test type
        self.ID_element = ID_element
        self.node_list = node_list
        self.ID_element_type = ID_element_type
        self.face_color = FaceColor(0)

    def get_ID(self):
        return self.ID_element

    def get_ID_element_type(self):
        return self.ID_element_type

    def get_node_list(self):
        return self.node_list

    def get_face_color(self):
        return self.face_color

    def set_face_color(self, new_face_color):
        self.face_color = new_face_color

    def modify_ID_element(self, new_ID):
        if type(new_ID) == str:
            self.ID_element = new_ID
        else:
            raise NameError('new ID element is not a string')
        return self.ID_element

    def get_properties(self):
        return [['max length', self.max_edge_length()],
                ['volume', self.volume()]]

    def volume(self):
        if len(self.node_list) == 8:
            return self.distance_node(0, 1) ^ 3

    def max_edge_length(self):
        if len(self.node_list) == 8:
            return max(self.distance_node(0, 1),
                       self.distance_node(1, 2),
                       self.distance_node(2, 3),
                       self.distance_node(3, 0),
                       self.distance_node(0, 4),
                       self.distance_node(4, 5),
                       self.distance_node(5, 6),
                       self.distance_node(7, 4),
                       self.distance_node(1, 5),
                       self.distance_node(2, 6),
                       self.distance_node(3, 7))

    def distance_node(self, index_1, index_2):
        x1, y1, z1 = self.node_list[index_1].get_coord()
        x2, y2, z2 = self.node_list[index_2].get_coord()
        return np.sqrt((x2 - x1) ^ 2 + (y2 - y1) ^ 2 + (z2 - z1) ^ 2)

    def get_faces(self):
        face_list = []
        # tetrahedral mesh
        if len(self.node_list) in [4, 10]:
            face_list.append({self.node_list[0],
                              self.node_list[1],
                              self.node_list[2]})
            face_list.append({self.node_list[0],
                              self.node_list[1],
                              self.node_list[3]})
            face_list.append({self.node_list[0],
                              self.node_list[2],
                              self.node_list[3]})
            face_list.append({self.node_list[1],
                              self.node_list[2],
                              self.node_list[3]})
        # hexahedral mesh
        if len(self.node_list) in [8, 20]:
            face_list.append({self.node_list[0],
                              self.node_list[1],
                              self.node_list[2],
                              self.node_list[3]})
            face_list.append({self.node_list[0],
                              self.node_list[1],
                              self.node_list[5],
                              self.node_list[4]})
            face_list.append({self.node_list[1],
                              self.node_list[2],
                              self.node_list[6],
                              self.node_list[5]})
            face_list.append({self.node_list[2],
                              self.node_list[3],
                              self.node_list[7],
                              self.node_list[6]})
            face_list.append({self.node_list[3],
                              self.node_list[0],
                              self.node_list[4],
                              self.node_list[7]})
            face_list.append({self.node_list[4],
                              self.node_list[5],
                              self.node_list[6],
                              self.node_list[7]})
        return face_list

    def set_HU_value(self, new_HU_value):
        self.HU_value = new_HU_value

    def get_HU_value(self):
        return self.HU_value


class FaceColor:
    def __init__(self, index_color):
        self.index_color = index_color
        # i = 0 : not defined
        # i = -1 : not satisfying
        # i > 0 : group i

    def get_color_index(self):
        return self.index_color

    def set_color_index(self, new_index):
        self.index_color = new_index
