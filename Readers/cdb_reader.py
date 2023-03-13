import numpy as np


def read_named_selection_nodes(cdb_path):
    '''named selection format : [name, [node1, node2, ...]]'''
    named_selections_list = []
    with open(cdb_path, 'r', errors="ignore") as f:
        line = f.readline()
        while line:
            # DETECTING TABLE OF COORDINATE (NODES)
            if line.find("CMBLOCK") != -1 and line.find("NODE") != -1:
                set_nodes = set({})
                name = line.split(',')[1]
                number_nodes = int(line.split(',')[3].split('!')[0])
                f.readline()
                line = f.readline()
                while len(set_nodes) < number_nodes + 1:
                    node_line_list = line.split('\n')[0].split(' ')
                    for node in node_line_list:
                        set_nodes.add(node)
                    line = f.readline()
                set_nodes.remove('')
                list_nodes = sorted([int(node_str) for node_str in set_nodes])
                named_selections_list.append([name, list_nodes])
            line = f.readline()
    #print(named_selections_list)
    return named_selections_list


def read_mean_coordinates_named_selection(cdb_path, named_selection_path="", only_endplates=True):
    if named_selection_path == "":
        named_selection_path = cdb_path
    named_selection_list = read_named_selection_nodes(named_selection_path)
    mean_coordinates = []
    for named_selection in named_selection_list:
        if named_selection[0].find("ENDPLATE_TOP") == -1 and named_selection[0].find("ENDPLATE_BOTTOM") == -1 and only_endplates:
            pass
        else:
            x_list = []
            y_list = []
            z_list = []
            node_list = named_selection[1]
            with open(cdb_path, 'r', errors="ignore") as f:
                # Open the mesh_file_path file to extract the table of connection and the table of coordinates.
                extract_nodes = False
                line = f.readline()
                while line:
                    # DETECTING TABLE OF COORDINATE (NODES)
                    if line.find("NBLOCK") != -1:
                        line = f.readline()
                        NODE_LEN = int(line.split(',')[0].replace('(', '').split('i')[1])
                        NODE_PROPERTIES_NB = 3  # line.split(',')[0].replace('(', '').split('i')[0]
                        COORD_LEN = int(line.split(',')[1].split('.')[0].split('e')[1])
                        extract_nodes = True
                        line = f.readline()
                        continue

                    # EXTRACTING
                    if extract_nodes:
                        if line.find("-1,") != -1:
                            extract_nodes = False
                            line = f.readline()
                            continue
                        node_id = int(line[:NODE_LEN])
                        if node_id in node_list:
                            x_list.append(float(line[NODE_PROPERTIES_NB * NODE_LEN:3 * NODE_LEN + COORD_LEN]))
                            y_list.append(float(line[NODE_PROPERTIES_NB * NODE_LEN + COORD_LEN:3 * NODE_LEN + COORD_LEN * 2]))
                            z_list.append(float(line[NODE_PROPERTIES_NB * NODE_LEN + COORD_LEN * 2:3 * NODE_LEN + COORD_LEN * 3]))
                        line = f.readline()
                        continue
                    line = f.readline()
            mean_coordinates.append([average(x_list), average(y_list), average(z_list)])
    return mean_coordinates


def average(_list):
    return sum(_list)/len(_list)


def distance(point_a, point_b):
    xa, ya, za = point_a
    xb, yb, zb = point_b
    return np.sqrt((xa-xb)**2 + (ya-yb)**2 + (za-zb)**2)


def distance_endplates(cdb_path, named_selection_path=""):
    point_a, point_b = read_mean_coordinates_named_selection(cdb_path, named_selection_path, only_endplates=True)
    return distance(point_a, point_b)


