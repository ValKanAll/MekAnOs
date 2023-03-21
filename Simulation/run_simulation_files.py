import subprocess
import datetime
import ANSYS_default_scripts.act_scripts as act_scripts
import ANSYS_default_scripts.wb_scripts as wb_scripts
import time

from simulation_functions import (get_height,
                                  simu_EPP, simu_EPP_all_times, simu_EL, simu_get_volume,
                                  simu_gen_mesh_from_elemental_volume, simu_EPP_remote_point, simu_EPP_center_remote_point)

from Workflow.Choose_database import *


if is_JPR:
    cmd_workbench_template = r"D:\Batch_ansys\ANSYS_default_scripts\config_workbench_template.wbjn"
    script_act_template = r"C:\Users\U1033_BIOMECA\Desktop\Data_JPR\density_law_fitting\template\vertebra_analysis_template.py"

    cmd_workbench = r"C:\Users\U1033_BIOMECA\Desktop\Data_JPR\density_law_fitting\config_workbench.wbjn"
    script_act = r"C:\Users\U1033_BIOMECA\Desktop\Data_JPR\density_law_fitting\vertebra_analysis.py"

    sample_list = ['01_2007', '02_2007', '07_2007', '08_2007', '11_2007',
                   '12_2007', '13_2007', '15_2007', '16_2007', '17_2007',
                   '18_2007', '19_2007', '20_2007',
                   '03', '31', '32', '35', '37', '40', '43', '44']
    element_type_list = ['QT']
    poisson_list = ['v03']#, 'v04']
    step_list = [10]
                 #2, 5, 10, 20, 50]
    param_list = ['1mm']#10, 20, 50, 100, 200, 400, 500, 600, 700]
    location = 'VB'
    resolution = '984mic'
    mat_software = 'qctma'

    for sample in sample_list:
        for element_type in element_type_list:
            for step in step_list:
                for param in param_list:
                    for poisson in poisson_list:
                        act_script_path = r'D:\Data_L3\linear_model_sensitivity\Script' + '\\' + sample + '_' + resolution + '_' +\
                            location + '_' + element_type + '_' + param + '_' + mat_software + '_' + str(step) + poisson + '_act_script.py'
                        act_linear_script = act_scripts.act_template_linear
                        act_linear_script = act_linear_script.replace("{element_type}", element_type)
                        act_linear_script = act_linear_script.replace("{sample}", sample)
                        act_linear_script = act_linear_script.replace("{material_law}", str(step)+poisson)
                        act_linear_script = act_linear_script.replace("{param}", param)
                        with open(act_script_path, 'w+') as f:
                            f.write(act_linear_script)

                        wb_script_path = r'D:\Data_L3\linear_model_sensitivity\Script' + '\\' + sample + '_' + resolution + '_' +\
                            location + '_' + element_type + '_' + param + '_' + mat_software + '_' + str(step) + poisson + '_wb_script.wbjn'
                        wb_script_simulation = wb_scripts.wb_script_simulation_default
                        wb_script_simulation = wb_script_simulation.replace("{element_type}", element_type)
                        wb_script_simulation = wb_script_simulation.replace("{sample}", sample)
                        wb_script_simulation = wb_script_simulation.replace("{material_law}", str(step)+poisson)
                        wb_script_simulation = wb_script_simulation.replace("{param}", param)
                        wb_script_simulation = wb_script_simulation.replace("{path_act}", act_script_path)
                        wb_script_simulation = wb_script_simulation.replace("{path_logfile}", r'D:\Data_L3\linear_model_sensitivity\logfile.txt')
                        with open(wb_script_path, 'w+') as f:
                            f.write(wb_script_simulation)
                        try:
                            cmd = r'"C:\Program Files\ANSYS Inc\v211\Framework\bin\Win64\RunWB2.exe"  -B -R "%s"' % wb_script_path
                            print(cmd)
                            subprocess.check_call(cmd, shell=True)
                        except:
                            print("ERROR : %s" % sample)

if is_JPR_volume:
    #time.sleep(3600)
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
    param_list = ['01', '02', '05', '08', '1', '2']# ['10k', '20k', '50k', '100k', '200k', '500k']
    seg_list = ['VB']
    resolution_list = ['984mic']

    for patient in patient_list:
        patient_folder = folder_path + "\\" + patient
        for resolution in resolution_list:
            resolution_folder = patient_folder + "\\" + patient + "_" + resolution
            mesh_folder = resolution_folder + r"\Mesh"
            for seg in seg_list:
                stl_path = resolution_folder + '\\' + patient + "_" + resolution + "_" + seg + '.stl'
                for element_type in element_type_list:
                    for param in param_list:
                        mesh_base = mesh_folder + "\\" + patient + "_" + resolution + "_" + seg + "_" + element_type + '_' + param
                        act_script_path = folder_path + r'\ACT_scripts' + '\\' + patient + '_' + resolution + '_' +\
                            seg + '_' + element_type + '_' + param + '_get_volume_act_script.py'
                        wb_script_path = folder_path + r'\WB_scripts' + '\\' + patient + '_' + resolution + '_' + \
                                         seg + '_' + element_type + '_' + param + '_get_volume_wb_script.wbjn'
                        mesh_path = mesh_base + ".cdb"

                        volume_path = folder_path + '\\' + r'volume\\' + patient + "_" + resolution + "_" + seg + "_" + element_type + '_' + param + '_volume.txt'
                        simu_get_volume(mesh_path, volume_path, act_script_path, wb_script_path)

