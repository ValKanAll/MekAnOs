from module.Structure.Mekamesh import Mekamesh
from module.Reader.cdb_reader import read_cdbfile, get_element_occurence, read_occurence_file
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np



if __name__ == "__main__":
    #actions
    export_occurence_files = True
    read_occurence_files = True
    plot_histogram = True
    blandt_altman = True

    #projects
    is_WL_predefect_HRpQCT = False
    is_WL_predefect_QCT = False
    is_Artorg = False
    is_WL = True

    if is_WL_predefect_HRpQCT:
        project_folder_qct = "E:\Data_pre-defect_2021-03-19\L1"
        project_folder_hrpqct = "E:\Data_pre-defect_HRpQCT"
        sample_list = ['01_2005_L1',
                       #'01_2006_L1',
                       #'02_2006_L1',
                       #'2a_2005_L1',
                       #'2b_2005_L1'
                       ]
        '''               '03_2006_L1',
                       '04_2006_L1',
                       '05_2006_L1',
                       '06_2006_L1',
                       '08_2006_L1',
                       '10_2006_L1',
                       'USOD18433_L1',
                       'USOD20307_L1']'''

        resolution_list = ['FOV20', 'FOV38']
        location_list = ['VB']
        mesh_param_list = [#'QH_1mm',
                           #'QT_1mm',
                           'QV_1mm'
        ]
        qctma_step = '10'

        for patient in sample_list:
            for location in location_list:
                for param in mesh_param_list:
                    mesh_qct_FOV20_path = project_folder_qct + "\\" + patient + "\\" + 'FOV20' + "\Mesh\\" \
                                + patient + "_" + 'FOV20' + "_" + location + "_" + param + "_" + "qctma_" + qctma_step + "v03C" + ".cdb"
                    mesh_qct_FOV38_path = project_folder_qct + "\\" + patient + "\\" + 'FOV38' + "\Mesh\\" \
                                     + patient + "_" + 'FOV38' + "_" + location + "_" + param + "_" + "qctma_" + qctma_step + "v03C" + ".cdb"

                    mesh_hrpqct_410_path = project_folder_hrpqct + "\\" + patient + "\Mesh\\" \
                                      + patient + "_410mic_" + location + "_" + param + "_" + "qctma_" + qctma_step + "v03" + ".cdb"
                    mesh_hrpqct_738_path = project_folder_hrpqct + "\\" + patient + "\Mesh\\" \
                                      + patient + "_738mic_" + location + "_" + param + "_" + "qctma_" + qctma_step + "v03" + ".cdb"

                    if export_occurence_files:
                        print(mesh_qct_FOV20_path)
                        get_element_occurence(mesh_qct_FOV20_path)
                        print(mesh_qct_FOV38_path)
                        get_element_occurence(mesh_qct_FOV38_path)

                        print(mesh_hrpqct_410_path)
                        get_element_occurence(mesh_hrpqct_410_path)
                        print(mesh_hrpqct_738_path)
                        get_element_occurence(mesh_hrpqct_738_path)

                    if read_occurence_files:
                        occurence_file_410_path = mesh_hrpqct_410_path.split('.cdb')[0] + '_occurrence_file_by_element.txt'
                        E_list_410, rho_list_410 = read_occurence_file(occurence_file_410_path)
                        occurence_file_738_path = mesh_hrpqct_738_path.split('.cdb')[0] + '_occurrence_file_by_element.txt'
                        E_list_738, rho_list_738 = read_occurence_file(occurence_file_738_path)

                        occurence_file_FOV20_path = mesh_qct_FOV20_path.split('.cdb')[0] + '_occurrence_file_by_element.txt'
                        E_list_FOV20, rho_list_FOV20 = read_occurence_file(occurence_file_FOV20_path)
                        occurence_file_FOV38_path = mesh_qct_FOV38_path.split('.cdb')[0] + '_occurrence_file_by_element.txt'
                        E_list_FOV38, rho_list_FOV38 = read_occurence_file(occurence_file_FOV38_path)

                    if plot_histogram:
                        #plt.figure()
                        fig, axs = plt.subplots(2, 2)
                        axs[0, 0].hist(E_list_738-E_list_410, density=True, bins=100)
                        axs[0, 0].set_title('738mic-410mic')

                        axs[0, 1].hist(E_list_FOV38-E_list_FOV20, density=True, bins=100)
                        axs[0, 1].set_title('FOV38-FOV20')

                        axs[1, 0].hist(E_list_738-E_list_FOV38, density=True, bins=100)
                        axs[1, 0].set_title('738mic-FOV38')

                        axs[1, 1].hist(E_list_410-E_list_FOV20, density=True, bins=100)
                        axs[1, 1].set_title('FOV20-410mic')

                        plt.setp(axs[-1, :], xlabel='E(MPa)')
                        plt.setp(axs[:, 0], ylabel='Proportion')

                        plt.subplots_adjust(hspace=0.5, wspace=0.4, left=0.2)

                        fig.suptitle(patient + ' ' + param)

                        fig.savefig(patient + '_' + param + '_fig1.png', dpi=200)

                        #plt.figure()
                        fig, axs = plt.subplots(2, 2)
                        axs[0, 0].plot(E_list_FOV20, E_list_410, '+')
                        axs[0, 0].set_title('410mic = f(FOV20)')

                        axs[1, 0].plot(E_list_FOV38, E_list_738, '+')
                        axs[1, 0].set_title('738mic = f(FOV38)')

                        axs[0, 1].plot(E_list_FOV20, E_list_FOV38, '+')
                        axs[0, 1].set_title('FOV38 = f(FOV20)')

                        axs[1, 1].plot(E_list_410, E_list_738, '+')
                        axs[1, 1].set_title('738mic = f(410mic)')

                        plt.setp(axs[-1, :], xlabel='E(MPa)')
                        plt.setp(axs[:, 0], ylabel='E(MPa)')

                        plt.subplots_adjust(hspace=0.5, wspace=0.4, left=0.2)

                        fig.suptitle(patient + ' ' + param)
                        fig.savefig(patient + '_' + param + '_fig2.png', dpi=200)

                        nb_bin = 50
                        fig = plt.figure()
                        plt.hist(E_list_410, alpha=0.5, density=True, bins=nb_bin, label='410mic')
                        plt.hist(E_list_738, density=True, bins=nb_bin, label='738mic')
                        plt.hist(E_list_FOV20, density=True, bins=nb_bin, label='FOV20')
                        plt.hist(E_list_FOV38, density=True, bins=nb_bin, label='FOV38')
                        plt.xlabel('E(MPa)')
                        plt.ylabel('Proportion')
                        plt.legend(loc='upper right')
                        fig.suptitle(patient + ' ' + param)
                        fig.savefig(patient + '_' + param + '_fig_hist_E.png', dpi=200)

                        fig = plt.figure()
                        plt.hist(rho_list_410, alpha=0.5, density=True, bins=nb_bin, label='410mic')
                        plt.hist(rho_list_738, density=True, bins=nb_bin, label='738mic')
                        plt.hist(rho_list_FOV20, density=True, bins=nb_bin, label='FOV20')
                        plt.hist(rho_list_FOV38, density=True, bins=nb_bin, label='FOV38')
                        plt.xlabel('rho(g/cc)')
                        plt.ylabel('Proportion')
                        plt.legend(loc='upper right')
                        fig.suptitle(patient + ' ' + param)
                        fig.savefig(patient + '_' + param + '_fig_hist_rho.png', dpi=200)

                        print(param)

                        #plt.show()

                    if blandt_altman:
                        fig, axs = plt.subplots(2, 2)
                        diff = E_list_FOV38 - E_list_FOV20
                        avrge = (E_list_FOV38 + E_list_FOV20) / 2
                        axs[0, 0].plot(avrge, diff, '+')
                        axs[0, 0].set_title('FOV38 vs FOV20')

                        diff = E_list_738 - E_list_410
                        avrge = (E_list_738 + E_list_410) / 2
                        axs[1, 0].plot(avrge, diff, '+')
                        axs[1, 0].set_title('738mic vs 410 mic')

                        diff = E_list_738 - E_list_FOV38
                        avrge = (E_list_738 + E_list_FOV38) / 2
                        axs[0, 1].plot(avrge, diff, '+')
                        axs[0, 1].set_title('738mic vs FOV38')

                        diff = E_list_410 - E_list_FOV20
                        avrge = (E_list_410 + E_list_FOV20) / 2
                        axs[1, 1].plot(avrge, diff, '+')
                        axs[1, 1].set_title('410mic vs FOV20')

                        plt.setp(axs[-1, :], xlabel='average - E(MPa)')
                        plt.setp(axs[:, 0], ylabel='diff - E(MPa)')

                        plt.subplots_adjust(hspace=0.5, wspace=0.4, left=0.2)

                        fig.suptitle(patient + ' ' + param)
                        fig.savefig(patient + '_' + param + '_blandt-altman.png', dpi=100)

                        #plt.show()

    if is_WL:
        project_folder = "E:\Data_WL"
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
                       'USOD20307_L1']

        seg_list = ['HRpQCT_VB', 'def_VB_F_transformed', 'def_VB_transformed']
        mesh_param_list = ['QT_100k'
        ]
        qctma_step = '10'


        for seg in seg_list:
            fig = make_subplots(rows=1, cols=2,
                                specs=[[{"type": "xy"}, {"type": "xy"}]])
            for patient in sample_list:
                for param in mesh_param_list:
                    mesh_path = project_folder + "\\" + "\Mekamesh\\" \
                                + patient + "_" + seg + "_" + param + "_" + "qctma_" + qctma_step + "v03" + ".cdb"

                    if export_occurence_files:
                        print(mesh_path)
                        get_element_occurence(mesh_path)

                    if read_occurence_files:
                        occurence_file_path = mesh_path.split('.cdb')[0] + '_occurrence_file_by_element.txt'
                        E_list, rho_list = read_occurence_file(occurence_file_path)

                    if plot_histogram:
                        #plt.figure()

                        #fig.update_layout(title_text=title)

                        hist_E_y, hist_E_x = np.histogram(E_list, bins=1000, density=True)
                        hist_rho_y, hist_rho_x = np.histogram(rho_list, bins=1000, density=True)

                        x_E = []
                        for i in range(len(hist_E_x) - 1):
                            x_E.append((hist_E_x[i] + hist_E_x[i + 1]) / 2)

                        x_rho = []
                        for i in range(len(hist_rho_x) - 1):
                            x_rho.append((hist_rho_x[i] + hist_rho_x[i + 1]) / 2)

                        fig.add_trace(go.Scatter(x=x_E, y=hist_E_y, name=patient + "_" + seg), row=1, col=1)
                        fig.add_trace(go.Scatter(x=x_rho, y=hist_rho_y, name=patient + "_" + seg), row=1, col=2)
            fig.show()



    if is_Artorg:

        sample_list = ['192']
        '''['188', '192',
             '195', '196', '199', '203', '204', '206', '208', '214', '217', '218', '220', '224',
                   '225', '226', '230', '231', '235', '236', '240', '248', '252', '256', '257', '260', '261', '264',
                   '268', '269', '273', '280', '281', '284', '285', '288', '289', '295', '298', '299', '301', '305',
                   '308', '309', '317']'''
        element_type_list = ['QT']
        size_list = ['1']
        location = 'VB'
        resolution = '294mic'
        seg_list = ['VA']  # , 'VA']
        config = 'Kopperdahl2002-EPP-iso'
        material_step_type = "equal_material_proportion"
        material_step = 10  # number of materials
        approximation = 'average'
        approx_size_list = ['GS_1', 'GS_3', 'GS_5', 'GS_10']
        qctma_step = '10'

        for sample in sample_list:
            for seg in seg_list:
                for element_type in element_type_list:
                    for size in size_list:
                        E_list = []
                        mesh_path = r'E:\Artorg_data_2021_metastatic_vertebrae' + '\\' + sample + '\\' + sample + '_' + resolution + '_' + \
                                    location + '_' + seg + '_' + element_type + '_' + size + 'mm_qctma_' + qctma_step + 'v03' + '.cdb'

                        occurence_file_path = mesh_path.split('.cdb')[0] + '_occurrence_file_by_element.txt'
                        E_list.append(read_occurence_file(occurence_file_path))
                        for approx_size in approx_size_list:

                            mesh_path = r'E:\Artorg_data_2021_metastatic_vertebrae' + '\\' + sample + '\\' + sample + '_' + resolution + '_' + \
                                        location + '_' + seg + '_' + element_type + '_' + size + 'mm_qctma_' + qctma_step + 'v03_' + approx_size + '.cdb'

                            occurence_file_path = mesh_path.split('.cdb')[0] + '_occurrence_file_by_element.txt'
                            E_list.append(read_occurence_file(occurence_file_path))


                if plot_histogram:

                    fig = plt.figure()
                    E_name_list = ['No smoothing', '1 mm', '3 mm', '5 mm', '10 mm']
                    for i in range(len(E_list)):
                        plt.hist(E_list[i], alpha=0.5, density=True, bins=100, label=E_name_list[i])

                    plt.xlabel('E(MPa)')
                    plt.ylabel('Proportion')
                    plt.legend(loc='upper right')
                    fig.suptitle(sample + ' ')
                    fig.savefig(sample + '_fig_GS.png', dpi=100)
                    plt.xlim(0, 400)
                    plt.show()
