from qctma import qctma
import numpy as np



def gl2density_JPR(gl_mat):
    s = gl_mat.shape
    rho_mat = np.zeros(s)
    intercept = -0.35746
    slope = 0.0001773
    for i in range(s[0]):
        if len(s) >= 2:
            for j in range(s[1]):
                if len(s) == 3:
                    for k in range(s[2]):
                        rho_mat[i, j, k] = intercept + slope * gl_mat[i, j, k]
                else:
                    rho_mat[i, j] = intercept + slope * gl_mat[i, j]
        else:
            rho_mat[i] = intercept + slope * gl_mat[i]

    return rho_mat


def gl2density_HRpQCT_WL_predefect(gl_mat):
    s = gl_mat.shape
    rho_mat = np.zeros(s)
    intercept = -0.3503
    slope = 0.000176797
    for i in range(s[0]):
        if len(s) >= 2:
            for j in range(s[1]):
                if len(s) == 3:
                    for k in range(s[2]):
                        rho_mat[i, j, k] = intercept + slope * gl_mat[i, j, k]
                else:
                    rho_mat[i, j] = intercept + slope * gl_mat[i, j]
        else:
            rho_mat[i] = intercept + slope * gl_mat[i]

    return rho_mat


def gl2density_QCT_WL_predefect(gl_mat):
    s = gl_mat.shape
    rho_mat = np.zeros(s)
    intercept = -0.0308734
    slope = 0.000656626
    for i in range(s[0]):
        if len(s) >= 2:
            for j in range(s[1]):
                if len(s) == 3:
                    for k in range(s[2]):
                        rho_mat[i, j, k] = intercept + slope * gl_mat[i, j, k]
                else:
                    rho_mat[i, j] = intercept + slope * gl_mat[i, j]
        else:
            rho_mat[i] = intercept + slope * gl_mat[i]

    return rho_mat

def gl2density_WL(gl_mat):
    s = gl_mat.shape
    rho_mat = np.zeros(s)
    intercept = -0.052869324
    slope = 0.000640576
    for i in range(s[0]):
        if len(s) >= 2:
            for j in range(s[1]):
                if len(s) == 3:
                    for k in range(s[2]):
                        rho_mat[i, j, k] = intercept + slope * gl_mat[i, j, k]
                else:
                    rho_mat[i, j] = intercept + slope * gl_mat[i, j]
        else:
            rho_mat[i] = intercept + slope * gl_mat[i]

    return rho_mat


def gl2density_ARTORG(gl_mat):
    s = gl_mat.shape
    rho_mat = np.zeros(s)
    intercept = -191.56*0.001
    slope = 369.154/4096*0.001
    for i in range(s[0]):
        if len(s) >= 2:
            for j in range(s[1]):
                if len(s) == 3:
                    for k in range(s[2]):
                        rho_mat[i, j, k] = intercept + slope * gl_mat[i, j, k]
                else:
                    rho_mat[i, j] = intercept + slope * gl_mat[i, j]
        else:
            rho_mat[i] = intercept + slope * gl_mat[i]

    return rho_mat


def density2E(rho_mat, with_min=True, min_E=0.001):
    s = rho_mat.shape
    E_mat = np.zeros(s)
    intercept = -34.7
    slope = 3230
    c = 1

    for i in range(len(rho_mat)):
        if len(s) >= 2:
            for j in range(s[1]):
                if len(s) == 3:
                    for k in range(s[2]):
                        if with_min:
                            E_mat[i, j, k] = max(intercept + slope * rho_mat[i, j, k] ** c, min_E)
                        else:
                            E_mat[i, j, k] = intercept + slope * rho_mat[i, j, k] ** c
                else:
                    if with_min:
                        E_mat[i, j] = max(intercept + slope * rho_mat[i, j] ** c, min_E)
                    else:
                        E_mat[i, j] = intercept + slope * rho_mat[i, j] ** c
        else:
            if with_min:
                E_mat[i] = max(intercept + slope * rho_mat[i] ** c, min_E)
            else:
                E_mat[i] = intercept + slope * rho_mat[i] ** c

    return E_mat


