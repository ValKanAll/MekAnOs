import numpy as np


class Dataset:
    def __init__(self, name, xl_dataset, main_folder, scans_list):
        self.sample_ID_list = xl_dataset['Sample_ID'].to_list()
        self.properties = ['Sample_ID', 'Age', 'Sex', 'Vertebral_level', 'F_exp(N)', 'Disp_exp(mm)', 'Annotation', 'Tumor type']

        self.xl_dataset = xl_dataset
        self.name = name

        self.main_folder = main_folder
        self.scans_list = scans_list
        print(self.scans_list)

        self.chosen_sample_ID_list = []
        for sample_ID in self.sample_ID_list:
            self.chosen_sample_ID_list.append(True)

        self.chosen_segmentation_list = []

    def get_chosen_segmentation_list(self):
        return self.chosen_segmentation_list

    def get_chosen_sample_ID_list(self):
        return self.chosen_sample_ID_list

    def get_name(self):
        return self.name

    def __repr__(self):
        return "Dataset(name={}, n={})".format(self.name, len(self.sample_ID_list))

    def __str__(self):
        return str(self.xl_dataset)

    def get_size(self):
        return len(self.sample_ID_list)

    def get_property_list(self, property=''):
        try:
            L = self.xl_dataset[property].to_list()
        except KeyError:
            raise(KeyError('Property listed is not available, please cite amongst {}'.format(str(self.properties))))

        return L

    def get_property_dict(self, property=''):
        d = dict({})
        try:
            L = self.xl_dataset[property].to_list()
        except KeyError:
            raise(KeyError('Property listed is not available, please cite amongst {}'.format(str(self.properties))))

        for i in range(len(self.sample_ID_list)):
            d[self.sample_ID_list[i]] = L[i]

        return d

    def get_samples_infos(self, property_list):
        samples_properties = []
        for i in range(len(self.sample_ID_list)):
            L = []
            for property in property_list:
                try:
                    L.append(self.xl_dataset[property].to_list()[i])
                except KeyError:
                    L.append(np.nan)
            samples_properties.append(L)
        return samples_properties