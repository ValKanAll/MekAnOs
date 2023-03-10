from Global_paths import dataset_path
import os
from Data.Excel_Reader import read_dataset_info, Dataset

from Simulation.simulation_functions import simu_gen_mesh


class FEA_model(object):

    def __init__(self, dataset_name, sample, segmentation):
        self.dataset = read_dataset_info(dataset_path, dataset_name)
        self.dataset_name = dataset_name  # dataset name
        self.sample = sample  # sample ID
        self.segmentation = segmentation  # segmentation name

        # Define file and path folders for each datasets

        self.folder_path = self.dataset.main_folder
        self.act_script_folder = os.path.join(self.folder_path, 'ACT_scripts')
        self.wb_script_folder = os.path.join(self.folder_path, 'WB_scripts')

        if self.dataset_name == "Wegrzyn et al. (2011)":
            resolution = self.segmentation.split('_')[0]
            resolution_folder = os.path.join(self.folder_path, self.sample, self.sample + '_' + resolution)
            self.dicom_folder = os.path.join(resolution_folder, self.sample + '_' + resolution + '_DICOM')
            self.nrrd_path = None
            self.stl_path = os.path.join(resolution_folder, self.sample + '_' + self.segmentation)
            self.mesh_folder = os.path.join(resolution_folder, "Mesh")
            self.mekamesh_folder = os.path.join(resolution_folder, "Mesh")

        elif self.dataset_name == "Choisne et al. (2018)":
            self.dicom_folder = None
            self.nrrd_path = os.path.join(self.folder_path, 'Seg_VB', 'Seg_' + self.sample[:-3] + '_VB.nrrd')
            self.stl_path = os.path.join(self.folder_path, 'Segmentation', self.sample + '_' + self.segmentation + '.stl')
            self.mesh_folder = os.path.join(self.folder_path, "Mesh")
            self.mekamesh_folder = os.path.join(self.folder_path, "Mekamesh")

        elif self.dataset_name == "Stadelmann et al. (2020)":
            sample_folder = os.path.join(self.folder_path, self.sample)
            resolution = self.segmentation.split('_')[0]
            self.dicom_folder = os.path.join(sample_folder, self.sample + '_' + resolution + '_DICOM')
            self.nrrd_path = None
            self.stl_path = os.path.join(sample_folder, self.sample + '_' + self.segmentation + '.stl')
            self.mesh_folder = sample_folder
            self.mekamesh_folder = sample_folder

    def create_mesh(self, element_type='QTV', param=1, mesh_save_path=""):
        """
        Launch meshing
        """
        self.element_type = element_type
        self.param = param
        if mesh_save_path:
            self.mesh_base = mesh_save_path.split('.cdb')[0]
            self.mesh_path = mesh_save_path
        else:
            self.mesh_base = self.sample + "_" + self.segmentation + "_" + self.element_type + '_' + self.param
            self.mesh_path = os.path.join(self.mesh_folder, self.mesh_base, self.mesh_base + '.cdb')

        act_script_path = os.path.join(self.act_script_folder, self.mesh_base + '_act_script_path.py')
        wb_script_path = os.path.join(self.wb_script_folder, self.mesh_base + '_wb_script_path.py')

        # Launch simulation
        simu_gen_mesh(self.mesh_path, self.stl_path, act_script_path, wb_script_path, self.element_type, self.param)


    def inject_materials(self, source_mesh_path="", dicom_dir_path="", out_mesh_path=""):
        """
        Define material for each element in the source mesh, based on the dicom and the gray level to Young's modulus
        relationships.
        :param source_mesh_path: Path to the original mesh.
        :param dicom_dir_path: Path to the Dicom directory.
        :param out_mesh_path: Path to the final mesh that will be created. Maybe void, in that case, it will be saved in
        the same directory and with the same name as the source mesh with a "_qctma" appendix.
        :return out_mesh_path:
        """
        qctma.qctma(dcm_path=dicom_dir_path, mesh_path=source_mesh_path, gl2density=self.gl2density,
                    density2E=self.density2E, deltaE=self.deltaE, process=True, save_mesh_path=out_mesh_path)

        return out_mesh_path

    def set_constitutive_laws(self, laws=[], save_mesh_path=''):
        pass

    def set_boundary_conditions(self, pstf_file_path=''):
        pass

    def simulate(self):
        pass