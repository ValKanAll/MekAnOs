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
                                    + element_type + '\t'\
                                    + param + '\t' + 'action=meshing' + '\t' + 'status=waiting' + '\n'
                            print(_line)
                            self.safe_write(self.path, _line)

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
                                        '\t' + element_type + '\t'\
                                        + param + '\t' + 'action=mesh_analysis' + '\t' + analysis + '\t' + 'status=waiting' + '\n'
                                print(_line)
                                self.safe_write(self.path, _line)

    def add_mekameshing(self, datasets, meshes,
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
                                    + mesh + '\t' + 'action=mekameshing' + '\t' + \
                                    'material_step_type=' + material_step_type + '\t' + \
                                    'material_step=' + material_step + '\t' + \
                                    'min_value=' + min_value + '\t' + \
                                    str([str(m) for m in mechanical_law_list]) + '\t' + 'status=waiting' + '\n'
                            print(_line)
                            self.safe_write(self.path, _line)

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
        # avoid multiple writing at the same time
        # create a lock
        lock = threading.Lock()
        # acquire the lock
        lock.acquire()
        # open the file and write
        with open(self.path, 'r') as file:
            _text = file.read()
        # release the lock
        lock.release()

        return _text