if is_JPR_mesh_gen:
    #time.sleep(3600)
    folder_path = "E:\Data_L3"
    patient_list = ['01_2007',
                    '02_2007', '07_2007', '08_2007', '11_2007',
                   '12_2007', '13_2007', '15_2007',
                    '16_2007',
                    '17_2007',
                   '18_2007', '19_2007',
        '20_2007',
                   '03',
        '31',

        '32',
        '35', '37', '40', '43', '44'
        ]
    element_type_list = ['QT']
    poisson_list = ['v03']
    param_list = [#0.328,
                  #0.219,
                  1
                  ]
    seg_list = ['VB',
                'VB2',
                #'VB_AL',
                #'VB_SA',
                #'VB_EC'
                ]
    resolution_list = [#'328mic',
                       '656mic',
        #'984mic'
    ]

    for patient in patient_list:
        patient_folder = folder_path + "\\" + patient
        for resolution in resolution_list:
            resolution_folder = patient_folder + "\\" + patient + "_" + resolution
            mesh_folder = resolution_folder + r"\Mesh"
            for seg in seg_list:
                stl_path = resolution_folder + '\\' + patient + "_" + resolution + "_" + seg + '.stl'
                for element_type in element_type_list:
                    for param in param_list:
                        mesh_base = mesh_folder + "\\" + patient + "_" + resolution + "_" + seg + "_" + element_type + '_' + str(param).replace('.', '')
                        act_script_path = folder_path + r'\ACT_scripts' + '\\' + patient + '_' + resolution + '_' +\
                            seg + '_' + element_type + '_' + str(param).replace('.', '') + '_act_script.py'
                        wb_script_path = folder_path + r'\WB_scripts' + '\\' + patient + '_' + resolution + '_' + \
                                         seg + '_' + element_type + '_' + str(param).replace('.', '') + '_wb_script.wbjn'
                        mesh_path = mesh_base + ".cdb"
                        simu_gen_mesh_from_elemental_volume(mesh_path, stl_path, act_script_path, wb_script_path, param, element_type)

