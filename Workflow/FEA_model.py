from Global_paths import dataset_path
import os
from Data.Excel_Reader import read_dataset_info

from Simulation.simulation_functions import simu_gen_mesh, simu_displacement_height, simu_displacement
from Geometry_modifyer.SetNamedSelections import detect_endplate, add_endplates_ns
from Material_assignment.qctma import qctma
from Material_assignment.ModifyMechanicalLaw import set_config_meca_for_mekamesh, get_E_relationship_from_config

from Material_assignment.Conversion_equations import gl2density_JPR_HRpQCT, gl2density_IBHGC, gl2density_ARTORG_microCT

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

    def detect_endplates(self, plot=1, check=True):
        """
        if plot = 0 : no plot
        if plot == 1 : plot vertebra with endplates
        """
        # create pstf file
        self.pstf_file = self.stl_path.replace('.stl', '.pstf')

        if check:
            if not(os.path.isfile(self.pstf_file)):
                detect_endplate(self.stl_path, sample=5000, distance=0.2, plot=plot, endplate_height=3)
        else:
            detect_endplate(self.stl_path, sample=5000, distance=0.2, plot=plot, endplate_height=3)

    def create_mesh(self, element_type='QTV', param=1, check=True, mesh_save_path=""):
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
        if (check and not os.path.isfile(self.mesh_path)) or not check:
            simu_gen_mesh(self.mesh_path, self.stl_path, act_script_path, wb_script_path, self.element_type,
                              self.param)

    def inject_materials(self, delta_E=10, min_E=1, config='KopEPP07', check=True):
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

        self.mekamesh_base = self.qctma_mesh_base + '_' + config
        self.mekamesh_path = os.path.join(self.mekamesh_folder, self.mekamesh_base + '.cdb')

        if (check and not os.path.isfile(self.mekamesh_path)) or not check:
            E_relationship = get_E_relationship_from_config(config)
            E_relationship.set_min_value(self.min_E)
            density2E = E_relationship.get_density2E()
            E2density = E_relationship.get_E2density()
            qctma(dcm_path=self.dicom_folder, nrrd_path=self.nrrd_path, mesh_path=self.mesh_path,
                      gl2density=self.gl2density,
                      density2E=density2E, E2density=E2density, deltaE=self.delta_E, coef_poisson=0.3,
                      process=True, save_mesh_path=self.qctma_mesh_path)

        if (check and not os.path.isfile(self.qctma_mesh_path)) or not check:
            self.mekamesh = Mekamesh(path=self.qctma_mesh_path)
            self.mekamesh.read()
            set_config_meca_for_mekamesh(self.mekamesh, config, write=False)
            self.mekamesh.write()

    def set_constitutive_laws(self, config, check=True, save_mesh_path=''):
        self.mekamesh_base = self.qctma_mesh_base + '_' + config
        self.mekamesh_path = os.path.join(self.mekamesh_folder, self.mekamesh_base + '.cdb')

        if (check and not os.path.isfile(self.qctma_mesh_path)) or not check:
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

    def simulate(self, result_path, boundary_conditions='UC', remote_point=None, failure_criteria_type='total_strain', value=1.9/100, process=False):
        '''
        Launch simulation depending on boundary conditions
        :param result_path: path to export results
        :param boundary_conditions: UC (uni-axial compression), AC (anterior compression)
        :param remote_point: if given load from it, else rigid load from endplate
        :param failure_criteria_type: total_strain for height value (adimension), displacement (mm)
        :param value: depending on failure criteria_type
        :param process: if True, will simulate, won't simulate otherwise
        :return:
        '''
        if process:
            script_base = self.mekamesh_base + '_' + boundary_conditions + '_' + failure_criteria_type + '_' + str(value)
            act_script_path = os.path.join(self.act_script_folder, script_base + '.py')
            wb_script_path = os.path.join(self.wb_script_folder, script_base + '.wbjn')

            if boundary_conditions == 'UC':
                if failure_criteria_type == 'total_strain':
                    simu_displacement_height(self.mekamesh_path, result_path, act_script_path, wb_script_path, value)
                elif failure_criteria_type == 'displacement':
                    simu_displacement(self.mekamesh_path, result_path, act_script_path, wb_script_path, value)

if __name__ == '__main__': # pas touche
    pass