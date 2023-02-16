from module.Writer.cdb_writer import write_cdb_file
from module.Structure.Material import Material
import matplotlib.pyplot as plt


def set_property(mekamesh, new_mechanical_law_list):
    material_list = mekamesh.get_material_list()
    mechanical_law_list = mekamesh.get_mechanical_law_list()
    for material in material_list:
        material.clean()
    for new_mechanical_law in new_mechanical_law_list:
        # change material property
        prop = new_mechanical_law.get_law_property()
        measure = new_mechanical_law.get_densitometric_measure()
        law = new_mechanical_law.get_equation()
        for material in material_list:
            if prop == 'EX':
                material.set_EX(law(material.get_DENS()))
            if prop == 'EY':
                material.set_EY(law(material.get_DENS()))
            if prop == 'EZ':
                material.set_EZ(law(material.get_DENS()))
            if prop == 'NUXY':
                material.set_NUXY(law(material.get_DENS()))
            if prop == 'NUYZ':
                material.set_NUYZ(law(material.get_DENS()))
            if prop == 'NUXZ':
                material.set_NUXZ(law(material.get_DENS()))
            if prop == 'GXY':
                material.set_GXY(law(material.get_DENS()))
            if prop == 'GYZ':
                material.set_GYZ(law(material.get_DENS()))
            if prop == 'GXZ':
                material.set_GXZ(law(material.get_DENS()))
            if prop == 'YS':
                if measure == 'EX':
                    material.set_yield_strength(law(material.get_EX()))
                else:
                    material.set_yield_strength(law(material.get_DENS()))
            if prop == 'PM':
                if material.get_EX() > material.get_DENS():
                    material.set_plastic_modulus(law(material.get_DENS()))
                else:
                    material.set_plastic_modulus(material.get_EX()*0.9)
        # modify material law
        found = False
        while not found:
            index = 0
            for mechanical_law in mechanical_law_list:
                if mechanical_law.get_law_property() == prop:
                    mechanical_law_list[index] = new_mechanical_law
                    found = True
                else:
                    index += 1
            if index == len(mechanical_law_list) and not found:
                mechanical_law_list.append(new_mechanical_law)


