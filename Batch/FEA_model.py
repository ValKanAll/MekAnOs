import numpy as np
import warnings
import ANSYS_default_scripts.wb_scripts as wb_scripts
import ANSYS_default_scripts.act_scripts as act_scripts
import os
import subprocess
import qctma


class FEA_model(object):

    def __init__(self):
        self.ansysWB_path = r"C:\Program Files\ANSYS Inc\v211\Framework\bin\Win64\RunWB2.exe"
        self.type_elem = 'tet'  # if 'tet', create a tetrahedral mesh; if 'voxel', create a cartesian mesh (voxel-based hexaedral).
        self.order_elem = 2  # Either 1 (first order element) or 2 (second order element).
        self.size_elem = None  # Size of the element (may be None if nb_elem is not None).
        self.nb_elem = None  # Total number of elements (may be None if size_elem is not None).
        self.deltaE = 0  # Step between each material definition (MPa) (if 0, each element will have a specific material).

    def gl2density(self, gl_array):
        """
        Transforms the grey level value to a density value (the equation is obtained with the help of a phantom).
        :param gl_array: Array or value of the pixels' gray level.
        :return: The associated density.
        """

        return np.array(gl_array)

    def density2E(self, density_mat):
        """
        Transforms the density values to Young's modulus values.
        :param density_array: Array or value of the density.
        :return: The associated Young's modulus.
        """

        return np.array(density_mat)

    def act_script_mesh_creation(self, type_elem='tet', order_elem=2, size_elem=None, nb_elem=None, mesh_save_path=""):
        """
        Create an Ansys Mechanical (ACT) script file for mesh creation.
        :param type_elem: if 'tet', create a tetrahedral mesh; if 'voxel', create a cartesian mesh (voxel-based hexaedral).
        :param order_elem: Either 1 (first order element) or 2 (second order element).
        :param size_elem: size of the element (may be None if nb_elem is not None).
        :param nb_elem: Total number of elements (may be None if size_elem is not None).
        :param mesh_save_path: Path to the mesh that will be created. If "", the path will be the same as stl_path,
        with the extension changed with '.cdb"
        :return act_create_mesh_script: String containing the script to use with Ansys Mechanical to create a mesh.
        """
        if not size_elem and not nb_elem:
            raise ValueError("size_elem and nb_elem are both None. Please assign a value to one of both.")
        if size_elem and nb_elem:
            raise ValueError("size_elem and nb_elem are both assigned. Please assign a value to ONLY one of both.")
        if type_elem == 'voxel' and not size_elem:
            raise ValueError("'voxel' type only accepts size_elem to define the number and size of elements. Please assign a value to size_elem.")

        act_create_mesh_script = act_scripts.act_script_createMesh_default
        act_create_mesh_script = act_create_mesh_script.replace("{type_elem}", str(type_elem))
        act_create_mesh_script = act_create_mesh_script.replace("{order_elem}", str(order_elem))
        act_create_mesh_script = act_create_mesh_script.replace("{size_elem}", str(size_elem))
        act_create_mesh_script = act_create_mesh_script.replace("{nb_elem}", str(nb_elem))
        act_create_mesh_script = act_create_mesh_script.replace("{mesh_save_path}", mesh_save_path)

        return act_create_mesh_script

    def wb_script_mesh_creation(self, stl_path="", act_script_path=""):
        """
        Create an Ansys Workbench script file for mesh creation.
        :param stl_path: Path to the STL file.
        :param act_script_path: Path to the ACT script file to create the mesh in Ansys Mechanical.
        :return wb_create_mesh_script: String containing the script to use with Workbench to create a mesh.
        """
        if stl_path == "":
            raise ValueError("The STL path is empty.")
        if act_script_path == "":
            raise ValueError("The ACT script file path is empty.")

        wb_create_mesh_script = wb_scripts.wb_script_createMesh_default
        wb_create_mesh_script = wb_create_mesh_script.replace("{stl_path}", str(stl_path))
        wb_create_mesh_script = wb_create_mesh_script.replace("{act_script_path}", str(act_script_path))

        return wb_create_mesh_script

    def create_mesh(self, stl_path="", mesh_save_path="", script_save_dir_path=None):
        """
        Create .CDB mesh with Ansys Workbench process.
        :param stl_path: see wb_script_mesh_creation.
        :param mesh_save_path: see act_script_mesh_creation.
        :param script_save_dir_path: Path to the directory in which Workbench and ACT scripts will be saved.
        :return mesh_save_path:
        """
        if not script_save_dir_path:
            warnings.warn("'script_save_dir_path' is empty.\n"
                          "Scripts will be saved in directory 'Scripts' in the same directory as the STL file.")
            script_save_dir_path = os.path.join(os.path.split(stl_path)[0], "Scripts")
        if not os.path.exists(script_save_dir_path):
            os.makedirs(script_save_dir_path)
        if not os.path.exists(os.path.split(mesh_save_path)[0]):
            os.makedirs(os.path.split(mesh_save_path)[0])

        act_script_path = os.path.join(script_save_dir_path, "ACT_mesh_creation.py")
        with open(act_script_path, 'w+') as f:
            f.write(
                self.act_script_mesh_creation(type_elem=self.type_elem, order_elem=self.order_elem, size_elem=self.size_elem,
                                              nb_elem=self.nb_elem, mesh_save_path=mesh_save_path)
            )

        wb_script_path = os.path.join(script_save_dir_path, "WB_mesh_creation.wbjn")
        with open(wb_script_path, 'w+') as f:
            f.write(
                self.wb_script_mesh_creation(stl_path=stl_path, act_script_path=act_script_path)
            )

        cmd = f'"{self.ansysWB_path}" -B -R "{wb_script_path}"'
        subprocess.check_call(cmd, shell=True)
        return mesh_save_path

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