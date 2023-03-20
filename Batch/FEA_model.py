from Global_paths import dataset_path
import os
from Data.Excel_Reader import read_dataset_info
from Structure.Dataset import Dataset

from Simulation.simulation_functions import simu_gen_mesh, simu_displacement_height
from Geometry_modifyer.SetNamedSelections import detect_endplate, add_endplates_ns
from Material_assignment.qctma import qctma
from Material_assignment.ModifyMechanicalLaw import set_config_meca_for_mekamesh

from Material_assignment.Conversion_equations import gl2density_JPR_HRpQCT, gl2density_IBHGC, gl2density_ARTORG_microCT
from Material_assignment.Conversion_equations import E2density, density2E

from Structure.Mekamesh import Mekamesh


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
            self.stl_path = os.path.join(resolution_folder, self.sample + '_' + self.segmentation + '.stl')
            self.mesh_folder = os.path.join(resolution_folder, "Mesh")
            self.mekamesh_folder = os.path.join(resolution_folder, "Mesh")
            self.gl2density = gl2density_JPR_HRpQCT

        elif self.dataset_name == "Choisne et al. (2018)":
            self.dicom_folder = None
            self.nrrd_path = os.path.join(self.folder_path, 'Seg_VB', 'Seg_' + self.sample[:-3] + '_VB.nrrd')
            self.stl_path = os.path.join(self.folder_path, 'Segmentation', self.sample + '_' + self.segmentation + '.stl')
            self.mesh_folder = os.path.join(self.folder_path, "Mesh")
            self.mekamesh_folder = os.path.join(self.folder_path, "Mekamesh")
            self.gl2density = gl2density_IBHGC

        elif self.dataset_name == "Stadelmann et al. (2020)":
            sample_folder = os.path.join(self.folder_path, self.sample)
            resolution = self.segmentation.split('_')[0]
            self.dicom_folder = os.path.join(sample_folder, self.sample + '_' + resolution + '_DICOM')
            self.nrrd_path = None
            self.stl_path = os.path.join(sample_folder, self.sample + '_' + self.segmentation + '.stl')
            self.mesh_folder = sample_folder
            self.mekamesh_folder = sample_folder
            self.gl2density = gl2density_ARTORG_microCT

    def detect_endplates(self, plot=1, process=False):
        """
        if plot = 0 : no plot
        if plot == 1 : plot vertebra with endplates
        """
        # create pstf file
        if process:
            detect_endplate(self.stl_path, sample=5000, distance=0.2, plot=plot, endplate_height=3)
        self.pstf_file = self.stl_path.replace('.stl', '.pstf')

    def create_mesh(self, element_type='QTV', param=1, process=False, mesh_save_path=""):
        """
        Launch meshing
        """
        self.element_type = element_type
        self.param = param
        if mesh_save_path:
            self.mesh_base = mesh_save_path.split('.cdb')[0]
            self.mesh_path = mesh_save_path
        else:
            self.mesh_base = self.sample + "_" + self.segmentation + "_" + self.element_type + '_' + str(self.param)
            self.mesh_path = os.path.join(self.mesh_folder, self.mesh_base + '.cdb')

        act_script_path = os.path.join(self.act_script_folder, self.mesh_base + '_act_script_path.py')
        wb_script_path = os.path.join(self.wb_script_folder, self.mesh_base + '_wb_script_path.wbjn')

        # Launch simulation
        if process:
            simu_gen_mesh(self.mesh_path, self.stl_path, act_script_path, wb_script_path, self.element_type, self.param)

    def inject_materials(self, delta_E=10, min_E=1, process=False):
        '''
        Define density for each element in the source mesh, based on the dicom and the gray level to Young's modulus
        relationships.
        :param delta_E: material step > 0. In MPa
        :param min_E: minimum value of Young's modulus
        :param process: boolean to process
        :return: path to mesh with density values
        '''
        self.delta_E = delta_E
        self.min_E = min_E
        self.qctma_mesh_base = self.mesh_base + '_qctma_' + str(delta_E) + 'min' + str(min_E)
        self.qctma_mesh_path = os.path.join(self.mekamesh_folder, self.qctma_mesh_base + '.cdb')
        if process:
            qctma(dcm_path=self.dicom_folder, nrrd_path=self.nrrd_path, mesh_path=self.mesh_path, gl2density=self.gl2density,
                    density2E=density2E(min_E), E2density=E2density, deltaE=self.delta_E, coef_poisson=0.3, process=True, save_mesh_path=self.qctma_mesh_path)

        return self.qctma_mesh_path

    def set_constitutive_laws(self, config, process=False, save_mesh_path=''):
        self.mekamesh_base = self.qctma_mesh_base + '_' + config
        self.mekamesh_path = os.path.join(self.mekamesh_folder, self.mekamesh_base + '.cdb')

        if process:
            self.mekamesh = Mekamesh(path=self.qctma_mesh_path)
            self.mekamesh.read()

            set_config_meca_for_mekamesh(self.mekamesh,
                                         config,
                                         write=False)
            self.mekamesh.write()

        else:
            self.mekamesh = Mekamesh(path=self.mekamesh_path)

    def add_endplates(self, pstf_file=None, process=False):
        if process:
            if pstf_file:
                add_endplates_ns(self.mekamesh, pstf_file)
            else:
                add_endplates_ns(self.mekamesh, self.pstf_file)
            self.mekamesh.write()

    def simulate(self, result_path, boundary_conditions='UC', failure_criteria_type='total_strain', value=1.9/100, process=False):
        if process:
            script_base = self.mekamesh_base + '_' + boundary_conditions + '_' + failure_criteria_type + '_' + str(value)
            act_script_path = os.path.join(self.act_script_folder, script_base + '.py')
            wb_script_path = os.path.join(self.wb_script_folder, script_base + '.wbjn')

            if boundary_conditions == 'UC' and failure_criteria_type == 'total_strain':
                simu_displacement_height(self.mekamesh_path, result_path, act_script_path, wb_script_path, value)

if __name__ == '__main__': # pas touche
    pass