import pandas as pd
from Structure.Dataset import Dataset

path = r'D:\MekAnOs_workflow\MekAnos\Data\Samples.xlsx'


def read_dataset_info(_path=path, dataset_name=None):
    """
    Opens excel file with dataset info, 'Dataset_list' sheet contains their names and then each dataset contains a sheet
    :param path: path for excel file
    :return:
    """
    dataset_list = pd.read_excel(_path, sheet_name='Dataset_list', engine='openpyxl')['Source'].tolist()
    year_list = pd.read_excel(_path, sheet_name='Dataset_list', engine='openpyxl')['Year'].tolist()
    main_folder_list = pd.read_excel(_path, sheet_name='Dataset_list', engine='openpyxl')['Main folder'].tolist()
    available_seg_list = pd.read_excel(_path, sheet_name='Dataset_list', engine='openpyxl')['Available_segmentations'].tolist()

    #print(pd.read_excel(_path, sheet_name='Dataset_list'))

    datasets = []

    for k in range(len(dataset_list)):
        dataset = dataset_list[k]
        year = year_list[k]
        main_folder = main_folder_list[k]
        seg_list = available_seg_list[k].replace(' ', '').split(';')
        try:
            xl_dataset = pd.read_excel(_path, sheet_name=dataset, engine='openpyxl')
            if dataset_name:
                if dataset_name == dataset + ' ({})'.format(year):
                    return Dataset(dataset + ' ({})'.format(year), xl_dataset, main_folder, seg_list)
            else:
                datasets += [Dataset(dataset + ' ({})'.format(year), xl_dataset, main_folder, seg_list)]

        except (ValueError, KeyError) as e:
            print(str(e))
            print(str(dataset), 'is empty')

    return datasets




if __name__ == '__main__':
    print(read_dataset_info(path))