def read_cdbfile_return_dict_element_density(path):
    """
    Extract the elements number and their associated material from a cdb mesh file.
    :param path: Path to the cdb file.
    :param is_mekamesh: if True, adds material property to element
    :return: Elements number array and associated materials, Nodes and associated coordinates x, y and z arrays.
    """
    # EXTRACTING THE TABLES OF CONNECTION AND COORDINATES
    load_elements = False
    extract_material = True
    node_list = []
    element_list = []
    material_list = []
    dict_frequency_material = {}  # count occurence of materials

    materials = []  # Material property number
    elems = []  # Table of connection
    with open(path, 'r', errors="ignore") as f:
        # Open the mesh_file_path file to extract the table of connection and the table of coordinates.
        extract_nodes = False
        extract_elems = False
        extract_plastic_prop = False
        line = f.readline()
        while line:
            #print(line)
            # DETECTING TABLE OF CONNECTION (ELEMENTS)
            if line.find("EBLOCK") != -1:
                line = f.readline()
                ELEM_LEN = int(line.split(',')[0].replace(')', '').split('i')[1])
                ELEM_START = 10  # Table of connection doesn't start before the 10th value
                extract_elems = True
                line = f.readline()
                continue

            # DETECTING AND EXTRACTING TABLE OF MATERIALS
            # ELASTIC PROPERTIES
            if line.find("MPDATA") != -1 and extract_material:
                prop = line.split(',')
                material_id = int(prop[4])
                index = 0
                for material in material_list:
                    id_mat = material['ID']
                    if material_id == id_mat:
                        continue
                    else:
                        index += 1
                if index == len(material_list):
                    new_material = {'ID': material_id}
                    material_list.append(new_material)

                if prop[3].find('EX') != -1:
                    material_list[index]['EX'] = float(prop[6])
                if prop[3].find('EY') != -1:
                    material_list[index]['EY'] = float(prop[6])
                if prop[3].find('EZ') != -1:
                    material_list[index]['EZ'] = float(prop[6])

                if prop[3].find('NUXY') != -1 or prop[3].find('PRXY') != -1:
                    material_list[index]['NUXY'] = float(prop[6])
                if prop[3].find('NUYZ') != -1 or prop[3].find('PRYZ') != -1:
                    material_list[index]['NUYZ'] = float(prop[6])
                if prop[3].find('NUXZ') != -1 or prop[3].find('PRXZ') != -1:
                    material_list[index]['NUXZ'] = float(prop[6])

                if prop[3].find('GXY') != -1:
                    material_list[index]['GXY'] = float(prop[6])
                if prop[3].find('GYZ') != -1:
                    material_list[index]['GYZ'] = float(prop[6])
                if prop[3].find('GXZ') != -1:
                    material_list[index]['GXZ'] = float(prop[6])

                if prop[3].find('DENS') != -1:
                    material_list[index]['DENS'] = float(prop[6])

                #print(line)
                line = f.readline()
                continue
            # PLASTIC PROPERTIES
            if line.find('TB,BISO') != -1 and extract_material:
                prop = line.split(',')
                material_id = int(prop[2])
                index = 0
                for material in material_list:
                    id_mat = material['ID']
                    if material_id == id_mat:
                        continue
                    else:
                        index += 1
                if index == len(material_list):
                    material_list.append(new_material)

                extract_plastic_prop = True
                line = f.readline()
                continue
            if extract_plastic_prop:
                if line.find('TBDAT') != -1:
                    prop = line.split(',')
                    material_list[index]['YS'] = float(prop[2])
                    material_list[index]['PM'] = float(prop[3])
                    extract_plastic_prop = False
                    line = f.readline()
                    continue

            # EXTRACTING
            if extract_elems:
                if line.find("-1") != -1:
                    extract_elems = False
                    line = f.readline()
                    continue
                line += f.readline()
                line = line.replace("\n", '')
                ID_material = int(line[:ELEM_LEN])
                try:
                    dict_frequency_material[ID_material] += 1
                except KeyError:
                    dict_frequency_material[ID_material] = 1
                # Count  number of elements with same element type
                line_elem = [int(line[i * ELEM_LEN:(i + 1) * ELEM_LEN]) for i in
                             range(ELEM_START, len(line) // ELEM_LEN)]

                if extract_material:
                    ID_element = line_elem[0]
                    element_list.append([ID_element, ID_material])
                else:
                    materials.append(ID_material)
                    elems.append(line_elem)
                line = f.readline()
                #print(line)
                continue

            line = f.readline()
    f.close()

    dict_rho_by_element = {}
    for element in element_list:
        ID_element = element[0]
        ID_material = element[1]
        for material in material_list:
            id = material['ID']
            if id == ID_material:
                dict_rho_by_element[ID_element] = material['DENS']
                continue
            else:
                index += 1

    return dict_rho_by_element, material_list





