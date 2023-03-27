from Workflow.FEA_model import FEA_model
from Global_paths import dataset_path
import os
from Data.Excel_Reader import read_dataset_info
import datetime


class Batch(object):
    def __init__(self, dataset_name, sample_list=None, segmentation_list=['984mic_VB'],
                 mesh_parameters_list=[['QTV', 1]], qctma_parameters_list=[[10, 1]],
                 config_list=['KopEPP07'],
                 model='Lyon', check=True):
        '''

        :param dataset_name:
        :param model:
        :param priority:
        '''
        self.dataset = read_dataset_info(dataset_path, dataset_name)
        self.dataset_name = dataset_name
        if sample_list:
            self.sample_list = sample_list
        else:
            self.sample_list = self.dataset.sample_ID_list

        self.segmentation_list = segmentation_list
        self.mesh_parameters_list = mesh_parameters_list
        self.qctma_parameters_list = qctma_parameters_list
        self.config_list = config_list

        self.model = model
        self.check = check

    def process(self):
        str_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        for sample in self.sample_list:
            print('Sample = {}'.format(sample))
            for segmentation in self.segmentation_list:
                FEmodel = FEA_model(dataset_name=self.dataset_name, sample=sample, segmentation=segmentation)
                FEmodel.detect_endplates(0)

                for mesh_params in self.mesh_parameters_list:
                    element_type, param = mesh_params
                    FEmodel.create_mesh(element_type, param, check=self.check)

                    for qctma_params in self.qctma_parameters_list:
                        delta_E, min_E = qctma_params
                        for config in self.config_list:
                            FEmodel.inject_materials(delta_E, min_E, config, check=self.check)
                            FEmodel.add_endplates(process=True)

                            result_path = os.path.join(self.dataset.main_folder, str_time + '_results_{}.txt'.format(self.model))

                            if self.model == 'Lyon':
                                FEmodel.simulate(result_path, 'UC', None, 'total_strain', 1.9/100, True)





if __name__ == '__main__':
    dataset = 'Wegrzyn et al. (2011)'
    segmentation_list = ['984mic_VB']
    mesh_param_list = [['QTV', 1]]
    qctma_param_list = [[10, 0.1], [10, 0.01], [10, 0.001]]
    config_list = ['KopEPP07']
    model = 'Lyon'
    b = Batch('Wegrzyn et al. (2011)', segmentation_list, mesh_param_list, qctma_param_list, config_list)

    b.process()