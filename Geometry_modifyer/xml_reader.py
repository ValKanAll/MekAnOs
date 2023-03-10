from xml.etree import cElementTree as ET
import numpy as np


def read_position_file(pstf_path, version="1.0"):
    tree = ET.parse(pstf_path)
    root = tree.getroot()
    stl_path = root.attrib["stl_path"]
    # get patient list
    axis_tree = root.find("axis")
    X_vector = np.array([float(coord) for coord in axis_tree.find("X_vector").text.split("\t")])
    Y_vector = np.array([float(coord) for coord in axis_tree.find("Y_vector").text.split("\t")])
    Z_vector = np.array([float(coord) for coord in axis_tree.find("Z_vector").text.split("\t")])
    origin = np.array([float(coord) for coord in root.find("origin").text.split("\t")])
    selection_tree_list = root.find("selections")
    selection_list = []
    for selection_tree in selection_tree_list:
        #print(selection_tree)
        name = selection_tree.tag
        measure = selection_tree.attrib["measure"]
        function = selection_tree.attrib["function"]
        value = float(selection_tree.attrib["value"])
        selection_list.append([name, measure, function, value])

    #print(selection_list)

    return stl_path, X_vector, Y_vector, Z_vector, origin, selection_list