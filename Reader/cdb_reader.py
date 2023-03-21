import numpy as np
from Structure.Material import Material
from Structure.Node import  Node
from Structure.Element import Element
from Structure.MekaElement import MekaElement


def read_cdbfile(path, mesh=None, print_occurence_file_by_element=True, print_occurence_file_by_material=False):
    """
    Extract the elements number and their associated material from a cdb mesh file.
    :param path: Path to the cdb file.
    :param mesh: if None, function just read the file, if not None it fills element_list of given mesh
    :param is_mekamesh: if True, adds material property to element
    :return: Elements number array and associated materials, Nodes and associated coordinates x, y and z arrays.
    """
    folder_path = path[:-len(path.split('/')[-1])]
    occurence_file_by_material_path = path.split('.cdb')[0] + '_occurrence_file_by_material.txt'
    occurence_file_by_element_path = path.split('.cdb')[0] + '_occurrence_file_by_element.txt'
    # EXTRACTING THE TABLES OF CONNECTION AND COORDINATES
    load_elements = False
    extract_material = False
    if mesh:
        if type(mesh).__name__ == 'Mekamesh':
            #ID_mesh = mesh.get_ID()
            load_elements = True
            extract_material = True
        elif type(mesh).__name__ == 'Mesh':
            try:
                ID_mesh = mesh.get_ID()
            except AttributeError:
                ID_mesh = None
            load_elements = True
            extract_material = False
        else:
            raise NameError('Given mesh is not Mesh or Mekamesh type')
    node_list = []
    element_list = []
    element_type_list = []
    material_list = []
    dict_frequency_material = {}  # count occurence of materials

    materials = []  # Material property number
    elems = []  # Table of connection
    nodes = []  # Table of coordinates
    x = []  # x-coordinates
    y = []  # y-coordinates
    z = []  # z-coordinates
    with open(path, 'r', errors="ignore") as f:
        # Open the mesh_file_path file to extract the table of connection and the table of coordinates.
        extract_nodes = False
        extract_elems = False
        extract_plastic_prop = False
        line = f.readline()
        while line:
            #print(line)
            # DETECTING TABLE OF COORDINATE (NODES)
            if line.find("NBLOCK") != -1:
                line = f.readline()
                NODE_LEN = int(line.split(',')[0].replace('(', '').split('i')[1])
                NODE_PROPERTIES_NB = 3  # line.split(',')[0].replace('(', '').split('i')[0]
                COORD_LEN = int(line.split(',')[1].split('.')[0].split('e')[1])
                extract_nodes = True
                line = f.readline()
                continue

            # DETECTING TABLE OF CONNECTION (ELEMENTS)
            if line.find("EBLOCK") != -1:
                line = f.readline()
                ELEM_LEN = int(line.split(',')[0].replace(')', '').split('i')[1])
                LINE_LEN = int(line.split(',')[0].replace('(', '').split('i')[0])
                ELEM_START = 10  # Table of connection doesn't start before the 10th value
                extract_elems = True
                line = f.readline()
                IS2LINES = False
                curs_pos = f.tell()
                sec_line = f.readline()
                if len(line) != len(sec_line):
                    IS2LINES = True
                f.seek(curs_pos)
                continue

            if line.find("ET,") != -1 and load_elements and line.find("SET") == -1 and line.find("DELETE") == -1:
                element_type_ID = line.split(',')[1]
                element_type_ref = line.split(',')[2].split('\n')[0]
                if element_type_ref == '187':
                    element_type = 'quadratic tetrahedron'
                if element_type_ref == '185':
                    element_type = 'linear hexahedron'
                if element_type_ref == '186':
                    element_type = 'quadratic hexahedron'
                if element_type_ref == '285':
                    element_type = 'linear tetrahedron'
                element_type_count = 0
                element_type_list.append([int(element_type_ID), element_type, element_type_count])

            # DETECTING AND EXTRACTING TABLE OF MATERIALS
            # ELASTIC PROPERTIES
            if line.find("MPDATA") != -1 and extract_material:
                prop = line.split(',')
                material_id = int(prop[4])
                index = 0
                for material in material_list:
                    id_mat = material.get_ID()
                    if material_id == id_mat:
                        continue
                    else:
                        index += 1
                if index == len(material_list):
                    new_material = Material(material_id)
                    try:

                        new_material.set_element_occurence(dict_frequency_material[material_id])
                    except KeyError:
                        print('Warning : material number {} do not contain elements'.format(material_id))
                        new_material.set_element_occurence(0)
                    #print(material_id)
                    material_list.append(new_material)

                if prop[3].find('EX') != -1:
                    material_list[index].set_EX(float(prop[6]))
                if prop[3].find('EY') != -1:
                    material_list[index].set_EY(float(prop[6]))
                if prop[3].find('EZ') != -1:
                    material_list[index].set_EZ(float(prop[6]))

                if prop[3].find('NUXY') != -1 or prop[3].find('PRXY') != -1:
                    material_list[index].set_NUXY(float(prop[6]))
                if prop[3].find('NUYZ') != -1 or prop[3].find('PRYZ') != -1:
                    material_list[index].set_NUYZ(float(prop[6]))
                if prop[3].find('NUXZ') != -1 or prop[3].find('PRXZ') != -1:
                    material_list[index].set_NUXZ(float(prop[6]))

                if prop[3].find('GXY') != -1:
                    material_list[index].set_GXY(float(prop[6]))
                if prop[3].find('GYZ') != -1:
                    material_list[index].set_GYZ(float(prop[6]))
                if prop[3].find('GXZ') != -1:
                    material_list[index].set_GXZ(float(prop[6]))

                if prop[3].find('DENS') != -1:
                    material_list[index].set_DENS(float(prop[6]))

                #print(line)
                line = f.readline()
                continue
            # PLASTIC PROPERTIES
            if line.find('TB,BISO') != -1 and extract_material:
                prop = line.split(',')
                material_id = int(prop[2])
                index = 0
                for material in material_list:
                    id_mat = material.get_ID()
                    if material_id == id_mat:
                        continue
                    else:
                        index += 1
                if index == len(material_list):
                    new_material = Material(material_id)
                    new_material.set_element_occurence(dict_frequency_material[material_id])
                    material_list.append(new_material)

                extract_plastic_prop = True
                line = f.readline()
                continue
            if extract_plastic_prop:
                if line.find('TBDAT') != -1:
                    prop = line.split(',')
                    material_list[index].set_yield_strength(float(prop[2]))
                    material_list[index].set_plastic_modulus(float(prop[3]))
                    extract_plastic_prop = False
                    line = f.readline()
                    continue

            # EXTRACTING
            if extract_nodes:
                if line.find("-1,") != -1:
                    extract_nodes = False
                    line = f.readline()
                    continue
                node_id = int(line[:NODE_LEN])
                x_coord = float(line[NODE_PROPERTIES_NB * NODE_LEN:3 * NODE_LEN + COORD_LEN])
                y_coord = float(line[NODE_PROPERTIES_NB * NODE_LEN + COORD_LEN:3 * NODE_LEN + COORD_LEN * 2])
                z_coord = float(line[NODE_PROPERTIES_NB * NODE_LEN + COORD_LEN * 2:3 * NODE_LEN + COORD_LEN * 3])
                if load_elements:
                    node_list.append(Node(node_id, x_coord, y_coord, z_coord))
                else:
                    nodes.append(node_id)
                    x.append(x_coord)
                    y.append(y_coord)
                    z.append(z_coord)
                line = f.readline()
                continue
            if extract_elems:
                if line.find("-1") != -1:
                    extract_elems = False
                    line = f.readline()
                    continue
                if IS2LINES:
                    line += f.readline()
                #line = f.readline()
                line = line.replace("\n", '')
                ID_material = int(line[:ELEM_LEN])
                try:
                    dict_frequency_material[ID_material] += 1
                except KeyError:
                    dict_frequency_material[ID_material] = 1
                ID_element_type = int(line[ELEM_LEN: 2 * ELEM_LEN])
                # Count  number of elements with same element type
                for element_type in element_type_list:
                    if element_type[0] == ID_element_type:
                        element_type[2] += 1
                line_elem = [int(line[i * ELEM_LEN:(i + 1) * ELEM_LEN]) for i in
                             range(ELEM_START, len(line) // ELEM_LEN)]
                if load_elements:
                    if extract_material:
                        element_list.append(MekaElement(line_elem[0], ID_element_type, line_elem[1:], ID_material))
                    else:
                        element_list.append(Element(line_elem[0], ID_element_type, line_elem[1:]))
                else:
                    materials.append(ID_material)
                    elems.append(line_elem)
                line = f.readline()
                #print(line)
                continue

            line = f.readline()
    f.close()

    if load_elements:
        mesh.set_element_list(element_list)
        mesh.set_node_list(node_list)
        mesh.set_element_type_list(element_type_list)
        mesh.set_named_selections_list(read_named_selection_nodes(path))
        mesh.set_number_element(len(element_list))

        if extract_material:
            mesh.set_material_list(material_list)
            if print_occurence_file_by_material:
                file_occurence_by_material = open(occurence_file_by_material_path, 'w')
                file_occurence_by_material.write("ID_material\tEX(MPa)\n")
                for material in material_list:
                    for i in range(material.get_element_occurence()):
                        file_occurence_by_material.write(
                            str(material.get_ID()) + '\t'
                            + str(material.get_EX()) + '\n')
                file_occurence_by_material.close()

            if print_occurence_file_by_element:
                file_occurence_by_element = open(occurence_file_by_element_path, 'w')
                file_occurence_by_element.write("ID_element\tID_material\tEX(MPa)\n")
                for element in element_list:
                    ID_element = element.get_ID()
                    ID_material = element.get_ID_material()
                    EX = material_list[int(ID_material)-1].get_EX()
                    file_occurence_by_element.write(
                        str(ID_element) + '\t' + str(ID_material) + '\t' + str(EX) + '\n')
                file_occurence_by_element.close()

            print('extract materials')
            #mesh.set_is_loaded(True)

        return mesh
    '''else:
        elems = np.array(elems)
        materials = np.array(materials)
        nodes = np.array(nodes)
        x = np.array(x)
        y = np.array(y)
        z = np.array(z)

        return elems, materials, nodes, x, y, z'''


def get_element_occurence(path, result_path=None, all_prop=False):
    """
    Extract the elements number and their associated material from a cdb mesh file.
    :param path: Path to the cdb file.
    :return: Elements number array and associated materials, Nodes and associated coordinates x, y and z arrays.
    """
    folder_path = path[:-len(path.split('/')[-1])]
    if result_path:
        occurence_file_by_element_path = result_path
    else:
        occurence_file_by_element_path = path.split('.cdb')[0] + '_occurrence_file_by_element.txt'
    # EXTRACTING THE TABLES OF CONNECTION AND COORDINATES

    element_list = []
    material_list = []
    extract_material = True

    materials = []  # Material property number
    elems = []  # Table of connection
    nodes = []  # Table of coordinates
    x = []  # x-coordinates
    y = []  # y-coordinates
    z = []  # z-coordinates
    with open(path, 'r', errors="ignore") as f:
        # Open the mesh_file_path file to extract the table of connection and the table of coordinates.
        extract_nodes = False
        extract_elems = False
        extract_plastic_prop = False
        line = f.readline()
        while line:
            #print(line)
            # DETECTING TABLE OF COORDINATE (NODES)
            if line.find("NBLOCK") != -1:
                line = f.readline()
                NODE_LEN = int(line.split(',')[0].replace('(', '').split('i')[1])
                NODE_PROPERTIES_NB = 3  # line.split(',')[0].replace('(', '').split('i')[0]
                COORD_LEN = int(line.split(',')[1].split('.')[0].split('e')[1])
                #extract_nodes = True
                line = f.readline()
                continue

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
                if material_id == len(material_list) + 1:
                    new_material = Material(material_id)
                    # print(material_id)
                    material_list.append(new_material)
                index = material_id - 1

                if prop[3].find('EX') != -1:
                    material_list[index].set_EX(float(prop[6]))
                if prop[3].find('DENS') != -1:
                    material_list[index].set_DENS(float(prop[6]))
                if all_prop:
                    if prop[3].find('EY') != -1:
                        material_list[index].set_EY(float(prop[6]))
                    if prop[3].find('EZ') != -1:
                        material_list[index].set_EZ(float(prop[6]))

                    if prop[3].find('NUXY') != -1 or prop[3].find('PRXY') != -1:
                        material_list[index].set_NUXY(float(prop[6]))
                    if prop[3].find('NUYZ') != -1 or prop[3].find('PRYZ') != -1:
                        material_list[index].set_NUYZ(float(prop[6]))
                    if prop[3].find('NUXZ') != -1 or prop[3].find('PRXZ') != -1:
                        material_list[index].set_NUXZ(float(prop[6]))

                    if prop[3].find('GXY') != -1:
                        material_list[index].set_GXY(float(prop[6]))
                    if prop[3].find('GYZ') != -1:
                        material_list[index].set_GYZ(float(prop[6]))
                    if prop[3].find('GXZ') != -1:
                        material_list[index].set_GXZ(float(prop[6]))


                #print(line)
                line = f.readline()
                continue
            # PLASTIC PROPERTIES
            if all_prop:
                if line.find('TB,BISO') != -1 and extract_material:
                    prop = line.split(',')
                    material_id = int(prop[2])
                    index = 0
                    for material in material_list:
                        id_mat = material.get_ID()
                        if material_id == id_mat:
                            continue
                        else:
                            index += 1
                    if index == len(material_list):
                        new_material = Material(material_id)
                        material_list.append(new_material)

                    extract_plastic_prop = True
                    line = f.readline()
                    continue
                if extract_plastic_prop:
                    if line.find('TBDAT') != -1:
                        prop = line.split(',')
                        material_list[index].set_yield_strength(float(prop[2]))
                        material_list[index].set_plastic_modulus(float(prop[3]))
                        extract_plastic_prop = False
                        line = f.readline()
                        continue

            # EXTRACTING
            if extract_nodes:
                if line.find("-1,") != -1:
                    extract_nodes = False
                    line = f.readline()
                    continue
                node_id = int(line[:NODE_LEN])
                x_coord = float(line[NODE_PROPERTIES_NB * NODE_LEN:3 * NODE_LEN + COORD_LEN])
                y_coord = float(line[NODE_PROPERTIES_NB * NODE_LEN + COORD_LEN:3 * NODE_LEN + COORD_LEN * 2])
                z_coord = float(line[NODE_PROPERTIES_NB * NODE_LEN + COORD_LEN * 2:3 * NODE_LEN + COORD_LEN * 3])

                nodes.append(node_id)
                x.append(x_coord)
                y.append(y_coord)
                z.append(z_coord)
                line = f.readline()
                continue
            if extract_elems:
                if line.find("-1") != -1:
                    extract_elems = False
                    line = f.readline()
                    continue
                line += f.readline()
                line = line.replace("\n", '')
                ID_material = int(line[:ELEM_LEN])
                ID_element_type = int(line[ELEM_LEN: 2 * ELEM_LEN])
                # Count  number of elements with same element type
                line_elem = [int(line[i * ELEM_LEN:(i + 1) * ELEM_LEN]) for i in
                             range(ELEM_START, len(line) // ELEM_LEN)]
                if extract_material:
                    # ID_element, ID_element_type, node_number, ID_material
                    element_list.append([line_elem[0], line_elem[1:], ID_material])
                    #element_list.append(MekaElement(line_elem[0], ID_element_type, line_elem[1:], ID_material))

                else:
                    materials.append(ID_material)
                    elems.append(line_elem)
                line = f.readline()
                #print(line)
                continue

            line = f.readline()
    f.close()

    '''if load_elements:
        mesh.set_element_list(element_list)
        mesh.set_node_list(node_list)
        mesh.set_element_type_list(element_type_list)
        mesh.set_named_selections_list(read_named_selection_nodes(path))
        mesh.set_number_element(len(element_list))
        if extract_material:
            mesh.set_material_list(material_list)'''

    if extract_material:
        file_occurence_by_element = open(occurence_file_by_element_path, 'w')
        file_occurence_by_element.write("ID_element\tID_material\tEX(MPa)\trho(g/cc)\n")
        for element in element_list:
            ID_element = element[0]
            ID_material = element[2]
            EX = material_list[int(ID_material)-1].get_EX()
            rho = material_list[int(ID_material)-1].get_DENS()
            file_occurence_by_element.write(
                str(ID_element) + '\t' + str(ID_material) + '\t' + str(EX) + '\t' + str(rho) + '\n')
        file_occurence_by_element.close()

    print('extract materials')
    #mesh.set_is_loaded(True)

    del element_list
    del material_list
    del materials
    del elems
    del nodes
    del x
    del y
    del z

    return result_path


def read_occurence_file(path):
    E_list = []
    rho_list = []
    with open(path, 'r', errors="ignore") as f:
        line = f.readline()
        while line:
            try:
                E_list.append(float(line.split('\n')[0].split('\t')[2]))
                rho_list.append(float(line.split('\n')[0].split('\t')[3]))
            except ValueError:
                pass
            line = f.readline()
    f.close()
    return np.array(E_list), np.array(rho_list)


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







