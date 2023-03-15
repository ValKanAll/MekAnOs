from Writers.cdb_writer import write_cdb_file
from Readers.Mechanical_law_reader import global_list_EX, global_list_EY, global_list_EZ, \
                                            global_list_PM, global_list_YS,\
                                            global_list_NUXY, global_list_NUXZ, global_list_NUYZ,\
                                            global_list_GXY, global_list_GXZ, global_list_GYZ


def return_mechanical_law_from_config(config):
    mechanical_law_list = []
    if config == 'KopEPP07':
        mechanical_law_list.append(global_list_EX[3])
        mechanical_law_list.append(global_list_NUXY[1])
        mechanical_law_list.append(global_list_PM[0])
        mechanical_law_list.append(global_list_YS[0])

    elif config == 'KopEPP08':
        mechanical_law_list.append(global_list_EX[3])
        mechanical_law_list.append(global_list_NUXY[1])
        mechanical_law_list.append(global_list_PM[0])
        mechanical_law_list.append(global_list_YS[1])

    elif config == 'KopEPP10':
        mechanical_law_list.append(global_list_EX[3])
        mechanical_law_list.append(global_list_NUXY[1])
        mechanical_law_list.append(global_list_PM[0])
        mechanical_law_list.append(global_list_YS[2])

    elif config == 'KopEPP12':
        mechanical_law_list.append(global_list_EX[3])
        mechanical_law_list.append(global_list_NUXY[1])
        mechanical_law_list.append(global_list_PM[0])
        mechanical_law_list.append(global_list_YS[3])

    elif config == 'KopEPP15':
        mechanical_law_list.append(global_list_EX[3])
        mechanical_law_list.append(global_list_NUXY[1])
        mechanical_law_list.append(global_list_PM[0])
        mechanical_law_list.append(global_list_YS[4])

    elif config == 'KopEPP20':
        mechanical_law_list.append(global_list_EX[3])
        mechanical_law_list.append(global_list_NUXY[1])
        mechanical_law_list.append(global_list_PM[0])
        mechanical_law_list.append(global_list_YS[5])

    elif config == 'A0B3C1P5EPP07':
        mechanical_law_list.append(global_list_EX[7])
        mechanical_law_list.append(global_list_NUXY[1])
        mechanical_law_list.append(global_list_PM[0])
        mechanical_law_list.append(global_list_YS[5])

    elif config == 'A0B3C2EPP07':
        mechanical_law_list.append(global_list_EX[8])
        mechanical_law_list.append(global_list_NUXY[1])
        mechanical_law_list.append(global_list_PM[0])
        mechanical_law_list.append(global_list_YS[5])

    elif config == 'A0B3P5C1P5EPP07':
        mechanical_law_list.append(global_list_EX[9])
        mechanical_law_list.append(global_list_NUXY[1])
        mechanical_law_list.append(global_list_PM[0])
        mechanical_law_list.append(global_list_YS[5])

    elif config == 'A0B3P5C2EPP07':
        mechanical_law_list.append(global_list_EX[10])
        mechanical_law_list.append(global_list_NUXY[1])
        mechanical_law_list.append(global_list_PM[0])
        mechanical_law_list.append(global_list_YS[5])

    elif config == 'A0B3P5C0P8EPP07':
        mechanical_law_list.append(global_list_EX[11])
        mechanical_law_list.append(global_list_NUXY[1])
        mechanical_law_list.append(global_list_PM[0])
        mechanical_law_list.append(global_list_YS[5])

    elif config == 'A0B7C1P5EPP07':
        mechanical_law_list.append(global_list_EX[12])
        mechanical_law_list.append(global_list_NUXY[1])
        mechanical_law_list.append(global_list_PM[0])
        mechanical_law_list.append(global_list_YS[5])

    elif config == 'KopEL':
        mechanical_law_list.append(global_list_EX[3])
        mechanical_law_list.append(global_list_NUXY[1])

    elif config == 'KopEL04':
        mechanical_law_list.append(global_list_EX[3])
        mechanical_law_list.append(global_list_NUXY[2])

    return mechanical_law_list


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


def create_new_mekamesh_from_mekamesh(mekamesh, config_meca, write=False):
    """
    Modifies mechanical properties of mechanical mesh (mekamesh)
    :param mekamesh: type Mekamesh, read mesh and its mechanical properties.
    :param config_meca: string name of the mechanical configuration applied.
    """
    # data from mesh
    mekamesh.read()
    new_path = mekamesh.get_path().split('.cdb')[0] + '_' + config_meca + '.cdb'
    mekamesh.modify_path(new_path)

    mechanical_law_list = return_mechanical_law_from_config(config_meca)

    set_property(mekamesh, mechanical_law_list)

    if write:
        write_cdb_file(mekamesh.get_path(), mekamesh)

    return mekamesh
