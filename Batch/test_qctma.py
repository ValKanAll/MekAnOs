from qctma import qctma
import numpy as np
import math


def gl2density(intercept, slope, no_min=False):
    def f(gl_mat):
        s = gl_mat.shape
        rho_mat = np.zeros(s)
        for i in range(s[0]):
            if len(s) >= 2:
                for j in range(s[1]):
                    if len(s) == 3:
                        for k in range(s[2]):
                            if no_min:
                                rho_mat[i, j, k] = intercept + slope * gl_mat[i, j, k]
                            else:
                                rho_mat[i, j, k] = max(0, intercept + slope * gl_mat[i, j, k])
                    else:
                        if no_min:
                            rho_mat[i, j] = intercept + slope * gl_mat[i, j]
                        else:
                            rho_mat[i, j] = max(0, intercept + slope * gl_mat[i, j])
            else:
                if no_min:
                    rho_mat[i] = intercept + slope * gl_mat[i]
                else:
                    rho_mat[i] = max(0, intercept + slope * gl_mat[i])

        return rho_mat
    return f


gl2density_JPR_HRpQCT = gl2density(-0.35746, 0.0001773)
gl2density_WL_HRpQCT_predefect = gl2density(-0.3503, 0.000176797)
gl2density_WL_QCT_predefect = gl2density(-0.0308734, 0.000656626)
#gl2density_WL_QCT_predefect_corrected = gl2density(-0.0, 0.001, no_min=True)
#gl2density_WL_QCT_postdefect = gl2density(-0.052869324, 0.000640576)
#gl2density_WL_QCT_postdefect_corrected = gl2density(-0.052869324 + 1024*0.000640576, 0.000640576)
gl2density_ARTORG_HRpQCT = gl2density(-191.56*0.001, 369.154/4096*0.001)
gl2density_IBHQC = gl2density(0, 1)
gl2density_MCC = gl2density(0.01745, 0.0006855)


def density2E(_min_E=1):
    def dens2E(rho_mat, with_min=True, _min_E=1,
                  intercept=-34.7, slope=3230, c=1):
        s = rho_mat.shape
        E_mat = np.zeros(s)

        for i in range(len(rho_mat)):
            if len(s) >= 2:
                for j in range(s[1]):
                    if len(s) == 3:
                        for k in range(s[2]):
                            if with_min:
                                E_mat[i, j, k] = max(intercept + slope * rho_mat[i, j, k] ** c, _min_E)
                            else:
                                E_mat[i, j, k] = intercept + slope * rho_mat[i, j, k] ** c
                    else:
                        if with_min:
                            E_mat[i, j] = max(intercept + slope * rho_mat[i, j] ** c, _min_E)
                        else:
                            E_mat[i, j] = intercept + slope * rho_mat[i, j] ** c
            else:
                if with_min:
                    E_mat[i] = max(intercept + slope * rho_mat[i] ** c, _min_E)
                else:
                    E_mat[i] = intercept + slope * rho_mat[i] ** c

        return E_mat

    return dens2E


def E2density(E_mat, min_rho=0.000001, intercept=-34.7, slope=3230, c=1):
    rho_mat = []

    for i in range(len(E_mat)):
        rho_mat.append(((E_mat[i] - intercept) / slope) ** (1/c))
        #rho_mat.append(max(((E_mat[i] - intercept) / slope) ** (1/c), min_rho))

    return rho_mat


