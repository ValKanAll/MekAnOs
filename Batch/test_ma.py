from functools import partial
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pycpd.rigid_registration import RigidRegistration
import math
import datetime
import copy

import numpy as np

from module.Structure.Mekamesh import Mekamesh
from module.Converters.SetNamedSelections import add_endplates_ns, detect_endplate, add_endplates_ns_from_param, read_pstf_vertebra
from module.Reader.Mechanical_law_reader import global_list_EX, global_list_EY, global_list_EZ, \
                                            global_list_PM, global_list_YS,\
                                            global_list_NUXY, global_list_NUXZ, global_list_NUYZ,\
                                            global_list_GXY, global_list_GXZ, global_list_GYZ

from module.Converters.ModifyMechanicalLaw import create_new_mekamesh_from_mekamesh


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





def main():
    import time
    #time.sleep(3600)
    is_Artorg = False
    is_IBHGC = False
    is_JPR = True
    is_WL_QCT_postdefect = False
    is_WL = False
    is_MCC = False

    if is_JPR:
        time.sleep(3*3600)
        folder_path = "E:\Data_L3"
        patient_list = ['01_2007', '02_2007',
             '03',
                        '07_2007',
                         '08_2007',
                        '11_2007',
            '12_2007',
                        '13_2007', '15_2007',
                        '16_2007',
                    '17_2007',
                        '18_2007',
        '19_2007',
                        '20_2007',
                        '31',
            '32',
                        '35', '37', '40',
             '43', '44'
                        ]
        resolution_list = [#"984mic",
                           "656mic",
                           #"328mic"
                           ]
        seg_list = ['VB',
                    'VB2',
                    #'VB_AL',
                    #'VB_EC'
                    ]
        param_list = [#'QT_0328',
                        #'QT_0219',
                        'QT_1',
            #'QT_035',
                      #'QT_01', 'QT_08',
                      #'QT_02', 'QT_05', 'QT_1', 'QT_2']#, 'QT_200k']#, 'QT_500k'
                      ]
        software = 'qctma'
        qctma_step_list = [10,
            #1, 2,
                           #5, 10, 20, 50, 100, 200, 500
        ]
        poisson_coef_list = [[0.3, 'v03']]
        config_list = [#'KopEL',
                       'KopEPP07'
                        #'A0B3C1P5EPP07'
                        #"A0B3C2EPP07", "A0B3P5C1P5EPP07", "A0B3P5C2EPP07"
            #"A0B3P5C0P8EPP07", "A0B7C1P5EPP07"
                       ]
                       #'KopEPP15']  # 'Kopperdahl2002-EPP-iso'
        material_step_type = None#"equal_material_proportion"
        nb_mat_list = [200]  # number of materials
        approximation = 'average'

        for patient in patient_list:
            patient_folder = folder_path + "\\" + patient
            for resolution in resolution_list:
                resolution_folder = patient_folder + "\\" + patient + "_" + resolution
                mesh_folder = resolution_folder + r"\Mesh"
                for seg in seg_list:
                    stl_path = resolution_folder + '\\' + patient + "_" + resolution + "_" + seg + '.stl'
                    #detect_endplate(stl_path, sample=3000, distance=0.2, plot=2, endplate_height=3)
                    for param in param_list:
                        mesh_base = mesh_folder + "\\" + patient + "_" + resolution + "_" + seg + "_" + param
                        for qctma_step in qctma_step_list:
                            for poisson_coef in poisson_coef_list:
                                try:
                                    mekamesh_path = mesh_base + '_' + software + '_' + str(qctma_step) + poisson_coef[1] + ".cdb"
                                    print(mekamesh_path)
                                    t0 = datetime.datetime.now()
                                    print('\tStarted at : ', t0)
                                    mekamesh = Mekamesh(ID='', path=mekamesh_path)
                                    mekamesh.read()
                                    pstf_path = patient_folder + "\\" + patient + "_984mic" + '\\' + patient + "_984mic_VB.pstf"
                                    add_endplates_ns(mekamesh, stl_path, pstf_path=pstf_path, write=False)

                                    for config in config_list:
                                        for nb_mat in nb_mat_list:
                                            create_new_mekamesh_from_mekamesh(copy.deepcopy(mekamesh),
                                                                          config,
                                                                          return_mechanical_law_from_config(config),
                                                                          material_step_type, nb_mat,
                                                                          approximation, write=True)
                                        #mekamesh.write()
                                    t1 = datetime.datetime.now()
                                    print('\tDuration : ', t1 - t0)
                                except FileNotFoundError as e:
                                    print('#####ERROR: ', e)

    if is_WL_QCT_postdefect:
        folder_path = r"D:\Data_post-defect_2021-05-18"
        sample_list = ['01_2005_L1',
                       '01_2006_L1',
                       '02_2006_L1',
                       '2a_2005_L1',
                       '2b_2005_L1',
                       '03_2006_L1',
                       '04_2006_L1',
                       '05_2006_L1',
                       '06_2006_L1',
                       '08_2006_L1',
                       '10_2006_L1',
                       'USOD18433_L1',
                       'USOD20307_L1'
                       ]
        element_type_list = ['QT']
        param_list = ['100k']
        location = 'VB'
        resolution = 'def'
        config_list = ['KopEPP07']
        material_step_type = "equal_material_proportion"
        material_step = 100  # number of materials
        approximation = 'average'
        qctma_step = '10'
        software = 'qctma'
        time.sleep(1600)

        for sample in sample_list:
                for element_type in element_type_list:
                    for param in param_list:
                            for config in config_list:
                                try:
                                    mesh_path = folder_path + '\\' + sample + '_' + resolution + '\\' + 'Mesh' + '\\' + sample + '_' + resolution + '_' + \
                                                     location + '_' + element_type + '_' + param + '_' + software + '_' + qctma_step + 'v03NC.cdb'
                                    stl_path = folder_path + '\\' + sample + '_' + resolution + '\\' + '3DSlicer' + '\\' + sample + '_' + resolution + '_' + \
                                               location + '.stl'

                                    print(mesh_path)
                                    mekamesh = Mekamesh(ID='', path=mesh_path)
                                    mekamesh.read()
                                    add_endplates_ns(mekamesh, stl_path, write=False)

                                    create_new_mekamesh_from_mekamesh(mekamesh,
                                                                      config,
                                                                      return_mechanical_law_from_config(config),
                                                                      material_step_type, material_step,
                                                                      approximation, write=False)
                                    mekamesh.write()
                                except FileNotFoundError:
                                    pass

    if is_WL:
        folder_path = r"E:\Data_WL"
        sample_list = ['01_2005_L1',
                       '01_2006_L1',
                       '02_2006_L1',
                       '2a_2005_L1',
                       '2b_2005_L1',
                       '03_2006_L1',
                       '04_2006_L1',
                       '05_2006_L1',
                        '06_2006_L1',
                       '08_2006_L1',
                       '10_2006_L1',
                       'USOD18433_L1',
                       'USOD20307_L1'
                       ]
        element_type_list = ['QT']
        param_list = ['1',
            #'02', '03', '05', '1'
                      ]
        location = 'VB'
        seg_list = ['def_VB_F_transformed',
                    'def_VB_transformed',
                    'HRpQCT_VB'
            ]
        config_list = ['KopEPP07',
                       'KopEPP15',
                       'KopEL'
                       ]
        material_step_type = None#"equal_material_proportion"
        nb_mat = 100  # number of materials
        approximation = 'average'
        qctma_step_list = [#'5', '10',
                           '10']
        software = 'qctma'
        detect = False
        write = True
        read = False

        for sample in sample_list:
            for seg in seg_list:
                for element_type in element_type_list:
                    for param in param_list:
                        for qctma_step in qctma_step_list:
                            for config in config_list:

                                mesh_path = folder_path + '\\' + 'Mekamesh' + '\\' + sample + '_' + seg + '_' + element_type + '_' + param + '_' + software + '_' + qctma_step + 'v03_100MPa.cdb'
                                stl_path = folder_path + '\\' + 'Segmentation' + '\\' + sample + '_' + seg + '.stl'
                                if detect:
                                    detect_endplate(stl_path, sample=2000, distance=0.2, plot=1, endplate_height=2)
                                if read:
                                    read_pstf_vertebra(stl_path.replace('stl', 'pstf'), 1)
                                if write:
                                    print(mesh_path)
                                    mekamesh = Mekamesh(ID='', path=mesh_path)
                                    mekamesh.read()
                                    add_endplates_ns(mekamesh, stl_path, write=False)

                                    create_new_mekamesh_from_mekamesh(mekamesh,
                                                                      config,
                                                                      return_mechanical_law_from_config(config),
                                                                      material_step_type, nb_mat,
                                                                      approximation, write=False)
                                    mekamesh.write()

    if is_Artorg:

        sample_list = ['188', '192',
                        '195', '196', '199', '203', '204', '206', '208', '214', '217', '218', '220', '224',
                        '225', '226', '230', '231', '235', '236', '240', '248', '252', '256', '257', '260', '261', '264',
                        '268', '269', '273', '280', '281', '284', '285', '288', '289', '295', '298', '299',
                       '301', '305',
                        '308', '309', '317']
        element_type_list = ['QT']
        size_list = ['1']
        location = 'VB'
        resolution = '294mic'
        seg_list = ['A']#, 'VA']
        config_list = ['KopEPP15', 'KopEL']#, 'KopEPP10', 'KopEPP12', 'KopEPP15', 'KopEPP20']#'Kopperdahl2002-EPP-iso'
        material_step_type = None#"equal_material_proportion"
        material_step = 10  # number of materials
        approximation = 'average'
        approx_size_list = ['GS_0']#'GS_1', 'GS_3', 'GS_5', 'GS_10']
        qctma_step = '10'
        detect = False
        read = False
        write = True

        for sample in ['309']:
            for seg in seg_list:
                for element_type in element_type_list:
                    for size in size_list:
                            for config in config_list:
                                try:
                                    mesh_path = r'E:\Artorg_data_2021_metastatic_vertebrae' + '\\' + sample + '\\' + sample + '_' + resolution + '_' + \
                                                     location + '_' + seg + '_' + element_type + '_' + size + '_qctma_' + qctma_step + 'v03_100MPa' + '.cdb'

                                    stl_path = r'E:\Artorg_data_2021_metastatic_vertebrae' + '\\' + sample + '\\' + sample + '_' + resolution + '_' + \
                                               location + '_' + seg + '.stl'

                                    print(mesh_path)
                                    if detect:
                                        detect_endplate(stl_path, sample=3000, distance=0.2, plot=2, endplate_height=1)
                                    if read:
                                        read_pstf_vertebra(stl_path.replace('stl', 'pstf'), 1)
                                    if write:
                                        print(mesh_path)
                                        mekamesh = Mekamesh(ID='', path=mesh_path)
                                        mekamesh.read()
                                        add_endplates_ns(mekamesh, stl_path, write=False)

                                        create_new_mekamesh_from_mekamesh(mekamesh,
                                                                          config,
                                                                          return_mechanical_law_from_config(config),
                                                                          material_step_type, material_step,
                                                                          approximation, write=False)
                                        mekamesh.write()
                                except FileNotFoundError:
                                    print(mesh_path)


    if is_IBHGC:
        #time.sleep(3600)
        folder_path = r'E:\Data_IBHGC'
        sample_list = ['25_L2', '25_L3',
                       '41_L1', '41_L2',
                       '383_L1', '383_L2', '383_L3',
                       '421_L2', '421_L3',
                       '433_L1', '433_L2', '433_L3',
                       '436_L1', '436_L2', '436_L3',
                       '438_L1', '438_L2', '438_L3',
                       '448_L1', '448_L2', '448_L3',
                       '471_L1', '471_L2', '471_L3',
                       '484_L1', '484_L2', '484_L3',
                       '493_L2']
        param_list = ['QT_1', 'QT_2']
        seg_list = ['VB',
                    #'VB2'
                    ]
        config_list = [#'KopEPP07', 'KopEL',
                       'KopEL04']
                       #'KopEPP15']
        material_step_type = None #"equal_material_proportion"
        approximation = 'average'
        qctma_step = '10'
        min_E = 1
        detect = False
        read = False
        write = True

        for sample in sample_list:
            for seg in seg_list:
                stl_path = folder_path + '\\' + 'Segmentation' + '\\' + sample + '_' + \
                           seg + '.stl'
                for param in param_list:
                    try:
                        mesh_path = folder_path + '\\' + 'Mekamesh' + '\\' + sample + '_' + \
                                    seg + '_' + param + '_qctma_' + qctma_step + 'v03' + '.cdb'
                        if min_E:
                            mesh_path = folder_path + '\\' + 'Mekamesh' + '\\' + sample + '_' + \
                                        seg + '_' + param + '_qctma_' + qctma_step + 'min' + str(min_E) + '.cdb'
                        print(mesh_path)
                        t0 = datetime.datetime.now()
                        print('\tStarted at : ', t0)
                        if detect:
                            detect_endplate(stl_path, sample=3000, distance=0.2, plot=1, endplate_height=2.5)
                        if read:
                            read_pstf_vertebra(stl_path.replace('stl', 'pstf'), 1)
                        if write:
                            print(mesh_path)
                            mekamesh = Mekamesh(ID='', path=mesh_path)
                            mekamesh.read()
                            add_endplates_ns(mekamesh, stl_path, write=False)

                            for config in config_list:

                                create_new_mekamesh_from_mekamesh(mekamesh,
                                                                  config,
                                                                  return_mechanical_law_from_config(config),
                                                                  material_step_type, 0,
                                                                  approximation, write=False)

                                mekamesh.write()
                                mekamesh.modify_path(mesh_path)
                        t1 = datetime.datetime.now()
                        print('\tDuration : ', t1-t0)
                    except FileNotFoundError as e:
                        print('#####ERROR: ', e)
                        pass

    if is_MCC:  # Mekanos clinical cases
        # time.sleep(3600)
        folder_path = "E:\Mekanos_clinical_cases"
        patient_list = ['01017',
                        '01036'
                        ]
        element_type_list = ['QT']
        poisson_list = ['v03']
        param_list = [
            1
        ]
        seg_list = ['L5', 'L4',
                    'L3',
                    'L2', 'L1',
                    'T12', 'T11', 'T10', 'T9', 'T8'
                    ]

        resolution = 'FOV36'
        config_list = ['KopEPP07']
        material_step_type = None
        approximation = 'average'

        detect = False
        read = False
        write = True

        for patient in patient_list:
            patient_folder = folder_path + "\\" + patient
            mesh_folder = patient_folder + r"\Mesh"
            for seg in seg_list:
                stl_path = patient_folder + '\\' + patient + "_" + seg + '.stl'
                for element_type in element_type_list:
                    for param in param_list:
                        mesh_base = mesh_folder + "\\" + patient + "_" + seg + "_" + element_type + '_' + str(
                            param).replace('.', '')
                        act_script_path = folder_path + r'\ACT_scripts' + '\\' + patient + '_' + \
                                          seg + '_' + element_type + '_' + str(param).replace('.',
                                                                                              '') + '_act_script.py'
                        wb_script_path = folder_path + r'\WB_scripts' + '\\' + patient + '_' + \
                                         seg + '_' + element_type + '_' + str(param).replace('.',
                                                                                             '') + '_wb_script.wbjn'

                        for step in [10]:
                            for poisson_coef in [[0.3, 'v03']]:
                                try:
                                    save_mesh_path = mesh_base + "_qctma_" + str(step) + poisson_coef[1] + ".cdb"
                                    print(save_mesh_path)
                                    t0 = datetime.datetime.now()
                                    print('\tStarted at : ', t0)
                                    if detect:
                                        detect_endplate(stl_path, sample=3000, distance=0.2, plot=1, endplate_height=2.5)
                                    if read:
                                        read_pstf_vertebra(stl_path.replace('stl', 'pstf'), 1)
                                    if write:
                                        print(save_mesh_path)
                                        mekamesh = Mekamesh(ID='', path=save_mesh_path)
                                        mekamesh.read()
                                        add_endplates_ns(mekamesh, stl_path, write=False)

                                        for config in config_list:
                                            create_new_mekamesh_from_mekamesh(mekamesh,
                                                                              config,
                                                                              return_mechanical_law_from_config(config),
                                                                              material_step_type, 0,
                                                                              approximation, write=False)

                                            mekamesh.write()
                                    t1 = datetime.datetime.now()
                                    print('\tDuration : ', t1 - t0)
                                except FileNotFoundError as e:
                                    print('#####ERROR: ', e)
                                    pass

if __name__ == '__main__':
    main()