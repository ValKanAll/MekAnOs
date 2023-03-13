import numpy as np
from Readers.cdb_reader import read_cdbfile_return_dict_element_density


def read_volume_file(path, return_dict=False):
    volume_list = []
    volume_dict = {}
    with open(path, 'r', errors="ignore") as f:
        line = f.readline()
        while line:
            try:
                if return_dict:
                    volume_dict[int(line.split('\n')[0].split('\t')[0])] = float(line.split('\n')[0].split('\t')[1])
                else:
                    volume_list.append(float(line.split('\n')[0].split('\t')[1]))
            except ValueError:
                pass
            line = f.readline()
    f.close()
    if return_dict:
        return volume_dict
    else:
        return np.array(volume_list)


def main():

    is_JPR = False
    is_WL = False
    is_Artorg = False
    is_MCC = False
    is_IBHGC = True

    if is_Artorg:
        # time.sleep(3600)
        folder_path = r'E:\Artorg_data_2021_metastatic_vertebrae'

        sample_list = ['188', '192', '195', '196', '199', '203', '204', '206', '208',
                       '214', '217', '218', '220', '224',
                       '225', '226', '230', '231', '235', '236', '240', '248', '252', '256', '257', '260', '261', '264',
                       '268', '269', '273', '280', '281', '284', '285', '288', '289', '295', '298', '299',
                       '301', '305',
                       '308', '309', '317'
                       ]
        element_type_list = ['QT']
        size_list = ['1']
        location = 'VB'
        resolution = '294mic'
        seg_list = ['VA',
                    # 'A'
                    ]
        config = 'KopEPP15'
        material_step_type = None  # "equal_material_proportion"
        material_step = 10  # number of materials
        approximation = 'average'
        qctma_step = '10'

        for sample in sample_list:
            for seg in seg_list:
                for element_type in element_type_list:
                    for param in size_list:
                        if material_step_type:
                            base = sample + '_' + resolution + '_' + \
                                   location + '_' + seg + '_' + element_type + '_' + param + '_qctma_' + qctma_step + 'v03_' \
                                   + material_step_type + '_' + config + '_' + str(material_step)
                        else:
                            base = sample + '_' + resolution + '_' + \
                                   location + '_' + seg + '_' + element_type + '_' + param + '_qctma_' + qctma_step + 'v03_100MPa' \
                                   + '_' + config
                        act_script_path = folder_path + r'\ACT_scripts' + '\\' + base + '_act_script.py'
                        result_reaction_file = folder_path + '\\' + 'results_1mm3_EPP15_100MPa_2p100_VA.txt'
                        mekamesh_save_path = folder_path + '\\' + sample + '\\' + base + '.cdb'
                        stl_path = folder_path + '\\' + sample + '\\' + sample + '_' + resolution + '_' + \
                                   location + '_' + seg + '.stl'
                        # print(stl_path)
                        # print(act_script_path)
                        print(mekamesh_save_path)
                        volume_path = folder_path + '\\' + r'volume\\' + base + '_volume.txt'
                        volume_dict = read_volume_file(volume_path, return_dict=True)

                        mesh_path = folder_path + "\\" + sample + "\\" + base + ".cdb"
                        density_dict, material_list = read_cdbfile_return_dict_element_density(mesh_path)

                        volume_tot = 0
                        BMC = 0

                        for element_ID in range(1, len(volume_dict)):
                            try:
                                volume_tot += volume_dict[element_ID]
                                BMC += volume_dict[element_ID] * density_dict[element_ID]
                            except KeyError:
                                print('ERROR: ', element_ID, len(volume_dict))

                        BMD = BMC / volume_tot
                        volume_mean = volume_tot / len(volume_dict)

                        file_analysis = open(folder_path + "\\" + "density_analysis.txt", 'a')
                        file_analysis.write(base + '\t' + str(volume_mean)
                                            + '\t' + str(volume_tot)
                                            + '\t' + str(BMC)
                                            + '\t' + str(len(volume_dict))
                                            + '\t' + str(len(material_list))
                                            + '\t' + str(BMD) + '\n')
                        file_analysis.close()

    if is_JPR:
        folder_path = "E:\Data_L3"
        patient_list = ['01_2007',
                        '02_2007',
                        '07_2007', '08_2007',
                        '11_2007',
                        '12_2007', '13_2007', '15_2007', '16_2007',
                        '17_2007',
                        '18_2007', '19_2007', '20_2007',
                        '03', '31',

                        '32',
                        '35', '37', '40', '43', '44'
                        ]
        element_type_list = ['QT']
        param_list = ['1',
                      #'02', '05', '08', '1', '2'
            #'10k', '20k', '50k', '100k', '200k', '500k'
                      ]
        seg_list = ['VB']
        resolution_list = ['984mic']
        qctma_step_list = [10,
                           #10, 20, 50, 100, 200, 500
                           ]
        software = 'qctma'

        for patient in patient_list:
            for resolution in resolution_list:
                for seg in seg_list:
                    for element_type in element_type_list:
                        for param in param_list:
                            base = patient + "_" + resolution + "_" + seg + "_" + element_type + '_' + param
                            volume_path = folder_path + '\\' + r'volume\\' + patient + "_" + resolution + "_" + seg + "_" + element_type + '_' + param + '_volume.txt'
                            volume_dict = read_volume_file(volume_path, return_dict=True)
                            for qctma_step in qctma_step_list:
                                mesh_base = base + '_' + software + '_' + str(qctma_step) + 'v03'
                                print(mesh_base)
                                mesh_path = folder_path + "\\" + patient + "\\" + patient + "_" + resolution + r"\Mesh" + "\\" + mesh_base + ".cdb"
                                density_dict, material_list = read_cdbfile_return_dict_element_density(mesh_path)

                                volume_tot = 0
                                BMC = 0

                                for element_ID in range(1, len(volume_dict)):
                                    try:
                                        volume_tot += volume_dict[element_ID]
                                        BMC += volume_dict[element_ID]*density_dict[element_ID]
                                    except KeyError:
                                        print('ERROR: ', element_ID, len(volume_dict))

                                BMD = BMC/volume_tot
                                volume_mean = volume_tot/len(volume_dict)

                                file_analysis = open(folder_path + "\\" + "density_analysis_1mm3.txt", 'a')
                                file_analysis.write(mesh_base + '\t' + str(volume_mean)
                                                           + '\t' + str(volume_tot)
                                                           + '\t' + str(BMC)
                                                    + '\t' + str(len(volume_dict))
                                                    + '\t' + str(len(material_list))
                                                           + '\t' + str(BMD) + '\n')
                                file_analysis.close()

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
        param_list = ['1']
        seg_list = [#'HRpQCT_VB',
                    #'def_VB_F_transformed',
                    'def_VB_transformed'
                    ]
        qctma_step_list = ['10']
        software = 'qctma'

        for sample in sample_list:
            for seg in seg_list:
                for element_type in element_type_list:
                    for param in param_list:
                        mesh_base = sample + '_' + seg + '_' + element_type + '_' + param
                        volume_path = folder_path + '\\' + 'Volume\\' + mesh_base + '_volume.txt'
                        volume_dict = read_volume_file(volume_path, return_dict=True)
                        for qctma_step in qctma_step_list:
                            mekamesh_base = mesh_base + '_' + software + '_' + str(qctma_step) + 'v03_100MPa'
                            mekamesh_path = folder_path + '\\' + 'Mekamesh' + '\\' + mekamesh_base + '.cdb'
                            print(mekamesh_base)
                            density_dict, material_list = read_cdbfile_return_dict_element_density(mekamesh_path)

                            volume_tot = 0
                            BMC = 0

                            for element_ID in range(1, len(volume_dict)):
                                try:
                                    volume_tot += volume_dict[element_ID]
                                    BMC += volume_dict[element_ID] * density_dict[element_ID]
                                except KeyError:
                                    print('ERROR: ', element_ID, len(volume_dict))

                            BMD = BMC / volume_tot
                            volume_mean = volume_tot / len(volume_dict)

                            file_analysis = open(folder_path + "\\" + "density_analysis_defect.txt", 'a')
                            file_analysis.write(mesh_base + '\t' + str(volume_mean)
                                                + '\t' + str(volume_tot)
                                                + '\t' + str(BMC)
                                                + '\t' + str(len(volume_dict))
                                                + '\t' + str(len(material_list))
                                                + '\t' + str(BMD) + '\n')
                            file_analysis.close()

    if is_IBHGC:
        folder_path = r'E:\Data_IBHGC'

        sample_list = ['25_L2', '25_L3',
                       '41_L1', '41_L2',
                       '383_L1', '383_L2', '383_L3',
                       '421_L2', '421_L3',
                       '433_L1', '433_L2', '433_L3',
                       '436_L1', '436_L2',
                       '436_L3',
                       '438_L1', '438_L2',
                       '438_L3',
                       '448_L1', '448_L2', '448_L3',
                       '471_L1', '471_L2', '471_L3',
                       '484_L1', '484_L2',
                       '484_L3',
                       '493_L2',
                       '484_L2']

        seg_list = ['VB',
                    # 'VB2'
                    ]
        element_type_list = ['QT']
        param_list = ['1']
        qctma_step_list = ['10']
        config_list = ['KopEPP07']
        material_step_type = None  # "equal_material_proportion"
        material_step = 100  # number of materials
        approximation = 'average'

        for sample in sample_list:
            for seg in seg_list:
                for element_type in element_type_list:
                    for param in param_list:
                        for qctma_step in qctma_step_list:
                            for config in config_list:
                                base = sample + '_' + seg + '_' + element_type + '_' + param + \
                                       '_qctma_' + qctma_step + 'v03_' + config
                                act_script_path_volume = folder_path + r'\ACT_scripts' + '\\' + base + '_volume_act_script.py'
                                wb_script_path_volume = folder_path + r'\WB_scripts' + '\\' + base + '_volume_wb_script.wbjn'
                                mekamesh_save_path = folder_path + '\\' + 'Mekamesh' + '\\' + base + '.cdb'
                                volume_path = folder_path + '\\' + 'volume' + '\\' + base + '_volume.txt'
                                volume_dict = read_volume_file(volume_path, return_dict=True)

                                density_dict, material_list = read_cdbfile_return_dict_element_density(
                                    mekamesh_save_path)

                                volume_tot = 0
                                BMC = 0

                                for element_ID in range(1, len(volume_dict)):
                                    try:
                                        volume_tot += volume_dict[element_ID]
                                        BMC += volume_dict[element_ID] * density_dict[element_ID]
                                    except KeyError:
                                        print('ERROR: ', element_ID, len(volume_dict))

                                BMD = BMC / volume_tot
                                volume_mean = volume_tot / len(volume_dict)

                                file_analysis = open(folder_path + "\\" + "density_analysis.txt", 'a')
                                file_analysis.write(base + '\t' + str(volume_mean)
                                                    + '\t' + str(volume_tot)
                                                    + '\t' + str(BMC)
                                                    + '\t' + str(len(volume_dict))
                                                    + '\t' + str(len(material_list))
                                                    + '\t' + str(BMD) + '\n')
                                file_analysis.close()

    if is_MCC:
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
        config_list = ['KopEPP07']
        qctma_step_list = ['10']
        software = 'qctma'
        material_step_type = None  # "equal_material_proportion"
        material_step = 100  # number of materials
        approximation = 'average'

        for patient in patient_list:
            for seg in seg_list:
                for element_type in element_type_list:
                    for param in param_list:
                        for qctma_step in qctma_step_list:
                            for config in config_list:
                                if material_step_type:
                                    base = patient + '_' + seg + '_' + element_type + '_' + str(param).replace(',',
                                                                                                               '.') + '_qctma_' + qctma_step + 'v03_' \
                                           + material_step_type + '_' + config + '_' + str(material_step)
                                else:
                                    base = patient + '_' + seg + '_' + element_type + '_' + str(param).replace(',',
                                                                                                               '.') + '_qctma_' + qctma_step + 'v03_' + config

                                mekamesh_path = folder_path + '\\' + patient + '\\' + 'Mesh' + '\\' + base + '.cdb'
                                volume_path = folder_path + '\\' + 'volume' + '\\' + base + '_volume.txt'
                                volume_dict = read_volume_file(volume_path, return_dict=True)

                                density_dict, material_list = read_cdbfile_return_dict_element_density(
                                    mekamesh_path)

                                volume_tot = 0
                                BMC = 0

                                for element_ID in range(1, len(volume_dict)):
                                    try:
                                        volume_tot += volume_dict[element_ID]
                                        BMC += volume_dict[element_ID] * density_dict[element_ID]
                                    except KeyError:
                                        print('ERROR: ', element_ID, len(volume_dict))

                                BMD = BMC / volume_tot
                                volume_mean = volume_tot / len(volume_dict)

                                file_analysis = open(folder_path + "\\" + "density_analysis.txt", 'a')
                                file_analysis.write(base + '\t' + str(volume_mean)
                                                    + '\t' + str(volume_tot)
                                                    + '\t' + str(BMC)
                                                    + '\t' + str(len(volume_dict))
                                                    + '\t' + str(len(material_list))
                                                    + '\t' + str(BMD) + '\n')
                                file_analysis.close()


if __name__ == '__main__':
    main()