def create_new_mekamesh_from_mekamesh(mekamesh, config_meca, mechanical_law_list,
                                   material_step_type=None, value_step=50, approximation='average', write=False):
    """
    Modifies mechanical properties of mechanical mesh (mekamesh)
    :param mekamesh: type Mekamesh, read mesh and its mechanical properties.
    :param config_meca: string name of the mechanical configuration applied.
    :param mechanical_law_list: list of mechanical laws applied to the properties.
    :param material_step_type: if None number of materials is not changed, just the properties;
    if .
    :param value_step: Function that maps the Young's modulus to every point of the 3D space.
    :param approximation: Persistent list where the integration of each element will be stored.
    """
    # data from mesh
    mekamesh.read()
    elementList = mekamesh.get_element_list()

    if material_step_type:
        new_path = mekamesh.get_path().split('.cdb')[0] + '_' + material_step_type + '_' + config_meca + '_' + str(value_step) + '.cdb'
    else:
        new_path = mekamesh.get_path().split('.cdb')[0] + '_' + config_meca + '.cdb'
    mekamesh.modify_path(new_path)

    if material_step_type:
        new_materialList = []
        materialList = mekamesh.get_material_list()
        materialDict = {}
        min_rho = 0
        max_rho = 0
        rho_list = []
        E_list = []
        rho_dict = {}

        if material_step_type == 'density_step':
            for material in mekamesh.get_material_list():
                rho = material.get_DENS()
                E_list.append(rho * 3230 - 34.7)
                rho_list.append(rho)
                min_rho = min(min_rho, rho)
                max_rho = max(max_rho, rho)
            rho_step = (max_rho - min_rho)/value_step
            print('number_step=', value_step)
            print('rho_step=', rho_step)
            print('number_of_materials=', len(rho_list))
            '''histo = plt.hist(E_list)
            plt.title('Young s modulus')
            plt.show()'''


            for element in elementList:
                material = materialList[element.get_ID_material()-1]
                ID = element.get_ID()
                rho = material.get_DENS()
                if approximation == 'inf':
                    rho = max(rho // rho_step * rho_step, 0)
                elif approximation == 'mid':
                    rho = max((rho // rho_step + 0.5) * rho_step, 0)
                elif approximation == 'sup':
                    rho = max((rho // rho_step + 1) * rho_step, 0)

                try:
                    ID_material = materialDict[rho]
                except KeyError:
                    ID_material = len(materialDict) + 1
                    materialDict[rho] = ID_material
                    material = Material(ID_material)
                    material.set_DENS(rho)
                    new_materialList.append(material)
                element.modify_material(ID_material)

        elif material_step_type == 'equal_material_proportion':
            for material in mekamesh.get_material_list():
                materialDict[material.get_ID()] = material

            sorted_ID_list = sorted(materialDict, key=lambda material_ID: materialDict[material_ID].get_DENS())  # sort material by their rho value

            index = 1
            init_number_mat = len(materialDict)
            number_mat_per_new_mat = init_number_mat // value_step
            accu_rho = []
            new_rho_list = []
            for material_ID in sorted_ID_list:
                accu_rho.append(materialDict[material_ID].get_DENS())
                if index % number_mat_per_new_mat == 0 or index == init_number_mat:
                    min_rho = min(accu_rho)
                    max_rho = max(accu_rho)
                    if approximation == 'inf':
                        new_rho = min_rho
                    elif approximation == 'mid':
                        new_rho = (max_rho - min_rho) / 2
                    elif approximation == 'sup':
                        new_rho = max_rho
                    elif approximation == 'average':
                        new_rho = sum(accu_rho) / len(accu_rho)
                    accu_rho = []
                    new_rho_list.append([min_rho, max_rho, new_rho])
                index += 1

            for element in elementList:
                material = materialList[element.get_ID_material()-1]
                ID = element.get_ID()
                rho = material.get_DENS()
                for bounds_rho in new_rho_list:
                    if bounds_rho[0] <= rho <= bounds_rho[1]:
                        rho = bounds_rho[2]

                try:
                    ID_material = rho_dict[rho]
                except KeyError:
                    ID_material = len(rho_dict) + 1
                    rho_dict[rho] = ID_material
                    material = Material(ID_material)
                    material.set_DENS(rho)
                    new_materialList.append(material)
                element.modify_material(ID_material)

            print('number_material=', value_step)
            '''histo = plt.hist(E_list)
            plt.title('Young s modulus')
            plt.show()'''

        elif material_step_type == 'equal_element_proportion':
            elementDict = {}
            for material in mekamesh.get_material_list():
                materialDict[material.get_ID()] = material

            for element in mekamesh.get_element_list():
                elementDict[element.get_ID()] = element

            sorted_element_ID_list = sorted(elementDict, key=lambda element_ID: materialDict[elementDict[element_ID].get_ID_material()].get_DENS())  # sort element by their rho value
            print(sorted_element_ID_list)
            print(len(sorted_element_ID_list))
# TODO redundant material
            index = 1
            index_material = 0
            number_element = len(elementDict)
            number_element_per_new_mat = number_element // value_step
            accu_rho = []
            accu_element = []
            for element_ID in sorted_element_ID_list:
                accu_rho.append(materialDict[elementDict[element_ID].get_ID_material()].get_DENS())
                accu_element.append(element_ID)
                if index % number_element_per_new_mat == 0 or index == number_element:
                    min_rho = min(accu_rho)
                    max_rho = max(accu_rho)
                    if approximation == 'inf':
                        new_rho = min_rho
                    elif approximation == 'mid':
                        new_rho = (max_rho - min_rho) / 2
                    elif approximation == 'sup':
                        new_rho = max_rho
                    elif approximation == 'average':
                        new_rho = sum(accu_rho) / len(accu_rho)
                    ID_material = index_material + 1
                    print(ID_material, len(accu_element), min_rho, max_rho, new_rho)
                    material = Material(ID_material)
                    material.set_DENS(new_rho)
                    new_materialList.append(material)
                    index_material += 1

                    for element_ID in accu_element:
                        element = elementDict[element_ID]
                        element.modify_material(ID_material)

                    accu_rho = []
                    accu_element = []
                index += 1

            print('number_material=', value_step)
            '''histo = plt.hist(E_list)
            plt.title('Young s modulus')
            plt.show()'''

        mekamesh.set_material_list(new_materialList)

    set_property(mekamesh, mechanical_law_list)

    if write:
        write_cdb_file(mekamesh.get_path(), mekamesh)

    return mekamesh
