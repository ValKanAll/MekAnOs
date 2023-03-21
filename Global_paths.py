import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
print('ROOT_DIR = ', ROOT_DIR)

dataset_path = os.path.join(ROOT_DIR, 'Data', 'Samples.xlsx')

literature_laws_path = os.path.join(ROOT_DIR, 'Data', 'Litterature_laws.mkbl')

ansysWB_path = r"C:\Program Files\ANSYS Inc\v211\Framework\bin\Win64\RunWB2.exe"