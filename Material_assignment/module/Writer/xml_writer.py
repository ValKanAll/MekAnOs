from xml.etree import cElementTree as ET
from xml.dom import minidom


def write_position_file(file_path, stl_path="", prop_dict={}, version='1.0'):
    # prop_dict structure is {prop1: value_prop1,
    #                           prop2: {sub_prop1: value_sub_prop_1, sub_prop2: value_sub_prop2}}
    tree = ET.Element('Position_File')
    tree.set('stl_path', stl_path)
    for prop in prop_dict:
        prop_tree = ET.SubElement(tree, prop)
        if type(prop_dict[prop]) == dict:
            for sub_prop in prop_dict[prop]:
                if type(prop_dict[prop][sub_prop]) == dict:
                    sub_prop_tree = ET.Element(sub_prop)
                    for sub_sub_prop in prop_dict[prop][sub_prop]:
                        sub_prop_tree.attrib[sub_sub_prop] = str(prop_dict[prop][sub_prop][sub_sub_prop])
                else:
                    sub_prop_tree = ET.Element(sub_prop)
                    sub_prop_tree.text = str(prop_dict[prop][sub_prop])
                prop_tree.append(sub_prop_tree)
        else:
            prop_tree.text = str(prop_dict[prop])

    tree_string = minidom.parseString(ET.tostring(tree, short_empty_elements=False, encoding='utf-8', method='xml')).toprettyxml()
    file = open(file_path, "w")
    file.write(tree_string)  # .encode("utf-8"))
    file.close()