def E2density(E_mat):
    rho_mat = []
    intercept = -34.7
    slope = 3230
    c = 1
    min_rho = 0.000001

    for i in range(len(E_mat)):
        rho_mat.append(((E_mat[i] - intercept) / slope) ** (1/c))
        #rho_mat.append(max(((E_mat[i] - intercept) / slope) ** (1/c), min_rho))

    return rho_mat



if __name__ == '__main__':
    is_JPR = False
    is_WL = False
    is_WL_HRpQCT_predefect = True
    is_WL_QCT_predefect = True
    is_Artorg = False

    if is_JPR:
        for patient in ['01_2007',
             '02_2007', '03', '07_2007', '08_2007', '11_2007', '12_2007',
                        '13_2007', '15_2007', '16_2007', '17_2007',
                        '18_2007', '19_2007', '20_2007',
                        '31', '32', '35', '37', '40', '43', '44'
                        ]:
            for param in [#'QT_10k', 'QT_20k', 'QT_50k', 'QT_100k', 'QT_200k', 'QT_400k', 'QT_500k', 'QT_600k', 'QT_700k',
                'QH_1.5mm', #'QH_1.5mm', 'QH_0.7mm', 'QH_0.5mm'
            ]:
                resolution = "984mic"
                dcm_path = "D:\Data_L3\\" + patient + "\\" + patient + "_" + resolution + "\\" + patient + "_" + resolution + "_DICOM"
                mesh_path = "D:\Data_L3\\" + patient + "\\" + patient + "_" + resolution + "\Mesh\\" + patient + "_984mic_VB_" + param + ".cdb"

                 # 0v03
                #save_mesh_path = "D:\Data_L3\\" + patient + "\\" + patient + "_" + resolution + "\Mesh\\" + patient + "_984mic_VB_QT_" + str(
                #    nb_element) + "k_qctma_0v03.cdb"
                #qctma(dcm_path, mesh_path, gl2density, density2E, E2density, 0, 0.3, True, save_mesh_path)


                for step in [10]:
                # v03
                    #save_mesh_path = "D:\Data_L3\\" + patient + "\\" + patient + "_" + resolution + "\Mesh\\" + patient + "_984mic_VB_" + param + "_qctma_" + str(step) + "v03.cdb"
                    #qctma(dcm_path, mesh_path, gl2density, density2E, E2density, step, 0.3, True, save_mesh_path)

                # v04
                    save_mesh_path = "D:\Data_L3\\" + patient + "\\" + patient + "_" + resolution + "\Mesh\\" + patient + "_984mic_VB_" + param + "_qctma_" + str(step) + "v04.cdb"
                    qctma(dcm_path, mesh_path, gl2density_JPR, density2E, E2density, step, 0.4, True, save_mesh_path)

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
                # 'QT_10k', 'QT_20k', 'QT_50k', 'QT_100k', 'QT_200k', 'QT_400k', 'QT_500k', 'QT_600k', 'QT_700k',
                'QV_1mm'#, 'QT_1mm', 'QV_1mm'
            ]:
                resolution = "def"
                dcm_path = "D:\Data_post-defect_2021-05-18\\" + patient + "_" + resolution + "\\Dicom"
                mesh_path = "D:\Data_post-defect_2021-05-18\\" + patient + "_" + resolution + "\Mesh\\" + patient + "_def_VB_" + param + ".cdb"

                # 0v03
                # save_mesh_path = "D:\Data_L3\\" + patient + "\\" + patient + "_" + resolution + "\Mesh\\" + patient + "_984mic_VB_QT_" + str(
                #    nb_element) + "k_qctma_0v03.cdb"
                # qctma(dcm_path, mesh_path, gl2density, density2E, E2density, 0, 0.3, True, save_mesh_path)
                gaussian_filter_sigma = 1
                for step in [0]:
                    # v03
                    save_mesh_path = "D:\Data_post-defect_2021-05-18\\" + patient + "_" + resolution + "\Mesh\\" + patient + "_def_VB_" + param + "_qctma_" + str(
                        step) + "v03.cdb"
                    print(save_mesh_path)
                    qctma(dcm_path, mesh_path, gl2density_WL, density2E, E2density, step, 0.3, True, save_mesh_path, gaussian_filter_sigma)

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
                'QT_1mm',
                'QV_1mm',
                'QH_1mm'
            ]:
                resolution_list = ["410mic", "738mic"]
                for resolution in resolution_list:
                    dcm_path = "E:\Data_pre-defect_HRpQCT\\" + patient + "\\Dicom_" + resolution
                    mesh_path = "E:\Data_pre-defect_HRpQCT\\" + patient + "\Mesh\\" + patient + "_" + resolution + "_VB_" + param + ".cdb"

                    gaussian_filter_sigma = 1
                    for step in [10]:
                        # v03
                        save_mesh_path = "E:\Data_pre-defect_HRpQCT\\" + patient + "\Mesh\\" + patient + "_" + resolution + "_VB_" + param + "_qctma_" + str(
                            step) + "v03.cdb"
                        print(save_mesh_path)
                        qctma(dcm_path, mesh_path, gl2density_HRpQCT_WL_predefect, density2E, E2density, step, 0.3, True, save_mesh_path, gaussian_filter_sigma)

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
                'QV_1mm', 'QT_1mm', 'QH_1mm'
            ]:
                resolution_list = ["FOV20", "FOV38"]#, "FOV38"]
                for resolution in resolution_list:
                    dcm_path = "E:\Data_pre-defect_2021-03-19\\L1\\" + patient + '\\' + resolution + "\\QCT"
                    mesh_path = "E:\Data_pre-defect_2021-03-19\\L1\\" + patient + '\\' + resolution + "\Mesh\\" + patient + "_" + resolution + "_VB_" + param + "_endplates.cdb"

                    gaussian_filter_sigma = 1
                    for step in [10]:
                        # v03
                        save_mesh_path = "E:\Data_pre-defect_2021-03-19\\L1\\" + patient + '\\' + resolution + "\Mesh\\" + patient + "_" + resolution + "_VB_" + param + "_qctma_" + str(
                            step) + "v03.cdb"
                        print(save_mesh_path)
                        qctma(dcm_path, mesh_path, gl2density_QCT_WL_predefect, density2E, E2density, step, 0.3, True, save_mesh_path, gaussian_filter_sigma)

    if is_Artorg:
        sample_list = ['195', '196', '199', '203', '204', '206', '208', '214', '217', '218', '220', '224',
                       '225', '226', '230', '231', '235', '236', '240', '248', '252', '256', '257', '260', '261', '264',
                       '268', '269', '273', '280', '281', '284', '285', '288', '289', '295', '298', '299', '301', '305',
                       '308', '309', '317']
        element_type_list = ['QT']
        size_list = ['1']
        location = 'VB'
        resolution = '294mic'
        seg_list = ['A', 'VA']

        for sample in sample_list:
            for seg in seg_list:
                for element_type in element_type_list:
                    for size in size_list:
                        try:
                            act_script_path = r'E:\Artorg_data_2021_metastatic_vertebrae\ACT_scripts' + '\\' + sample + '_' + resolution + '_' + \
                                              location + '_' + seg + '_' + element_type + '_' + size + 'mm_' + 'act_script.py'
                            mesh_path = r'E:\Artorg_data_2021_metastatic_vertebrae' + '\\' + sample + '\\' + sample + '_' + resolution + '_' + \
                                             location + '_' + seg + '_' + element_type + '_' + size + 'mm.cdb'
                            stl_path = r'E:\Artorg_data_2021_metastatic_vertebrae' + '\\' + sample + '\\' + sample + '_' + resolution + '_' + \
                                       location + '_' + seg + '.stl'
                            mesh_base = r'E:\Artorg_data_2021_metastatic_vertebrae' + '\\' + sample + '\\' + sample + '_' + resolution + '_' + \
                                             location + '_' + seg + '_' + element_type + '_' + size + 'mm'
                            dcm_path = r'E:\Artorg_data_2021_metastatic_vertebrae' + '\\' + sample + '\\' + sample + '_' + resolution + '_DICOM'

                            for step in [10]:
                                for poisson_coef in [[0.3, 'v03']]:
                                    save_mesh_path = mesh_base + "_qctma_" + str(step) + poisson_coef[1] + ".cdb"
                                    print(save_mesh_path)
                                    qctma(dcm_path, mesh_path, gl2density_ARTORG, density2E, E2density, step, poisson_coef[0], True, save_mesh_path)

                        except FileNotFoundError:
                            print('$$$$$$$$FAIL$$$$$$$', mesh_base)
