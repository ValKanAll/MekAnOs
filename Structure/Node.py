class Node:
    def __init__(self, ID_node, x, y, z):
        self.ID_node = ID_node
        self.x = x
        self.y = y
        self.z = z

    def get_ID_node(self):
        return self.ID_node

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z

    def get_coord(self):
        return self.x, self.y, self.z

    def set_coord(self, x, y, z):
        self.x, self.y, self.z = x, y, z
        return self.x, self.y, self.z

    def modify_ID_node(self, new_value):
        if type(new_value) == int:
            self.ID_node = new_value
        else:
            raise NameError('new ID_node is not integer type')
        return self.ID_node

    def modify_x(self, new_x):
        if type(new_x) == float:
            self.x = new_x
        else:
            raise NameError('new x is not float type')
        return self.x

    def modify_y(self, new_y):
        if type(new_y) == float:
            self.y = new_y
        else:
            raise NameError('new y is not float type')
        return self.y

    def modify_z(self, new_z):
        if type(new_z) == float:
            self.z = new_z
        else:
            raise NameError('new z is not float type')
        return self.z




