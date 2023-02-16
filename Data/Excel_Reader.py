import pandas as pd
import numpy as np

path = r'D:\MekAnOs_workflow\MekAnos\Data\Samples.xlsx'


def read_dataset_info(_path=path):
    """
    Opens excel file with dataset info, 'Dataset_list' sheet contains their names and then each dataset contains a sheet
    :param path: path for excel file
    :return:
    """
    dataset_list = pd.read_excel(_path, sheet_name='Dataset_list')['Source'].tolist()
    year_list = pd.read_excel(_path, sheet_name='Dataset_list')['Year'].tolist()
    main_folder_list = pd.read_excel(_path, sheet_name='Dataset_list')['Main folder'].tolist()
    structure_list = pd.read_excel(_path, sheet_name='Dataset_list')['Structure'].tolist()
    available_scans_list = pd.read_excel(_path, sheet_name='Dataset_list')['Available_scans'].tolist()

    #print(pd.read_excel(_path, sheet_name='Dataset_list'))

    datasets = []

    for k in range(len(dataset_list)):
        dataset = dataset_list[k]
        year = year_list[k]
        main_folder = main_folder_list[k]
        structure = structure_list[k]
        scans_list = []
        for scan in available_scans_list[k].replace(' ', '').split(';'):
            scan_name, seg_list = scan.replace(')', '').split('(')
            scans_list.append([scan_name, seg_list.split(',')])
        try:
            xl_dataset = pd.read_excel(_path, sheet_name=dataset)
            datasets += [Dataset(dataset + ' ({})'.format(year), xl_dataset, main_folder, structure, scans_list)]

        except (ValueError, KeyError) as e:
            print(str(e))
            print(str(dataset), 'is empty')

    return datasets


class Dataset:
    def __init__(self, name, xl_dataset, main_folder, structure, scans_list):
        self.sample_ID_list = xl_dataset['Sample_ID'].to_list()
        self.properties = ['Sample_ID', 'Age', 'Sex', 'Vertebral_level', 'F_exp(N)', 'Disp_exp(mm)', 'Annotation', 'Tumor type']

        self.xl_dataset = xl_dataset
        self.name = name

        self.main_folder = main_folder
        self.structure = structure
        self.scans_list = scans_list
        print(self.scans_list)

        self.chosen_sample_ID_list = []
        for sample_ID in self.sample_ID_list:
            self.chosen_sample_ID_list.append(True)

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



if __name__ == '__main__':
    print(read_dataset_info(path))