if is_JPR_EPP:
    #time.sleep(5*3600)
    folder_path = "E:\Data_L3"
    patient_list = ['01_2007',
                    '02_2007',
                    '07_2007', '08_2007',
                    '11_2007',
                   '12_2007',
                    '13_2007', '15_2007',
                    '16_2007',
                    '17_2007',
                   '18_2007',
        '19_2007',
                    '20_2007',
                   '03', '31',

        '32',
        '35', '37', '40', '43', '44'
        ]
    element_type_list = ['QT']
    poisson_list = ['v03']
    qctma_step_list = [10
        #1, 2,
                        #5, 10, 20, 50, 100, 200, 500
                       ]
    param_list = ['1'#'0328',
                        #'0219',
                        #'0109',
        #'035'
        #'2', '08', '01',
        #'02', '05', '1'
                  ]
    seg_list = ['VB', 'VB2',
                #'VB_EC', 'VB_AL'
                ]
    resolution_list = [#'984mic',
                       '656mic',
        #'328mic'
                       ]
    mat_software = 'qctma'
    config_list = [#'KopEL',
                    'KopEPP07'
                    #'A0B3C1P5EPP07',
        #"A0B3C2EPP07",
        #"A0B3P5C1P5EPP07",
        #"A0B3P5C2EPP07"
        #"A0B3P5C0P8EPP07",
        #"A0B7C1P5EPP07"
                   ]#, 'KopEPP15']
    is_EPP = True
    is_EPP_all_times = False
    is_EL = False
    is_EPP_remote_point_center = False
    nb_mat_list = ['']  # '10', '20', '50', '100']
    material_step_type = None  # "equal_material_proportion"
    result_reaction_file = folder_path + '\\' + 'results_JPR_EPP_OP_' + str(
        datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + '.txt'

    print(result_reaction_file)

    import time
    #time.sleep(2*3600)

    for patient in patient_list:
        patient_folder = folder_path + "\\" + patient
        for resolution in resolution_list:
            resolution_folder = patient_folder + "\\" + patient + "_" + resolution
            mesh_folder = resolution_folder + r"\Mesh"
            for seg in seg_list:
                stl_path = resolution_folder + '\\' + patient + "_" + resolution + "_" + seg + '.stl'
                for element_type in element_type_list:
                    for param in param_list:
                        mesh_base = mesh_folder + "\\" + patient + "_" + resolution + "_" + seg + "_" + element_type + '_' + param
                        for qctma_step in qctma_step_list:
                            for poisson in poisson_list:
                                for config in config_list:
                                    for nb_mat in nb_mat_list:
                                        act_script_path = folder_path + r'\ACT_scripts' + '\\' + patient + '_' + resolution + '_' +\
                                            seg + '_' + element_type + '_' + param + '_' + mat_software + '_' + str(qctma_step) + poisson + '_' + config + '_act_script.py'

                                        volume_path = folder_path + r'\volume' + '\\' + patient + '_' + resolution + '_' + \
                                                          seg + '_' + element_type + '_' + param + '_' + mat_software + '_' + str(
                                            qctma_step) + poisson + '_' + config + '_volume.txt'
                                        stress_path = folder_path + r'\stress' + '\\' + patient + '_' + resolution + '_' + \
                                                      seg + '_' + element_type + '_' + param + '_' + mat_software + '_' + str(
                                            qctma_step) + poisson + '_' + config + '_stress.txt'
                                        strain_path = folder_path + r'\strain' + '\\' + patient + '_' + resolution + '_' + \
                                                      seg + '_' + element_type + '_' + param + '_' + mat_software + '_' + str(
                                            qctma_step) + poisson + '_' + config + '_strain.txt'

                                        wb_script_path = folder_path + r'\WB_scripts' + '\\' + patient + '_' + resolution + '_' + \
                                                         seg + '_' + element_type + '_' + param + '_' + mat_software + '_' + str(
                                            qctma_step) + poisson + '_' + config + '_wb_script.wbjn'

                                        if material_step_type:
                                            mekamesh_path = mesh_base + '_' + mat_software + '_' + str(qctma_step) + poisson \
                                                        + '_' + material_step_type + '_' + config + '_' + nb_mat + ".cdb"
                                        else:
                                            mekamesh_path = mesh_base + '_' + mat_software + '_' + str(
                                                qctma_step) + poisson \
                                                            + '_' + config + ".cdb"

                                        if is_EPP:

                                            simu_EPP(mekamesh_path, result_reaction_file, act_script_path, wb_script_path
                                                 )

                                        if is_EPP_all_times:
                                            results_folder = folder_path + r'\results_all_times'
                                            act_script_path = folder_path + r'\ACT_scripts' + '\\' + patient + '_' + resolution + '_' + \
                                                              seg + '_' + element_type + '_' + param + '_' + mat_software + '_' + str(
                                                qctma_step) + poisson + '_' + config + '_act_script_all_times.py'
                                            wb_script_path = folder_path + r'\WB_scripts' + '\\' + patient + '_' + resolution + '_' + \
                                                             seg + '_' + element_type + '_' + param + '_' + mat_software + '_' + str(
                                                qctma_step) + poisson + '_' + config + '_wb_script_all_times.wbjn'

                                            simu_EPP_all_times(mekamesh_path, result_reaction_file, results_folder, act_script_path, wb_script_path,
                                                 4/100)

                                        if is_EPP_remote_point_center:
                                            simu_EPP_center_remote_point(mekamesh_path, result_reaction_file, "", act_script_path, wb_script_path, 10
                                                 )
                                        if is_EL:
                                            result_reaction_file = folder_path + '\\' + 'results_JPR_EL.txt'
                                            simu_EL(mekamesh_path, result_reaction_file, volume_path, stress_path, strain_path,
                                                act_script_path, wb_script_path
                                                 )

###########################

if is_WL_QCT_postdefect_mesh_gen:
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
    nb_element_list = ['100']
    location = 'VB'
    resolution = 'def'

    for sample in sample_list:
        for element_type in element_type_list:
            for nb in nb_element_list:

                act_script_path = folder_path + r'\ACT_scripts' + '\\' + sample + '_' + resolution + '_' + \
                                  location + '_' + element_type + '_' + nb + 'k_' + 'act_script.py'
                mesh_save_path = folder_path + '\\' + sample + '_' + resolution + '\\' + 'Mesh' + '\\' + sample + '_' + resolution + '_' + \
                                  location + '_' + element_type + '_' + nb + 'k.cdb'
                stl_path = folder_path + '\\' + sample + '_' + resolution + '\\' + '3DSlicer' + '\\' + sample + '_' + resolution + '_' + \
                                  location + '.stl'

                #print(stl_path)
                #print(act_script_path)
                print(mesh_save_path)

                act_linear_script = act_scripts.act_script_createMesh_default
                act_linear_script = act_linear_script.replace("{type_elem}", element_type)
                act_linear_script = act_linear_script.replace("{sample}", sample)
                act_linear_script = act_linear_script.replace("{size_elem}", 'None')
                act_linear_script = act_linear_script.replace("{nb_elem}", nb)
                act_linear_script = act_linear_script.replace("{mesh_save_path}", mesh_save_path)
                with open(act_script_path, 'w+') as f:
                    f.write(act_linear_script)

                wb_script_path = folder_path + r'\WB_scripts' + '\\' + sample + '_' + resolution + '_' + \
                                 location + '_' + element_type + '_' + nb + 'k_' + 'wb_script.wbjn'
                wb_script_simulation = wb_scripts.wb_script_createMesh_default
                wb_script_simulation = wb_script_simulation.replace("{stl_path}", stl_path)
                wb_script_simulation = wb_script_simulation.replace("{act_script_path}", act_script_path)
                with open(wb_script_path, 'w+') as f:
                    f.write(wb_script_simulation)
                try:
                    cmd = r'"C:\Program Files\ANSYS Inc\v211\Framework\bin\Win64\RunWB2.exe"  -B -R "%s"' % wb_script_path
                    print(cmd)
                    subprocess.check_call(cmd, shell=True)
                except:
                    print("ERROR : %s" % sample)

if is_WL_mesh_gen:
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
    nb_element_list = ['100']
    volume_element_list = [1]
    seg_list = [#'HRpQCT_VB', 'def_VB_F_transformed',
                'def_VB_transformed']

    for sample in sample_list:
        for seg in seg_list:
            for element_type in element_type_list:
                for param in volume_element_list:
                    act_script_path = folder_path + r'\ACT_scripts' + '\\' + sample + '_' + seg + '_' + element_type + '_' + str(param).replace('.', '') + '_act_script.py'
                    mesh_save_path = folder_path + '\\' + 'Mesh' + '\\' + sample + '_' + seg + '_' + element_type + '_' + str(param).replace('.', '') + '.cdb'
                    stl_path = folder_path + '\\' + 'Segmentation' + '\\' + sample + '_' + seg + '.stl'
                    wb_script_path = folder_path + r'\WB_scripts' + '\\' + sample + '_' + seg + '_' + element_type + '_' + str(param).replace('.', '') + '_' + 'wb_script.wbjn'
                    simu_gen_mesh_from_elemental_volume(mesh_save_path, stl_path, act_script_path, wb_script_path, param, element_type)

if is_WL_volume:
        folder_path = r"E:\Data_WL"
        sample_list = [   '01_2005_L1',
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

        for sample in sample_list:
            for seg in seg_list:
                for element_type in element_type_list:
                    for param in param_list:
                        mesh_base = sample + '_' + seg + '_' + element_type + '_' + param
                        act_script_path = folder_path + r'\ACT_scripts' + '\\' + sample + '_' + \
                                          seg + '_' + element_type + '_' + param + '_get_volume_act_script.py'
                        wb_script_path = folder_path + r'\WB_scripts' + '\\' + sample + '_' + \
                                         seg + '_' + element_type + '_' + param + '_get_volume_wb_script.wbjn'
                        mesh_path = folder_path + '\\Mesh\\' + mesh_base + ".cdb"

                        volume_path = folder_path + '\\' + r'Volume\\' + sample + "_" + seg + "_" + element_type + '_' + param + '_volume.txt'
                        simu_get_volume(mesh_path, volume_path, act_script_path, wb_script_path)

if is_WL_EPP:
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
    seg_list = [#'HRpQCT_VB',
                #'def_VB_F_transformed',
                'def_VB_transformed'
                ]
    config_list = [#'KopEPP07',
                   'KopEPP15'
                   ]
    qctma_step_list = ['10']
    software = 'qctma'
    material_step_type = None#"equal_material_proportion"
    material_step = 100  # number of materials
    approximation = 'average'

    is_EPP = True
    is_height = False
    total_strain = 2.3  # in percent of vertebral height
    #time.sleep(3600)

    for sample in sample_list:
        for seg in seg_list:
            for element_type in element_type_list:
                for param in param_list:
                    for qctma_step in qctma_step_list:
                        for config in config_list:
                            if material_step_type:
                                base = sample + '_' + seg + '_' + element_type + '_' + param + '_qctma_' + qctma_step + 'v03_' \
                                                 + material_step_type + '_' + config + '_' + str(material_step)
                            else:
                                base = sample + '_' + seg + '_' + element_type + '_' + param + '_qctma_' + qctma_step + 'v03_100MPa_' + config
                            act_script_path = folder_path + r'\ACT_scripts' + '\\' + base + 'act_script.py'
                            result_reaction_file = folder_path + '\\' + 'results_' + config + '_' + param + 'mm3_' + str(total_strain) +'p100.txt'
                            mekamesh_path = folder_path + '\\' + 'Mekamesh' + '\\' + base + '.cdb'
                            wb_script_path = folder_path + r'\WB_scripts' + '\\' + base + '_wb_script.wbjn'
                            if is_EPP:
                                simu_EPP(mekamesh_path, result_reaction_file, act_script_path, wb_script_path, total_strain/100, False
                                 )

                            if is_height:
                                result_file = folder_path + '\\' + 'height.txt'
                                get_height(mekamesh_path, result_file)

if is_WL_QCT_postdefect_EPP:
    time.sleep(3600)
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
    qctma_step = '10'
    software = 'qctma'
    material_step_type = "equal_material_proportion"
    material_step = 100  # number of materials
    approximation = 'average'

    for sample in sample_list:
        for element_type in element_type_list:
            for param in param_list:
                for config in config_list:
                    act_script_path = folder_path + r'\ACT_scripts' + '\\' + sample + '_' + resolution + '_' + \
                                     location + '_' + element_type + '_' + param + '_qctma_' + qctma_step + 'v03_' \
                                         + material_step_type + '_' + config + '_' + str(material_step) + 'act_script.py'
                    result_reaction_file = folder_path + '\\' + 'results_EPP.txt'
                    mekamesh_path = folder_path + '\\' + sample + '_' + resolution + '\\' + 'Mesh' + '\\' + sample + '_' + resolution + '_' + \
                                location + '_' + element_type + '_' + param + '_' + software + '_' + qctma_step + 'v03NC_' \
                                         + material_step_type + '_' + config + '_' + str(material_step) + '.cdb'
                    wb_script_path = folder_path + r'\WB_scripts' + '\\' + sample + '_' + resolution + '_' + \
                                     location + '_' + element_type + '_' + param + '_qctma_' + qctma_step + 'v03_' \
                                         + material_step_type + '_' + config + '_' + str(material_step) + '_wb_script.wbjn'
                    simu_EPP(mekamesh_path, result_reaction_file, act_script_path, wb_script_path
                         )

###########################

if is_Artorg_mesh_gen:
    folder_path = r'E:\Artorg_data_2021_metastatic_vertebrae'

    sample_list = ['188', '192', '195', '196', '199', '203', '204', '206', '208', '214', '217', '218', '220', '224',
                   '225', '226', '230', '231', '235', '236', '240', '248', '252', '256', '257', '260', '261', '264',
                   '268', '269', '273', '280', '281', '284', '285', '288', '289', '295', '298', '299', '301', '305',
                   '308', '309', '317']
    element_type_list = ['QT']
    param_list = [1]#'10', '20', '50', '100', '200', '500']
    location = 'VB'
    resolution = '294mic'
    seg_list = ['VA', 'A']

    for sample in sample_list:
        for seg in seg_list:
            for element_type in element_type_list:
                    for param in param_list:

                            act_script_path = folder_path + r'\ACT_scripts' + '\\' + sample + '_' + resolution + '_' + \
                                              location + '_' + seg + '_' + element_type + '_' + str(param).replace('.', '') + '_' + 'act_script.py'
                            wb_script_path = folder_path + r'\WB_scripts' + '\\' + sample + '_' + resolution + '_' + \
                                             location + '_' + seg + '_' + element_type + '_' + str(param).replace('.', '') + '_' + 'wb_script.wbjn'
                            mesh_path = folder_path + '\\' + sample + '\\' + sample + '_' + resolution + '_' + \
                                              location + '_' + seg + '_' + element_type + '_' + str(param).replace('.', '') + '.cdb'
                            stl_path = folder_path + '\\' + sample + '\\' + sample + '_' + resolution + '_' + \
                                              location + '_' + seg + '.stl'

                            simu_gen_mesh_from_elemental_volume(mesh_path, stl_path, act_script_path, wb_script_path,
                                                                param, element_type)

if is_Artorg_simu_EPP:
    #time.sleep(3600)
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
                #'A'
                ]
    config = 'KopEPP15'
    material_step_type = None#"equal_material_proportion"
    material_step = 10  # number of materials
    approximation = 'average'
    qctma_step = '10'

    simu_EPP = False
    volume = True

    for sample in sample_list:
        for seg in seg_list:
            for element_type in element_type_list:
                for size in size_list:
                    try:
                        if material_step_type:
                            base = sample + '_' + resolution + '_' + \
                                         location + '_' + seg + '_' + element_type + '_' + size + '_qctma_' + qctma_step + 'v03_' \
                                             + material_step_type + '_' + config + '_' + str(material_step)
                        else:
                            base = sample + '_' + resolution + '_' + \
                                         location + '_' + seg + '_' + element_type + '_' + size + '_qctma_' + qctma_step + 'v03_100MPa' \
                                            + '_' + config
                        act_script_path = folder_path + r'\ACT_scripts' + '\\' + base + '_act_script.py'
                        result_reaction_file = folder_path + '\\' + 'results_1mm3_EPP15_100MPa_2p100_VA.txt'
                        mekamesh_save_path = folder_path + '\\' + sample + '\\' + base + '.cdb'
                        stl_path = folder_path + '\\' + sample + '\\' + sample + '_' + resolution + '_' + \
                                   location + '_' + seg + '.stl'
                        #print(stl_path)
                        #print(act_script_path)
                        print(mekamesh_save_path)
                        if volume:
                            act_script_path_volume = folder_path + r'\ACT_scripts' + '\\' + base + '_get_volume_act_script.py'
                            wb_script_path_volume = folder_path + r'\WB_scripts' + '\\' + base + '_get_volume_wb_script.wbjn'
                            volume_path = folder_path + '\\volume\\' + base + '_volume.txt'
                            simu_get_volume(mekamesh_save_path, volume_path, act_script_path_volume, wb_script_path_volume)

                        wb_script_path = folder_path + r'\WB_scripts' + '\\' + base + '_wb_script.wbjn'

                        if simu_EPP:
                            simu_EPP(mekamesh_save_path, result_reaction_file, act_script_path, wb_script_path, 2/100, False
                             )
                    except FileNotFoundError:
                        print(mekamesh_save_path)

if is_Artorg_simu_EL:
    import time
    #time.sleep(1000)


    folder_path = r'E:\Artorg_data_2021_metastatic_vertebrae'

    sample_list = [#'214', '217', '218', '220', '224',
                   #'225', '226', '230', '231', '235', '236', '240', '248', '252', '256', '257', '260', '261', '264',
                   #'268', '269', '273', '280', '281', '284', '285', '288',
                   '289', '295', '298', '299', '301', '305',
                   '308', '309', '317']
    element_type_list = ['QT']
    size_list = ['1']
    location = 'VB'
    resolution = '294mic'
    seg_list = ['A']
    config_list = ['KopEPP15']#'Kopperdahl2002-EPP-iso'
    material_step_type = "equal_material_proportion"
    material_step = 10  # number of materials
    approximation = 'average'
    approx_size_list = ['GS_0']
    qctma_step = '10'

    for sample in sample_list:
        for seg in seg_list:
            for element_type in element_type_list:
                for size in size_list:
                    for approx_size in approx_size_list:
                        for config in config_list:
                            try:
                                if material_step_type:
                                    act_script_path = folder_path + r'\ACT_scripts' + '\\' + sample + '_' + resolution + '_' + \
                                                     location + '_' + seg + '_' + element_type + '_' + size + 'mm_qctma_' + qctma_step + 'v03_' \
                                                         + approx_size + '_' + material_step_type + '_' + config + '_' + str(material_step) + 'act_script.py'
                                    mekamesh_save_path = folder_path + '\\' + sample + '\\' + sample + '_' + resolution + '_' + \
                                                     location + '_' + seg + '_' + element_type + '_' + size + 'mm_qctma_' + qctma_step + 'v03_' \
                                                         + approx_size + '_' + material_step_type + '_' + config + '_' + str(material_step) + '.cdb'
                                    wb_script_path = folder_path + r'\WB_scripts' + '\\' + sample + '_' + resolution + '_' + \
                                                     location + '_' + seg + '_' + element_type + '_' + size + 'mm_qctma_' + qctma_step + 'v03_' \
                                                     + approx_size + '_' + material_step_type + '_' + config + '_' + str(
                                        material_step) + '_wb_script.wbjn'
                                else:
                                    act_script_path = folder_path + r'\ACT_scripts' + '\\' + sample + '_' + resolution + '_' + \
                                                      location + '_' + seg + '_' + element_type + '_' + size + 'mm_qctma_' + qctma_step + 'v03_' \
                                                      + 'act_script.py'
                                    mekamesh_save_path = folder_path + '\\' + sample + '\\' + sample + '_' + resolution + '_' + \
                                                         location + '_' + seg + '_' + element_type + '_' + size + 'mm_qctma_' + qctma_step + 'v03_' \
                                                         + approx_size + '_' + config + '.cdb'
                                    wb_script_path = folder_path + r'\WB_scripts' + '\\' + sample + '_' + resolution + '_' + \
                                                 location + '_' + seg + '_' + element_type + '_' + size + 'mm_qctma_' + qctma_step + 'v03_' \
                                                 + 'wb_script.wbjn'
                                result_reaction_file = folder_path + r'\ACT_scripts' + '\\' + 'results.txt'
                                stl_path = folder_path + '\\' + sample + '\\' + sample + '_' + resolution + '_' + \
                                               location + '_' + seg + '.stl'
                                #print(stl_path)
                                #print(act_script_path)
                                print(mekamesh_save_path)

                                act_linear_script = act_scripts.act_template_EPP
                                act_linear_script = act_linear_script.replace("{result_reaction_file}", result_reaction_file)
                                act_linear_script = act_linear_script.replace("{ID_mekamesh}", mekamesh_save_path.split('\\')[-1].split('.cdb')[0])
                                with open(act_script_path, 'w+') as f:
                                    f.write(act_linear_script)

                                wb_script_simulation = wb_scripts.wb_script_simulation_EPP
                                wb_script_simulation = wb_script_simulation.replace("{mekamesh_path}", mekamesh_save_path)
                                wb_script_simulation = wb_script_simulation.replace("{path_act}", act_script_path)
                                with open(wb_script_path, 'w+') as f:
                                    f.write(wb_script_simulation)
                                try:
                                    cmd = r'"C:\Program Files\ANSYS Inc\v211\Framework\bin\Win64\RunWB2.exe"  -B -R "%s"' % wb_script_path
                                    print("\tCMD: ", cmd)
                                    t0 = datetime.datetime.now()
                                    print("\tStarted at: ", t0)
                                    subprocess.check_call(cmd, shell=True)
                                    t1 = datetime.datetime.now()
                                    print("\tDuration: ", t1-t0)
                                except subprocess.CalledProcessError as error:
                                    print(error)
                                    print("### ERROR : %s" % sample)
                            except FileNotFoundError:
                                pass

###########################

if is_IBHGC_mesh_gen:
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

    seg_list = ['VB',
                #'VB2'
                ]
    element_type_list = ['QT']
    size_list = []#['1']
    nb_elem_list = ['200', '500']
    param_list = [0.5, 0.8]

    for sample in sample_list:
        for seg in seg_list:
            for element_type in element_type_list:
                    for param in param_list:
                        act_script_path = folder_path + r'\ACT_scripts' + '\\' + sample + '_' + \
                                          seg + '_' + element_type + '_' + str(param).replace('.', '') + '_act_script.py'
                        wb_script_path = folder_path + r'\WB_scripts' + '\\' + sample + '_' + \
                                          seg + '_' + element_type + '_' + str(param).replace('.', '') + '_wb_script.py'
                        mesh_save_path = folder_path + '\\' + 'Mesh' + '\\' + sample + '_' + \
                                          seg + '_' + element_type + '_' + str(param).replace('.', '') + '.cdb'
                        stl_path = folder_path + '\\' + 'Segmentation' + '\\' + sample + '_' + \
                                          seg + '.stl'

                        simu_gen_mesh_from_elemental_volume(mesh_save_path, stl_path, act_script_path, wb_script_path, param, element_type)

if is_IBHGC_simu_EPP:
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
                   '493_L2' ]

    remote_points = [[-10.37163429,	119.6584858,-114.4703302],
                    [-12.52083714,106.2091692,-156.684117],
                    [-13.58315366,160.5473995,-479.5191082],
                    [-11.02108278,154.4993417,-513.3055222],
                    [-8.409471784,154.3271243,-893.3003124],
                    [-11.45441715,157.2041292,-923.3531181],
                    [-13.14437823,152.4088934,-955.7951969],
                    [-8.989304572,142.2826455,-108.2357448],
                    [-9.243214118,125.842611,-142.5568753],
                    [-12.76190844,171.2909329,-473.7584714],
                    [-11.49727042,160.7495001,-502.382198],
                    [-12.59441371,147.5344026,-533.5778911],
                    [10.84905531,141.3097881,-897.3594106],
                    [15.06061897,133.6646386,-933.9035216],
                    [14.89623895,114.9182131,-973.4400722],
                    [-14.98547733,145.4976324,-76.59988613],
                    [-17.13767435,125.9028237,-105.1838967],
                    [-14.68840445,109.9574119,-137.7540637],
                    [-15.25028279,156.7459595,-479.1159007],
                    [-9.881251645,144.7348102,-515.5606684],
                    [-6.754195286,138.2302409,-550.5521276],
                    [-3.390718964,149.1255144,-908.1364758],
                    [-3.398770051,143.7606935,-946.378484],
                    [-1.13996111,137.5829286,-981.9695737],
                    [-9.995271285,175.280383,-462.1534422],
                    [-10.24605246,169.7243284,-494.2033219],
                    [-7.096904814,161.7193816,-526.2602589],
                    [-5.999242749,144.6050483,-837.0117769]]

    seg_list = ['VB',
                #'VB2'
                ]
    element_type_list = ['QT']
    param_list = ['2']
    qctma_step_list = ['10']
    config_list = ['KopEL04']
    material_step_type = None#"equal_material_proportion"
    material_step = 100  # number of materials
    approximation = 'average'
    min_E = 1

    sample_index = 0
    for sample in sample_list:
        for seg in seg_list:
            for element_type in element_type_list:
                for param in param_list:
                    for qctma_step in qctma_step_list:
                        for config in config_list:
                            if material_step_type:
                                base = sample + '_' + seg + '_' + element_type + '_' + param + \
                                   '_qctma_' + qctma_step + 'v03' + '_' + material_step_type + '_' + config + '_' + str(material_step)
                            else:
                                base = sample + '_' + seg + '_' + element_type + '_' + param + \
                                       '_qctma_' + qctma_step + 'v03' + '_' + config
                            if min_E:
                                base = sample + '_' + seg + '_' + element_type + '_' + param + \
                                       '_qctma_' + qctma_step + 'min' + str(min_E) + '_' + config
                            act_script_path = folder_path + r'\ACT_scripts' + '\\' + base + '_act_script.py'
                            wb_script_path = folder_path + r'\WB_scripts' + '\\' + base + '_wb_script.wbjn'
                            mekamesh_save_path = folder_path + '\\' + 'Mekamesh' + '\\' + base + '.cdb'

                            result_reaction_file = folder_path + '\\' + 'results_IBHGC_VB_EL.txt'
                            #result_reaction_file = folder_path + '\\' + 'results_IBHGC_nb_elem.txt'
                            results_folder = folder_path + '\\' + 'Results_files'
                            simu_EPP_remote_point(mekamesh_save_path, result_reaction_file, results_folder, act_script_path, wb_script_path,
                                    remote_points[sample_index], False, 5/100
                                     )
        sample_index += 1

