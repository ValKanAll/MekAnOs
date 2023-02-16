from FEA_model import *
import os
import xlrd
import numpy as np

stl_path = r""
mesh_save_path = r""  # Path where to save the original mesh created with Ansys Mechanical (MUST ENDS WITH .cdb)
script_save_dir_path = r""  # Path to the directory where scripts will be saved (for revision and tracing purpose)
dicom_dir_path = r""

cdb_path = r""  # Path where to save the result mesh of QCTMA (MUST ENDS WITH .cdb)

# MODEL SPECIFIC
model = FEA_model()
model.create_mesh(stl_path=stl_path, mesh_save_path=mesh_save_path, script_save_dir_path=script_save_dir_path)
model.inject_materials(source_mesh_path=mesh_save_path, dicom_dir_path=dicom_dir_path, out_mesh_path=cdb_path)