if __name__ == '__main__':
    is_JPR_HRpQCT = True

    is_WL_QCT_postdefect = False
    is_WL_HRpQCT_predefect = False
    is_WL_QCT_predefect = False

    is_Artorg_HRpQCT = False
    is_WL = False

    is_IBHGC = False

    is_MCC = False

    error_list = []

    if is_JPR_HRpQCT:
        import time
        time.sleep(1*3600)
        sample_list = ['01_2007',
             '02_2007',
                        '07_2007', '08_2007', '11_2007', '12_2007',
                        '13_2007', '15_2007',
            '16_2007',

            '17_2007',
                    '18_2007', '19_2007',
            '20_2007',
                        '03', '31', '32', '35', '37', '40', '43', '44'
                        ]
        for patient in sample_list:
            resolution_list = [#"984mic",
                                   "656mic",
                                   #"328mic"
                                   ]
            seg_list = ["VB",
                        "VB2",
                        #"VB_AL",
                        #"VB_EC"
                        #"VB_SA"
            ]

            for resolution in resolution_list:
                for seg in seg_list:
                    for param in [#'QT_0328',
                        #'QT_0219',
                        #'QT_0109',
                        #'QT_035',
                          # 'QT_08',
                          #'QT_02', 'QT_05',
                        'QT_1',
                        # 'QT_2'
                            ]:

                        dcm_path = "E:\Data_L3\\" + patient + "\\" + patient + "_" + resolution + "\\" + patient + "_" + resolution + "_DICOM"
                        image_path = "E:\Data_L3\\" + patient + "\\" + patient + "_" + resolution + "\\" + patient + "_" + resolution + ".nrrd"
                        mesh_path = "E:\Data_L3\\" + patient + "\\" + patient + "_" + resolution + "\Mesh\\" + patient + "_" + resolution + "_" + seg + "_" + param + ".cdb"
                        mesh_base = "E:\Data_L3\\" + patient + "\\" + patient + "_" + resolution + "\Mesh\\" + patient + "_" + resolution + "_" + seg + "_" + param

                        for step in [#5,
                                     10,
                                     #20, 50, 100, 200, 500
                                     ]:
                            for poisson_coef in [[0.3, 'v03']]:
                                save_mesh_path = mesh_base + "_qctma_" + str(step) + poisson_coef[1] + ".cdb"
                                print(save_mesh_path)
                                try:
                                    qctma(dcm_path, None, mesh_path, gl2density_JPR_HRpQCT, density2E(), E2density, step,
                                      poisson_coef[0], True,
                                      save_mesh_path)
                                except FileNotFoundError:
                                    error_list.append(mesh_base)

    if is_WL_QCT_postdefect:
        for patient in ['01_2005_L1',
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
                        ]:
            for param in [
                # 'QT_10k', 'QT_20k', 'QT_50k', 'QT_100k', 'QT_200k', 'QT_400k', 'QT_500k', 'QT_600k', 'QT_700k',
                'QT_100k'#, 'QT_1mm', 'QV_1mm'
            ]:
                resolution = "def"
                dcm_path = "D:\Data_post-defect_2021-05-18\\" + patient + "_" + resolution + "\\Dicom"
                mesh_path = "D:\Data_post-defect_2021-05-18\\" + patient + "_" + resolution + "\Mesh\\" + patient + "_def_VB_" + param + ".cdb"
                mesh_base = mesh_path.split('.cdb')[0]

                for step in [10]:
                    # v03
                    save_mesh_path = "D:\Data_post-defect_2021-05-18\\" + patient + "_" + resolution + "\Mesh\\" + patient + "_def_VB_" + param + "_qctma_" + str(
                        step) + "v03NC.cdb"
                    print(save_mesh_path)
                    qctma(dcm_path, mesh_path, gl2density_WL_QCT_postdefect, density2E, E2density, step, 0.3, True, save_mesh_path, )

    if is_WL_HRpQCT_predefect:
        for patient in ['01_2005_L1',
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
                        ]:
            for param in [
                # 'QT_10k', 'QT_20k', 'QT_50k', 'QT_100k', 'QT_200k', 'QT_400k', 'QT_500k', 'QT_600k', 'QT_700k',
                #'QT_1mm',
                'QV_1mm',
                #'QH_1mm'
            ]:
                resolution_list = ["410mic", "738mic"]
                for resolution in resolution_list:
                    dcm_path = "E:\Data_pre-defect_HRpQCT\\" + patient + "\\Dicom_" + resolution
                    mesh_path = "E:\Data_pre-defect_HRpQCT\\" + patient + "\Mesh\\" + patient + "_" + resolution + "_VB_" + param + ".cdb"

                    gaussian_filter_sigma = 0
                    for step in [10]:
                        # v03
                        save_mesh_path = "E:\Data_pre-defect_HRpQCT\\" + patient + "\Mesh\\" + patient + "_" + resolution + "_VB_" + param + "_qctma_" + str(
                            step) + "v03.cdb"
                        print(save_mesh_path)
                        qctma(dcm_path, mesh_path, gl2density_WL_HRpQCT_predefect, density2E, E2density, step, 0.3, True, save_mesh_path, 1, gaussian_filter_sigma)

    if is_WL:
        for patient in ['01_2005_L1',
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
                        ]:
            for param in [
                 #'QT_10k', 'QT_20k', 'QT_50k',
                #'QT_100k',
                #'QT_200k', 'QT_400k', 'QT_500k', 'QT_600k', 'QT_700k',
                #'QT_1mm',
                #'QV_1mm',
                #'QH_1mm'
                #'QT_08',
                #'QT_02', 'QT_03', 'QT_05', 'QT_1'
                #'QT_005', 'QT_01'
                'QT_1'
            ]:
                resolution_list = ["410mic"]#, "738mic"]
                seg_list = ['HRpQCT_VB', 'def_VB_F_transformed',
                            'def_VB_transformed']

                for resolution in resolution_list:
                    for seg in seg_list:
                        dcm_path = "E:\Data_pre-defect_HRpQCT\\" + patient + "\\Dicom_" + resolution
                        mesh_path = "E:\Data_WL\Mesh\\" + patient + "_" + seg + "_" + param + ".cdb"

                        gaussian_filter_sigma = 0
                        for step in [10]:
                            # v03
                            save_mesh_path = "E:\Data_WL\Mekamesh\\" + patient + "_" + seg + "_" + param + "_qctma_" + str(
                                step) + "v03_100MPa.cdb"
                            print(save_mesh_path)
                            qctma(dcm_path, None, mesh_path, gl2density_WL_HRpQCT_predefect, density2E, E2density, step,
                                  0.3, True,
                                  save_mesh_path)

    if is_IBHGC:
        sample_list = ['25_L2', '25_L3',
                       '41_L1', '41_L2',
                       '383_L1', '383_L2', '383_L3',
                       '421_L2', '421_L3',
                       '433_L1', '433_L2', '433_L3',
                       '436_L1', '436_L2', '436_L3',
                       '438_L1', '438_L2', '438_L3',
                       '448_L1', '448_L2',
            '448_L3',
                       '471_L1', '471_L2', '471_L3',
                       '484_L1', '484_L2', '484_L3',
                       '493_L2']
        folder_path = "E:\Data_IBHGC"
        min_E = 1

        for sample in sample_list:
            for param in [
                'QT_1', 'QT_2',
            ]:
                seg_list = ['VB',
                            #'VB2'
                            ]
                for seg in seg_list:
                        nrrd_path = folder_path + "\\Seg_VB\\Seg_" + sample[:-3] + "_VB.nrrd"
                        mesh_path = folder_path + "\\Mesh\\" + sample + "_" + seg + "_" + param + ".cdb"

                        gaussian_filter_sigma = 0
                        for step in [10]:
                            # v03
                            save_mesh_path = folder_path + "\\Mekamesh\\" + sample + "_" + seg + "_" + param + "_qctma_" + str(
                                step) + "v03.cdb"
                            if min_E:
                                save_mesh_path = folder_path + "\\Mekamesh\\" + sample + "_" + seg + "_" + param + "_qctma_" + str(
                                    step) + "min" + str(min_E) + ".cdb"
                            print(save_mesh_path)
                            qctma(None, nrrd_path, mesh_path, gl2density_IBHQC, density2E(min_E), E2density, step,
                                  0.3, True,
                                  save_mesh_path)

    if is_WL_QCT_predefect:
        for patient in ['01_2005_L1',
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
                        ]:
            for param in [
                # 'QT_10k', 'QT_20k', 'QT_50k', 'QT_100k', 'QT_200k', 'QT_400k', 'QT_500k', 'QT_600k', 'QT_700k',
                'QV_1mm',
                #'QT_1mm'
                #'QH_1mm'
            ]:
                resolution_list = ["FOV20", "FOV38"]#, "FOV38"]
                for resolution in resolution_list:
                    dcm_path = "E:\Data_pre-defect_2021-03-19\\L1\\" + patient + '\\' + resolution + "\\QCT"
                    mesh_path = "E:\Data_pre-defect_2021-03-19\\L1\\" + patient + '\\' + resolution + "\Mesh\\" + patient + "_" + resolution + "_VB_" + param + ".cdb"

                    gaussian_filter_sigma = 1
                    for step in [10]:
                        # v03
                        save_mesh_path = "E:\Data_pre-defect_2021-03-19\\L1\\" + patient + '\\' + resolution + "\Mesh\\" + patient + "_" + resolution + "_VB_" + param + "_qctma_" + str(
                            step) + "v03C.cdb"
                        print(save_mesh_path)
                        qctma(dcm_path, mesh_path, gl2density_WL_QCT_predefect_corrected, density2E, E2density, step, 0.3, True, save_mesh_path, 1, gaussian_filter_sigma)

    if is_Artorg_HRpQCT:
        sample_list = ['188', '192', '195', '196', '199', '203', '204', '206', '208', '214', '217', '218', '220', '224',
                   '225', '226', '230', '231', '235', '236', '240', '248', '252', '256', '257', '260', '261', '264',
                   '268', '269', '273', '280', '281', '284', '285', '288', '289', '295', '298', '299', '301', '305',
                   '308', '309', '317']
        element_type_list = ['QT']
        param_list = ['1']#'10k', '20k', '50k', '100k', '200k', '500k']
        location = 'VB'
        resolution = '294mic'
        seg_list = [#'VA',
                    'A']#, 'VA']
        res = 0.294

        for sample in ['309']:
            for seg in seg_list:
                for element_type in element_type_list:
                    for param in param_list:
                        try:
                            act_script_path = r'E:\Artorg_data_2021_metastatic_vertebrae\ACT_scripts' + '\\' + sample + '_' + resolution + '_' + \
                                              location + '_' + seg + '_' + element_type + '_' + param + '_' + 'act_script.py'
                            mesh_path = r'E:\Artorg_data_2021_metastatic_vertebrae' + '\\' + sample + '\\' + sample + '_' + resolution + '_' + \
                                             location + '_' + seg + '_' + element_type + '_' + param + '.cdb'
                            stl_path = r'E:\Artorg_data_2021_metastatic_vertebrae' + '\\' + sample + '\\' + sample + '_' + resolution + '_' + \
                                       location + '_' + seg + '.stl'
                            mesh_base = r'E:\Artorg_data_2021_metastatic_vertebrae' + '\\' + sample + '\\' + sample + '_' + resolution + '_' + \
                                             location + '_' + seg + '_' + element_type + '_' + param
                            dcm_path = r'E:\Artorg_data_2021_metastatic_vertebrae' + '\\' + sample + '\\' + sample + '_' + resolution + '_DICOM'

                            '''for size in [0]:#[1, 3, 5, 10]:
                                for step in [10]:
                                    for poisson_coef in [[0.3, 'v03']]:
                                        window_kernel = math.floor(size / res)
                                        gaussian_smoothing_sigma = window_kernel // 3
                                        save_mesh_path = mesh_base + "_qctma_" + str(step) + poisson_coef[1] + '_GS_' + str(size) + ".cdb"
                                        print(save_mesh_path)
                                        qctma(dcm_path, mesh_path, gl2density_ARTORG_HRpQCT, density2E, E2density, step, poisson_coef[0], True,
                                              save_mesh_path, 1, gaussian_smoothing_sigma, window_kernel)'''
                            for step in [10]:
                                for poisson_coef in [[0.3, 'v03']]:
                                    save_mesh_path = mesh_base + "_qctma_" + str(step) + poisson_coef[1] + "_100MPa.cdb"
                                    print(save_mesh_path)
                                    qctma(dcm_path, None, mesh_path, gl2density_ARTORG_HRpQCT, density2E, E2density, step,
                                          poisson_coef[0], True,
                                          save_mesh_path, 1)

                        except FileNotFoundError:
                            print('$$$$$$$$FAIL$$$$$$$', mesh_base)


    for error in error_list:
        print(error)