if is_IBHGC_volume:
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
                #'VB2'
                ]
    element_type_list = ['QT']
    param_list = ['1']
    qctma_step_list = ['10']
    config_list = ['KopEPP07']
    material_step_type = None#"equal_material_proportion"
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

                            simu_get_volume(mekamesh_save_path, volume_path, act_script_path_volume, wb_script_path_volume)



###########################

if is_MCC_mesh_gen:
    #time.sleep(3600)
    folder_path = "E:\Mekanos_clinical_cases"
    patient_list = [#'01017',
                    '01036'
        ]
    element_type_list = ['QT']
    poisson_list = ['v03']
    param_list = [
                  1
                  ]
    seg_list = [#'L5', 'L4',
                'L3',
                #'L2', 'L1',
                #'T12', 'T11', 'T10', 'T9', 'T8'
                ]
    edit = False

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
                    simu_gen_mesh_from_elemental_volume(mesh_path, stl_path, act_script_path, wb_script_path, param, element_type, edit)

if is_MCC_EPP:
    folder_path = "E:\Mekanos_clinical_cases"
    patient_list = ['01017',
        '01036'
    ]
    element_type_list = ['QT']
    poisson_list = ['v03']
    param_list = [
        1
    ]
    seg_list = [ 'L5', 'L4',
        'L3',
        'L2', 'L1',
        'T12', 'T11', 'T10', 'T9', 'T8'
    ]
    config_list = ['KopEPP07']
    qctma_step_list = ['10']
    software = 'qctma'
    material_step_type = None#"equal_material_proportion"
    material_step = 100  # number of materials
    approximation = 'average'

    is_EPP = False
    volume = True
    is_height = False

    str_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    for patient in patient_list:
        for seg in seg_list:
            for element_type in element_type_list:
                for param in param_list:
                    for qctma_step in qctma_step_list:
                        for config in config_list:
                            if material_step_type:
                                base = patient + '_' + seg + '_' + element_type + '_' + str(param).replace(',', '.') + '_qctma_' + qctma_step + 'v03_' \
                                                 + material_step_type + '_' + config + '_' + str(material_step)
                            else:
                                base = patient + '_' + seg + '_' + element_type + '_' + str(param).replace(',', '.') + '_qctma_' + qctma_step + 'v03_' + config
                            act_script_path = folder_path + r'\ACT_scripts' + '\\' + base + 'act_script.py'
                            result_reaction_file = folder_path + '\\' + 'results_MCC' + str(str_time) + '.txt'
                            mekamesh_path = folder_path + '\\' + patient + '\\' + 'Mesh' + '\\' + base + '.cdb'
                            wb_script_path = folder_path + r'\WB_scripts' + '\\' + base + '_wb_script.wbjn'
                            if is_EPP:
                                simu_EPP(mekamesh_path, result_reaction_file, act_script_path, wb_script_path, 1.9/100, False
                                 )

                            if volume:
                                act_script_path_volume = folder_path + r'\ACT_scripts' + '\\' + base + '_get_volume_act_script.py'
                                wb_script_path_volume = folder_path + r'\WB_scripts' + '\\' + base + '_get_volume_wb_script.wbjn'
                                volume_path = folder_path + '\\volume\\' + base + '_volume.txt'
                                simu_get_volume(mekamesh_path, volume_path, act_script_path_volume,
                                                wb_script_path_volume)

                            if is_height:
                                result_file = folder_path + '\\' + 'height.txt'
                                get_height(mekamesh_path, result_file)