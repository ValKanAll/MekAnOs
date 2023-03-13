from Readers.cdb_reader import read_cdbfile
from Writers.cdb_writer import write_cdb_file
import datetime
import numpy as np
import random


class Mesh:
    def __init__(self, path=None, parent=None):
        if path and type(path) == str:
            self.path = path
        else:
            raise NameError('mesh path is not a string')
        self.parent = parent

        # Init mekamesh
        self.mekamesh_list = []

        # Define elements, nodes and list
        self.is_loaded = False
        self.element_list = []
        self.node_list = []
        self.named_selections_list = []
        self.loaded_lonely_faces = False
        self.element_dict_by_neighbours_generated = False

    def set_parent(self, parent):
        self.parent = parent

    def set_number_element(self, number_elements):
        self.number_element = number_elements

    def get_is_loaded(self):
        return self.is_loaded

    def set_is_loaded(self, new_bool):
        self.is_loaded = new_bool
        return self.is_loaded

    def get_number_element(self):
        if self.is_loaded:
            self.number_element = str(len(self.element_list))
        return self.number_element

    def get_mekamesh_list(self):
        return self.mekamesh_list

    def set_mekamesh_list(self, mekamesh_list):
        for mekamesh in mekamesh_list:
            mekamesh.set_parent(self)
        self.mekamesh_list = mekamesh_list

    def get_element_list(self):
        return self.element_list

    def get_element_type_list(self):
        return self.element_type_list

    def get_node_list(self):
        return self.node_list

    def get_sample_node_list(self, population=1000):
        self.read()
        return np.array(random.sample([node.get_coord() for node in self.node_list
                                         ], population))  # returns np.array of n=population samples from points

    def get_path(self):
        return self.path

    def get_site(self):
        return self.site

    def get_named_selections_list(self):
        return self.named_selections_list

    def add_named_selections(self, named_selections):
        self.named_selections_list.append(named_selections)

    def modify_path(self, new_path):
        if type(new_path) == str:
            self.path = new_path
        else:
            raise NameError('new path is not a string')
        return self.path

    def modify_site(self, new_site):
        if type(new_site) == str:
            self.site = new_site
        else:
            raise NameError('new site is not a string')
        return self.site

    def set_element_list(self, element_list):
        self.element_list = element_list

    def set_element_type_list(self, element_type_list):
        self.element_type_list = element_type_list

    def set_node_list(self, node_list):
        self.node_list = node_list

    def set_named_selections_list(self, named_selections_list):
        self.named_selections_list = named_selections_list

    def get_infos(self):
        return [['Description', [['Object', 'Mesh'], ['Number of element', str(self.number_element)],
                ['Number of Mekameshes', str(len(self.mekamesh_list))], ['Path', self.path], ['FileName', self.path.split('/')[-1].split('\\')[-1]]]],
                ['Element types', [[str(element_type[0]), str(element_type[1]), str(element_type[2])] for element_type in self.element_type_list]],
                ['Named selections', self.named_selections_list]]

    def get_attributes_infos(self):
        self.attribute_list = [['Mesh', '']]
        self.attribute_list += [['Named selections', named_selections[0]] for named_selections in self.named_selections_list]
        return self.attribute_list

    def get_attributes(self):
        self.attribute_list = [self]
        self.attribute_list += self.named_selections_list
        return self.attribute_list

    def get_attributes_property(self):
        '''return a list of mesh properties (elements, materials)'''
        if not self.is_loaded:
            self.read()
        return [['Elements', self.element_list]]

    def get_nodes_dict(self):
        self.nodes_dict = dict()  # searching in dict is faster than searching in list
        for node in self.node_list:
            self.nodes_dict[node.get_ID_node()] = node

        return self.nodes_dict

    def get_element_dict(self):
        if not self.is_loaded:
            self.element_dict = dict()
            for element in self.element_list:
                self.element_dict[element.get_ID()] = element

    def get_center_element(self, ID_element):
        element = self.element_dict[ID_element]
        x = 0
        y = 0
        z = 0
        index = 0
        for ID_node in element.get_node_list():
            node = self.nodes_dict[ID_node]
            x += node.get_x()
            y += node.get_y()
            z += node.get_z()
            index += 1
        x = x/index
        y = y/index
        z = z/index
        return x, y, z

    #TODO diff get and calculate

    def get_element_dict_by_neighbours(self):
        '''returns a dict of element_ID : {IDs of neighbour elements}'''
        if not self.element_dict_by_neighbours_generated:
            faces_dict = dict()
            self.faces_dict = dict({})
            self.element_dict_by_neighbours = dict()
            index_face = 0
            for element in self.element_list:
                faces = element.get_faces()
                self.element_dict_by_neighbours[element.get_ID()] = frozenset()
                for face in faces:
                    if frozenset(face) in faces_dict:
                        element_set = set(faces_dict[frozenset(face)])
                        element_set.add(element.get_ID())
                        faces_dict[frozenset(face)] = frozenset(element_set)
                    else:
                        faces_dict[frozenset(face)] = frozenset({element.get_ID()})

            for face in faces_dict:
                elements = set(faces_dict[face])
                self.faces_dict[index_face] = elements
                index_face += 1
                for element in elements:
                    neighbours = set(self.element_dict_by_neighbours[element])
                    for element_ in elements:
                        if element_ != element:
                            neighbours.add(element_)
                    self.element_dict_by_neighbours[element] = frozenset(neighbours)
            self.element_dict_by_neighbours_generated = True
        return self.element_dict_by_neighbours

    def get_volume_dict(self, volume_path):
        self.volume_dict_by_element = read_data_by_elements(volume_path)
        return self.volume_dict_by_element

    def get_strain_dict(self, strain_path, yield_strain, time):
        self.strain_dict_by_element = read_data_by_elements(strain_path, yield_strain, time)
        return self.strain_dict_by_element

    def get_contiguous_plastic_volume(self, yield_strain, strain_path, volume_path, time=1):
        # get dict of volume and strain
        self.get_strain_dict(strain_path, yield_strain, time)
        print('strain file read')
        self.get_volume_dict(volume_path)
        print('volume file read')
        self.get_element_dict_by_neighbours()
        print('Element dict by neighbours written')

        # init
        total_volume_plastic = 0
        count_total_plastic_element = 0
        total_volume = 0
        color_index = 1
        self.plastic_element_list = []

        t0 = datetime.datetime.now()
        # first loop on elements to give them a first color
        for element in self.element_dict_by_neighbours:
            # add to count of total volume
            total_volume += self.volume_dict_by_element[element]
            center_strain = self.strain_dict_by_element[element]
            center_color = self.element_dict[element].get_face_color().get_color_index()
            if center_strain > 0:
                # add to the total count of plastic elements
                total_volume_plastic += self.volume_dict_by_element[element]
                count_total_plastic_element += 1
                self.plastic_element_list.append(element)
                if center_color == 0:
                    # for elements which has not been colored yet
                    min_color = color_index
                    center_color = color_index
                    for neighbour in self.element_dict_by_neighbours[element]:
                        neighbour_color = self.element_dict[neighbour].get_face_color().get_color_index()
                        # if neighbour is plastic it will have its color changed
                        if self.strain_dict_by_element[neighbour]:
                            # if index of neighbour smaller its index will be chosen
                            if min_color > neighbour_color > 0:
                                min_color = neighbour_color
                            # all plastic neighbours are pointing to center
                            self.element_dict[neighbour].set_face_color(self.element_dict[element].get_face_color())
                    # set center to min color
                    self.element_dict[element].get_face_color().set_color_index(min_color)
                    # if a new index has been chosen, increment count
                    if min_color == center_color:
                        color_index += 1
        t1 = datetime.datetime.now()
        print('Loop 1 done, time : {}'.format(t1 - t0))

        # loop to verify that sizes of islands do not move
        t0 = datetime.datetime.now()
        results_0 = self.plastic_element_list
        results_1, volumes_1 = self.loop()
        t1 = datetime.datetime.now()
        print('Loop 2 done, time : {}'.format(t1 - t0))
        count = 3
        while results_0 != results_1 or count < 10:
            t0 = datetime.datetime.now()
            results_0, volumes_0 = results_1, volumes_1
            #results_1, volumes_1 = self.loop2(results_0)
            results_1, volumes_1 = self.loop()
            t1 = datetime.datetime.now()
            print('Loop {} done, time : {}'.format(count, t1 - t0))
            count += 1
        # get results
        results, volumes = results_1, volumes_1

            # sort results by decreasing size of plastic volume
        sorted_volumes = [volume for volume in volumes]
        sorted_volumes.sort(reverse=True)
        sorted_index = []
        for volume in sorted_volumes:
            for index in range(len(volumes)):
                if volume == volumes[index]:
                    sorted_index.append(index)
                    break

        sorted_results = [results[k] for k in sorted_index]
        sorted_len_results = [result for result in sorted_results]

        '''
        # verify result
        len_total = len(sorted_results[0])
        index = 0
        for element in sorted_results[0]:
            if index % (len_total // 100) == 0:
                print(index)
            index += 1
            a = 0
            neighbours = self.element_dict_by_neighbours[element]
            for neighbour in neighbours:
                if neighbour not in sorted_results[0]:
                    a += 1
            if a == len(neighbours):
                print(element, 'ERROR no neighbour')
            if not self.strain_dict_by_element[element]:
                print(element, 'ERROR NOT PLASTIC')
                
        '''

        print('total_volume:', "%0.3f" % total_volume)
        print('total_volume_plastic:', "%0.3f" % total_volume_plastic)
        print('largest_plastic_volume:', "%0.3f" % sorted_volumes[0])
        print('loop_count= {}'.format(count))
        print('number_islands= {}'.format(len(sorted_len_results)))
        print('number_total_element', len(self.element_list))
        print('number_plastic_element:', count_total_plastic_element)
        print('number_element_largest_island:', sorted_len_results[0])

        return sorted_volumes[0], total_volume_plastic, total_volume

    def loop(self):
        max_color = 1
        for element in self.plastic_element_list:
            center_color = self.element_dict[element].get_face_color().get_color_index()
            max_color = max(max_color, center_color)
            min_color = center_color
            if center_color > 0:
                for neighbour in self.element_dict_by_neighbours[element]:
                    neighbour_color = self.element_dict[neighbour].get_face_color().get_color_index()
                    if min_color > neighbour_color > 0:
                        min_color = neighbour_color
                        self.element_dict[neighbour].set_face_color(self.element_dict[element].get_face_color())
                if min_color != center_color:
                    self.element_dict[element].get_face_color().set_color_index(min_color)

        # export results
        results = [0] * (max_color + 1)
        volumes = [0] * (max_color + 1)
        total_len = len(self.plastic_element_list)
        index = 0
        for element in self.plastic_element_list:
            '''if index % (total_len // 10) == 0:
                print(index)
            index += 1'''
            color = self.element_dict[element].get_face_color().get_color_index()
            if color > 0:
                results[color] += 1
                volumes[color] += self.volume_dict_by_element[element]

        return results, volumes

    def loop2(self, previous_results):
        for color in previous_results:
            island = previous_results[color]
            for element in island:
                center_color = self.element_dict[element].get_face_color().get_color_index()
                min_color = center_color
                if center_color > 0:
                    for neighbour in self.element_dict_by_neighbours[element]:
                        neighbour_color = self.element_dict[neighbour].get_face_color().get_color_index()
                        if min_color > neighbour_color > 0:
                            min_color = neighbour_color
                            self.element_dict[neighbour].set_face_color(self.element_dict[element].get_face_color())
                    if min_color != center_color:
                        self.element_dict[element].get_face_color().set_color_index(min_color)

        # export results
        results = dict({})
        volumes = dict({})
        for element in self.plastic_element_list:
            color = self.element_dict[element].get_face_color().get_color_index()
            if color > 0:
                if color in results:
                    res = set(results[color])
                    if element not in res:
                        res.add(element)
                        results[color] = frozenset(res)
                        volumes[color] += self.volume_dict_by_element[element]
                else:
                    res = set()
                    res.add(element)
                    results[color] = frozenset(res)
                    volumes[color] = self.volume_dict_by_element[element]

        return results, volumes

    def get_lonely_faces_nodes(self):
        '''return nodes that are only on surfaces'''
        if not self.loaded_lonely_faces:
            for ns in self.named_selections_list:
                if ns[0] == 'SURFACE_NODES':
                    self.lonely_faces_nodes = []
                    self.get_nodes_dict()
                    for node_ID in ns[1]:
                        self.lonely_faces_nodes.append(self.nodes_dict[node_ID])
                    self.loaded_lonely_faces = True
                    return self.lonely_faces_nodes

            lonely_faces_set = set({})
            faces_dict = dict()
            for element in self.element_list:
                faces = element.get_faces()
                for face in faces:
                    if frozenset(face) in faces_dict:
                        faces_dict[frozenset(face)] = faces_dict[frozenset(face)] + 1
                    else:
                        faces_dict[frozenset(face)] = 1
            for face in faces_dict:
                if faces_dict[frozenset(face)] == 1:
                    lonely_faces_set.add(frozenset(face))
            del faces_dict
            lonely_faces_nodes_set = set({})
            for lonely_face in lonely_faces_set:
                for node in lonely_face:
                    lonely_faces_nodes_set.add(node)
            lonely_faces_nodes_ID_list = list(lonely_faces_nodes_set)
            del lonely_faces_nodes_set
            self.lonely_faces_nodes = []
            self.get_nodes_dict()
            for node_ID in lonely_faces_nodes_ID_list:
                self.lonely_faces_nodes.append(self.nodes_dict[node_ID])
            self.loaded_lonely_faces = True

            self.named_selections_list.append(['SURFACE_NODES', lonely_faces_nodes_ID_list])
            del lonely_faces_nodes_ID_list
            return self.lonely_faces_nodes
        else:
            return self.lonely_faces_nodes

    def read(self):
        if not self.is_loaded:
            if self.path:
                read_cdbfile(self.path, self)
                self.is_loaded = True

            else:
                raise NameError('missing path for mesh')

    def unread(self):
        # empty memory of elements and nodes
        self.is_loaded = False
        self.element_list = []
        self.node_list = []
        self.named_selections_list = []

        try:
            del self.element_dict
            del self.nodes_dict
        except AttributeError:
            pass

        self.loaded_lonely_faces = False
        self.lonely_faces_nodes = []

    def write(self, new_path=None):
        if self.is_loaded:
            if new_path:
                self.path = new_path
            write_cdb_file(self.path, self)
        else:
            raise NameError('Mesh is not loaded so cannot be written')

    def remove_named_selections(self, name):
        if self.is_loaded:
            index = 0
            for named_selections in self.named_selections_list:
                if named_selections[0] == name:
                    self.named_selections_list.pop(index)
                    break
            self.write()


def read_data_by_elements(path, threshold=None, time=1):
    """ Reads document of 2 columns with elements ID in the first column
    and the corresponding value in the second column
    returns : a dict of the values """
    if threshold:
        try:
            threshold = float(threshold)
        except ValueError:
            raise ValueError('threshold is not a float')
    result_dict = dict({})
    with open(path, 'r', errors="ignore") as f:
        # Open the mesh_file_path file to extract the table of connection and the table of coordinates.
        line = f.readline()
        while line:
            try:
                values = line.split()
                if threshold is not None:
                    if time*float(values[1]) > threshold:
                        val = 1
                    else:
                        val = 0
                    result_dict[int(values[0])] = val
                else:
                    result_dict[int(values[0])] = time*float(values[1])
            except ValueError:
                pass
            line = f.readline()

    f.close()
    return result_dict


def intersect(L1, L2):
    res = []
    La, Lb = (L1, L2) if len(L1) <= len(L2) else (L2, L1)
    for i in La:
        if i in Lb:
            res.append(i)
    return res