if is_MCC:  # Mekanos clinical cases
    #time.sleep(3600)
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


    for patient in patient_list:
        patient_folder = folder_path + "\\" + patient
        mesh_folder = patient_folder + r"\Mesh"
        for seg in seg_list:
            stl_path = patient_folder + '\\' + patient + "_" + seg + '.stl'
            for element_type in element_type_list:
                for param in param_list:
                    mesh_base = mesh_folder + "\\" + patient + "_" + seg + "_" + element_type + '_' + str(param).replace('.', '')
                    act_script_path = folder_path + r'\ACT_scripts' + '\\' + patient + '_' +\
                        seg + '_' + element_type + '_' + str(param).replace('.', '') + '_act_script.py'
                    wb_script_path = folder_path + r'\WB_scripts' + '\\' + patient + '_' + \
                                     seg + '_' + element_type + '_' + str(param).replace('.', '') + '_wb_script.wbjn'
                    mesh_path = mesh_base + ".cdb"

                    dcm_path = folder_path + '\\' + patient + '\\' + patient + '_' + resolution + '_DICOM\\DICOM'

                    for step in [10]:
                        for poisson_coef in [[0.3, 'v03']]:
                            save_mesh_path = mesh_base + "_qctma_" + str(step) + poisson_coef[1] + ".cdb"
                            print(save_mesh_path)
                            qctma(dcm_path, None, mesh_path, gl2density_MCC, density2E, E2density, step,
                                  poisson_coef[0], True,
                                  save_mesh_path, 1)


