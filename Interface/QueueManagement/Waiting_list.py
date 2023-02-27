import threading

from Global_paths import global_path
from datetime import datetime


class Waiting_list:
    def __init__(self):
        self.path = global_path + '/Data/waiting_list.txt'

    def add_meshing(self, datasets, element_type, params):
        _time = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
        for dataset in datasets:
            chosen_samples = dataset.chosen_sample_ID_list
            chosen_seg = dataset.chosen_segmentation_list
            samples = dataset.sample_ID_list
            for i in range(len(chosen_samples)):
                if chosen_samples[i]:
                    for seg in chosen_seg:
                        for param in params:
                            _line = _time + '\t' + dataset.get_name() + '\t' + str(samples[i]) + '\t' + seg + '\t' \
                                    + element_type \
                                    + '_' + param + '\t' + 'action=meshing' + '\t' + 'status=waiting' + '\n'
                            print(_line)
                            self.safe_write(_line)

    def add_mesh_analysis(self, datasets, element_type, params, mesh_analysis):
        _time = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
        for dataset in datasets:
            chosen_samples = dataset.chosen_sample_ID_list
            chosen_seg = dataset.chosen_segmentation_list
            samples = dataset.sample_ID_list
            for i in range(len(chosen_samples)):
                if chosen_samples[i]:
                    for seg in chosen_seg:
                        for param in params:
                            for analysis in mesh_analysis:
                                _line = _time + '\t' + dataset.get_name() + '\t' + str(samples[i]) + '\t' + seg +\
                                        '\t' + element_type \
                                        + '_' + param + '\t' + 'action=mesh_analysis' + '\t' + analysis + '\t' + 'status=waiting' + '\n'
                                print(_line)
                                self.safe_write(_line)

    def add_laws_attribution(self, datasets, meshes,
                        material_step_type, material_step, min_value, mechanical_law_list):
        _time = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
        for dataset in datasets:
            chosen_samples = dataset.chosen_sample_ID_list
            chosen_seg = dataset.chosen_segmentation_list
            samples = dataset.sample_ID_list
            for i in range(len(chosen_samples)):
                if chosen_samples[i]:
                    for seg in chosen_seg:
                        for mesh in meshes:
                            _line = _time + '\t' + dataset.get_name() + '\t' + str(samples[i]) + '\t' + seg + '\t'\
                                    + mesh + '\t' + 'action=laws_attribution' + '\t' + \
                                    'material_step_type=' + material_step_type + '\t' + \
                                    'material_step=' + material_step + '\t' + \
                                    'min_value=' + min_value + '\t' + \
                                    str([str(m) for m in mechanical_law_list]) + '\t' + 'status=waiting' + '\n'
                            print(_line)
                            self.safe_write(_line)

    def safe_write(self, line):
        # avoid multiple writing at the same time
        # create a lock
        lock = threading.Lock()
        # acquire the lock
        lock.acquire()
        # open the file and write
        with open(self.path, 'a') as file:
            file.write(line)
        # release the lock
        lock.release()

    def safe_read(self):
        self.waiting_list = []

        # avoid multiple writing at the same time
        # create a lock
        lock = threading.Lock()
        # acquire the lock
        lock.acquire()
        # open the file and write
        with open(self.path, 'r') as file:
            line = file.readline()
            while line:
                info_list = line.replace('\n', '').split('\t')
                time = info_list[0]
                dataset_name = info_list[1]
                sample = info_list[2]
                seg = info_list[3]
                mesh = info_list[4]
                action = info_list[5].replace('action=', '')
                if action == 'meshing':
                    status = info_list[6].replace('status=', '')
                    self.waiting_list.append([time, 'meshing', dataset_name, sample, seg, mesh, '', '', '', '', '', status])
                elif action == 'mesh_analysis':
                    analysis = info_list[6]
                    status = info_list[7].replace('status=', '')
                    self.waiting_list.append([time, 'mesh_analysis', dataset_name, sample, seg, mesh, analysis, '', '', '', '', status])
                elif action == 'qctma':
                    material_step = info_list[7].replace('material_step=', '')
                    min_value = info_list[8].replace('min_value=', '')
                    status = info_list[9].replace('status=', '')
                    self.waiting_list.append([time, 'qctma', dataset_name, sample, seg, mesh, '', material_step, min_value, '', '', status])
                elif action == 'laws_attribution':
                    material_step = info_list[7].replace('material_step=', '')
                    min_value = info_list[8].replace('min_value=', '')
                    mechanical_laws = info_list[9]
                    status = info_list[10].replace('status=', '')
                    self.waiting_list.append(
                        [time, 'laws_attribution', dataset_name, sample, seg, mesh, '', material_step, min_value, mechanical_laws, '', status])
                elif action == 'mekamesh_analysis':
                    material_step = info_list[7].replace('material_step=', '')
                    min_value = info_list[8].replace('min_value=', '')
                    mechanical_laws = info_list[9]
                    analysis = info_list[10]
                    status = info_list[11].replace('status=', '')
                    self.waiting_list.append(
                        [time, 'mekamesh_analysis', dataset_name, sample, seg, mesh, material_step, min_value, mechanical_laws, analysis,
                         status])
                elif action == 'boundary_conditions':
                    pass
                elif action == 'simulation':
                    pass

                line = file.readline()
        # release the lock
        lock.release()

        return self.waiting_list


