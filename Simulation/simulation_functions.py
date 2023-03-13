import os
import subprocess
import datetime
from Readers.cdb_reader import read_mean_coordinates_named_selection
from Vector_cone_error import rotate_error_cone
import ANSYS_default_scripts.act_scripts as act_scripts
import ANSYS_default_scripts.wb_scripts as wb_scripts
import numpy as np
import copy
from stl import mesh

from Global_paths import ansysWB_path


def distance(point_a, point_b):
    xa, ya, za = point_a
    xb, yb, zb = point_b
    return np.sqrt((xa-xb)**2 + (ya-yb)**2 + (za-zb)**2)


def diff(point_a, point_b):
    xa, ya, za = point_a
    xb, yb, zb = point_b
    return xa-xb, ya-yb, za-zb


def get_height(_mekamesh_path, _result_path):
    try:
        print(_mekamesh_path)
        point_a, point_b = read_mean_coordinates_named_selection(_mekamesh_path, _mekamesh_path, only_endplates=True)
        point_a = np.array(point_a)
        point_b = np.array(point_b)
        h = np.linalg.norm(point_a - point_b)

        _result_file = open(_result_path, 'a')
        _result_file.write(_mekamesh_path + '\t' + str(h) + '\n')

    except FileNotFoundError:
        print("ERROR filenotfound ", _mekamesh_path)


def simu_gen_mesh(_mesh_path, _stl_path, _act_script_path, _wb_script_path, element_type, param):
    print(_mesh_path)

    # linear tetrahedron defined by element volume
    if element_type == 'LTV':
        volume = mesh.Mesh.from_file(_stl_path).get_mass_properties()[0]
        nb_elem = int(volume / param)
        print('elemental volume =', param, 'mm3')
        print('number of elements =', nb_elem)

        act_linear_script = act_scripts.act_script_createMesh_LT_nb_elem
        act_linear_script = act_linear_script.replace("{nb_elem}", str(nb_elem))
        act_linear_script = act_linear_script.replace("{mesh_save_path}", _mesh_path)

    # quadratic tetrahedron defined by element volume
    elif element_type == 'QTV':
        volume = mesh.Mesh.from_file(_stl_path).get_mass_properties()[0]
        nb_elem = int(volume / param)
        print('elemental volume =', param, 'mm3')
        print('number of elements =', nb_elem)

        act_linear_script = act_scripts.act_script_createMesh_QT_nb_elem
        act_linear_script = act_linear_script.replace("{nb_elem}", str(nb_elem))
        act_linear_script = act_linear_script.replace("{mesh_save_path}", _mesh_path)

    # linear tetrahedron defined by number of elements
    elif element_type == 'LTN':
        nb_elem = param
        print('number of elements =', nb_elem)

        act_linear_script = act_scripts.act_script_createMesh_LT_nb_elem
        act_linear_script = act_linear_script.replace("{nb_elem}", str(nb_elem))
        act_linear_script = act_linear_script.replace("{mesh_save_path}", _mesh_path)

    # quadratic tetrahedron defined by number of elements
    elif element_type == 'QTN':
        nb_elem = param
        print('number of elements =', nb_elem)

        act_linear_script = act_scripts.act_script_createMesh_QT_nb_elem
        act_linear_script = act_linear_script.replace("{nb_elem}", str(nb_elem))
        act_linear_script = act_linear_script.replace("{mesh_save_path}", _mesh_path)

    # linear tetrahedron defined by element size
    elif element_type == 'LTS':
        size_elem = param
        print('size of elements =',size_elem, ' mm')

        act_linear_script = act_scripts.act_script_createMesh_LT_size_elem
        act_linear_script = act_linear_script.replace("{size_elem}", str(size_elem))
        act_linear_script = act_linear_script.replace("{mesh_save_path}", _mesh_path)

    # quadratic tetrahedron defined by element size
    elif element_type == 'QTS':
        size_elem = param
        print('size of elements =', size_elem, ' mm')

        act_linear_script = act_scripts.act_script_createMesh_QT_size_elem
        act_linear_script = act_linear_script.replace("{size_elem}", str(size_elem))
        act_linear_script = act_linear_script.replace("{mesh_save_path}", _mesh_path)

    # linear hexahedron defined by element size
    elif element_type == 'LHS':
        size_elem = param
        print('size of elements =', size_elem, ' mm')

        act_linear_script = act_scripts.act_script_createMesh_LH_size_elem
        act_linear_script = act_linear_script.replace("{size_elem}", str(size_elem))
        act_linear_script = act_linear_script.replace("{mesh_save_path}", _mesh_path)

    # quadratic hexahedron defined by element size
    elif element_type == 'QHS':
        size_elem = param
        print('size of elements =', size_elem, ' mm')

        act_linear_script = act_scripts.act_script_createMesh_QH_size_elem
        act_linear_script = act_linear_script.replace("{size_elem}", str(size_elem))
        act_linear_script = act_linear_script.replace("{mesh_save_path}", _mesh_path)

    # linear hexahedron defined by number of divisions
    elif element_type == 'LHD':
        nb_div = param
        print('number of divisions =', nb_div)

        act_linear_script = act_scripts.act_script_createMesh_LH_nb_div
        act_linear_script = act_linear_script.replace("{nb_div}", str(nb_div))
        act_linear_script = act_linear_script.replace("{mesh_save_path}", _mesh_path)

    # quadratic hexahedron defined by number of divisions
    elif element_type == 'QHD':
        nb_div = param
        print('number of divisions =', nb_div)

        act_linear_script = act_scripts.act_script_createMesh_QH_nb_div
        act_linear_script = act_linear_script.replace("{nb_div}", str(nb_div))
        act_linear_script = act_linear_script.replace("{mesh_save_path}", _mesh_path)

    # linear voxel defined by element size
    elif element_type == 'LVS':
        size_elem = param
        print('size of elements =', size_elem, ' mm')

        act_linear_script = act_scripts.act_script_createMesh_LV_size_elem
        act_linear_script = act_linear_script.replace("{size_elem}", str(size_elem))
        act_linear_script = act_linear_script.replace("{mesh_save_path}", _mesh_path)

    # quadratic voxel defined by element size
    elif element_type == 'QVS':
        size_elem = param
        print('size of elements =', size_elem, ' mm')

        act_linear_script = act_scripts.act_script_createMesh_QV_size_elem
        act_linear_script = act_linear_script.replace("{size_elem}", str(size_elem))
        act_linear_script = act_linear_script.replace("{mesh_save_path}", _mesh_path)

    # linear voxel defined by number of divisions
    elif element_type == 'LVD':
        nb_div = param
        print('number of divisions =', nb_div)

        act_linear_script = act_scripts.act_script_createMesh_LV_nb_div
        act_linear_script = act_linear_script.replace("{nb_div}", str(nb_div))
        act_linear_script = act_linear_script.replace("{mesh_save_path}", _mesh_path)

    # quadratic voxel defined by number of divisions
    elif element_type == 'QVD':
        nb_div = param
        print('number of divisions =', nb_div)

        act_linear_script = act_scripts.act_script_createMesh_QV_nb_div
        act_linear_script = act_linear_script.replace("{nb_div}", str(nb_div))
        act_linear_script = act_linear_script.replace("{mesh_save_path}", _mesh_path)

    # TODO orient with pstf file for QH and QV

    with open(_act_script_path, 'w+') as f:
        f.write(act_linear_script)

    wb_script_simulation = wb_scripts.wb_script_createMesh_default
    wb_script_simulation = wb_script_simulation.replace("{stl_path}", _stl_path)
    wb_script_simulation = wb_script_simulation.replace("{act_script_path}", _act_script_path)
    with open(_wb_script_path, 'w+') as f:
        f.write(wb_script_simulation)
    try:
        print("Started at : ", str(datetime.datetime.now()))
        cmd = r'"{}"  -B -R "{}"'.format(ansysWB_path, _wb_script_path)
        print(cmd)
        subprocess.check_call(cmd, shell=True)

        if os.path.isfile(_mesh_path):
            return 0
        else:
            return 1
    except:
        print("ERROR : %s" % _wb_script_path)
        return 1


def simu_EPP(_mekamesh_path, _result_reaction_file, _act_script_path, _wb_script_path, factor=1.9/100, norm=False):
    try:
        print(_mekamesh_path)
        point_a, point_b = read_mean_coordinates_named_selection(_mekamesh_path, _mekamesh_path, only_endplates=True)
        point_a = np.array(point_a)
        point_b = np.array(point_b)
        disp = (point_a - point_b) * factor
        if norm:
            disp = disp / np.linalg.norm(disp)

        print("\tDISPLACEMENT : ", disp, 'mm')
        act_script = act_scripts.act_template_EPP
        act_script = act_script.replace("{result_reaction_file}", _result_reaction_file)
        act_script = act_script.replace("{disp}", str(list(disp)))
        act_script = act_script.replace("{is_EL}", "False")
        act_script = act_script.replace("{ID_mekamesh}", _mekamesh_path.split('\\')[-1].split('.cdb')[0])
        with open(_act_script_path, 'w+') as f:
            f.write(act_script)

        _wb_script_simulation = wb_scripts.wb_script_simulation_EPP
        _wb_script_simulation = _wb_script_simulation.replace("{mekamesh_path}", _mekamesh_path)
        _wb_script_simulation = _wb_script_simulation.replace("{path_act}", _act_script_path)

        with open(_wb_script_path, 'w+') as f:
            f.write(_wb_script_simulation)

        _cmd = r'"C:\Program Files\ANSYS Inc\v211\Framework\bin\Win64\RunWB2.exe"  -B -R "%s"' % _wb_script_path
        print("\tCMD: ", _cmd)
        t0 = datetime.datetime.now()
        print("\tStarted at: ", t0)
        subprocess.check_call(_cmd, shell=True)
        t1 = datetime.datetime.now()
        print("\tDuration: ", t1 - t0)
    except (subprocess.CalledProcessError, FileNotFoundError) as error:
        print(error)
        print("### ERROR : %s" % _mekamesh_path)


def simu_EPP_all_times(_mekamesh_path, _result_reaction_file, _results_folder, _act_script_path, _wb_script_path, factor=1.9/100):
    try:
        print(_mekamesh_path)
        point_a, point_b = read_mean_coordinates_named_selection(_mekamesh_path, _mekamesh_path, only_endplates=True)
        point_a = np.array(point_a)
        point_b = np.array(point_b)
        disp = (point_a - point_b) * factor

        print("\tDISPLACEMENT : ", disp, 'mm')
        act_script = act_scripts.act_template_EPP_all_times
        act_script = act_script.replace("{results_folder}", _results_folder)
        act_script = act_script.replace("{result_reaction_file}", _result_reaction_file)
        act_script = act_script.replace("{disp}", str(list(disp)))
        act_script = act_script.replace("{ID_mekamesh}", _mekamesh_path.split('\\')[-1].split('.cdb')[0])
        with open(_act_script_path, 'w+') as f:
            f.write(act_script)

        _wb_script_simulation = wb_scripts.wb_script_simulation_EPP
        _wb_script_simulation = _wb_script_simulation.replace("{mekamesh_path}", _mekamesh_path)
        _wb_script_simulation = _wb_script_simulation.replace("{path_act}", _act_script_path)

        with open(_wb_script_path, 'w+') as f:
            f.write(_wb_script_simulation)

        _cmd = r'"C:\Program Files\ANSYS Inc\v211\Framework\bin\Win64\RunWB2.exe"  -B -R "%s"' % _wb_script_path
        print("\tCMD: ", _cmd)
        t0 = datetime.datetime.now()
        print("\tStarted at: ", t0)
        subprocess.check_call(_cmd, shell=True)
        t1 = datetime.datetime.now()
        print("\tDuration: ", t1 - t0)
    except (subprocess.CalledProcessError, FileNotFoundError) as error:
        print(error)
        print("### ERROR : %s" % _mekamesh_path)


def simu_EL(_mekamesh_path, _result_reaction_file, _volume_path, _stress_path, _strain_path,
                                                _act_script_path, _wb_script_path, factor=1.9/100, disp_value=1
                                                 ):
    try:
        print(_mekamesh_path)
        point_a, point_b = read_mean_coordinates_named_selection(_mekamesh_path, _mekamesh_path, only_endplates=True)
        point_a = np.array(point_a)
        point_b = np.array(point_b)
        disp = (point_a - point_b) * factor
        if disp_value:
            disp = disp_value * disp / np.linalg.norm(disp)

        print("\tDISPLACEMENT : ", disp, 'mm')
        act_script = act_scripts.act_template_EPP
        act_script = act_script.replace("{result_reaction_file}", _result_reaction_file)
        act_script = act_script.replace("{volume_path}", _volume_path)
        act_script = act_script.replace("{strain_path}", _strain_path)
        act_script = act_script.replace("{stress_path}", _stress_path)
        act_script = act_script.replace("{is_EL}", "True")
        act_script = act_script.replace("{disp}", str(list(disp)))
        act_script = act_script.replace("{ID_mekamesh}", _mekamesh_path.split('\\')[-1].split('.cdb')[0])
        with open(_act_script_path, 'w+') as f:
            f.write(act_script)

        _wb_script_simulation = wb_scripts.wb_script_simulation_EPP
        _wb_script_simulation = _wb_script_simulation.replace("{mekamesh_path}", _mekamesh_path)
        _wb_script_simulation = _wb_script_simulation.replace("{path_act}", _act_script_path)

        with open(_wb_script_path, 'w+') as f:
            f.write(_wb_script_simulation)

        _cmd = r'"C:\Program Files\ANSYS Inc\v211\Framework\bin\Win64\RunWB2.exe"  -B -R "%s"' % _wb_script_path
        print("\tCMD: ", _cmd)
        t0 = datetime.datetime.now()
        print("\tStarted at: ", t0)
        subprocess.check_call(_cmd, shell=True)
        t1 = datetime.datetime.now()
        print("\tDuration: ", t1 - t0)
    except subprocess.CalledProcessError as error:
        print(error)
        print("### ERROR : %s" % _mekamesh_path)


def simu_get_volume(_mesh_path, _volume_path, _act_script_path, _wb_script_path):
    try:
        act_script = act_scripts.act_template_get_volume
        act_script = act_script.replace("{volume_path}", _volume_path)
        with open(_act_script_path, 'w+') as f:
            f.write(act_script)

        _wb_script_simulation = wb_scripts.wb_script_simulation_EPP
        _wb_script_simulation = _wb_script_simulation.replace("{mekamesh_path}", _mesh_path)
        _wb_script_simulation = _wb_script_simulation.replace("{path_act}", _act_script_path)

        with open(_wb_script_path, 'w+') as f:
            f.write(_wb_script_simulation)

        _cmd = r'"C:\Program Files\ANSYS Inc\v211\Framework\bin\Win64\RunWB2.exe"  -B -R "%s"' % _wb_script_path
        print("\tGET VOLUME of {}\n".format(_mesh_path))
        print("\tCMD: ", _cmd)
        t0 = datetime.datetime.now()
        print("\tStarted at: ", t0)
        subprocess.check_call(_cmd, shell=True)
        t1 = datetime.datetime.now()
        print("\tDuration: ", t1 - t0)
    except subprocess.CalledProcessError as error:
        print(error)
        print("### ERROR : %s" % _mesh_path)


def simu_gen_mesh_from_elemental_volume(_mesh_path, _stl_path, _act_script_path, _wb_script_path, volume_elem, element_type, edit=False):
    print(_mesh_path)
    volume = mesh.Mesh.from_file(_stl_path).get_mass_properties()[0]
    nb_elem = int(volume / volume_elem)
    print('elemental volume =', volume_elem, 'mm3')
    print('number of elements =', nb_elem)

    act_linear_script = act_scripts.act_script_createMesh_default
    act_linear_script = act_linear_script.replace("{type_elem}", element_type)
    act_linear_script = act_linear_script.replace("{size_elem}", 'None')
    act_linear_script = act_linear_script.replace("{nb_elem} * 1000", str(nb_elem))
    act_linear_script = act_linear_script.replace("{mesh_save_path}", _mesh_path)
    with open(_act_script_path, 'w+') as f:
        f.write(act_linear_script)

    wb_script_simulation = wb_scripts.wb_script_createMesh_default
    wb_script_simulation = wb_script_simulation.replace("{stl_path}", _stl_path)
    wb_script_simulation = wb_script_simulation.replace("{act_script_path}", _act_script_path)
    wb_script_simulation = wb_script_simulation.replace("{edit}", str(edit))
    with open(_wb_script_path, 'w+') as f:
        f.write(wb_script_simulation)
    try:
        print("Started at : ", str(datetime.datetime.now()))
        cmd = r'"C:\Program Files\ANSYS Inc\v211\Framework\bin\Win64\RunWB2.exe"  -B -R "%s"' % _wb_script_path
        print(cmd)
        subprocess.check_call(cmd, shell=True)
    except:
        print("ERROR : %s" % _wb_script_path)


def simu_EPP_remote_point(_mekamesh_path, _result_reaction_file, _results_folder, _act_script_path, _wb_script_path, remote_point,
                          all_times=False, factor=1.9/100, n=0, theta=5):#3/100
    try:
        print(_mekamesh_path)
        point_a, point_b = read_mean_coordinates_named_selection(_mekamesh_path, _mekamesh_path, only_endplates=True)
        point_a = np.array(point_a)
        point_b = np.array(point_b)

        if distance(remote_point, point_a) < distance(remote_point, point_b):
            disp = (point_b - point_a) * factor
            print('Distance_endplate: ', np.linalg.norm(point_b-point_a))
            print('Disp: ', np.linalg.norm(disp))
            top_index = 1
            bottom_index = 2
        else:
            disp = (point_a - point_b) * factor
            top_index = 2
            bottom_index = 1
        disp_list = [disp]
        if n > 1:
            disp_list += rotate_error_cone(copy.deepcopy(disp), n, theta)

        print("\tDISPLACEMENT : ", disp, 'mm')
        act_script = act_scripts.act_template_EPP_remote_point
        act_script = act_script.replace("{result_reaction_file}", _result_reaction_file)
        act_script = act_script.replace("{results_folder}", _results_folder)
        act_script = act_script.replace("{disp_list}", str([list(d) for d in disp_list]))
        act_script = act_script.replace("{all_times}", str(all_times))
        act_script = act_script.replace("{remote_point}", str(remote_point))
        act_script = act_script.replace("{top_index}", str(top_index))
        act_script = act_script.replace("{bottom_index}", str(bottom_index))
        act_script = act_script.replace("{ID_mekamesh}", _mekamesh_path.split('\\')[-1].split('.cdb')[0])
        with open(_act_script_path, 'w+') as f:
            f.write(act_script)

        _wb_script_simulation = wb_scripts.wb_script_simulation_EPP
        _wb_script_simulation = _wb_script_simulation.replace("{mekamesh_path}", _mekamesh_path)
        _wb_script_simulation = _wb_script_simulation.replace("{path_act}", _act_script_path)

        with open(_wb_script_path, 'w+') as f:
            f.write(_wb_script_simulation)

        _cmd = r'"C:\Program Files\ANSYS Inc\v211\Framework\bin\Win64\RunWB2.exe"  -B -R "%s"' % _wb_script_path
        print("\tCMD: ", _cmd)
        t0 = datetime.datetime.now()
        print("\tStarted at: ", t0)
        subprocess.check_call(_cmd, shell=True)
        t1 = datetime.datetime.now()
        print("\tDuration: ", t1 - t0)
    except subprocess.CalledProcessError as error:
        print(error)
        print("### ERROR : %s" % _mekamesh_path)


def simu_EPP_center_remote_point(_mekamesh_path, _result_reaction_file, _results_folder, _act_script_path, _wb_script_path, distance,
                          all_times=False, factor=1.9/100, n=0, theta=5):#3/100
    try:
        print(_mekamesh_path)
        point_a, point_b = read_mean_coordinates_named_selection(_mekamesh_path, _mekamesh_path, only_endplates=True)
        point_a = np.array(point_a)
        point_b = np.array(point_b)

        remote_point = list((point_b - point_a) / np.linalg.norm(point_b-point_a) * distance + point_b)
        disp = (point_a - point_b) * factor
        top_index = 2
        bottom_index = 1
        disp_list = [disp]
        if n > 1:
            disp_list += rotate_error_cone(copy.deepcopy(disp), n, theta)

        print("\tDISPLACEMENT : ", disp, 'mm')
        act_script = act_scripts.act_template_EPP_remote_point
        act_script = act_script.replace("{result_reaction_file}", _result_reaction_file)
        act_script = act_script.replace("{results_folder}", _results_folder)
        act_script = act_script.replace("{disp_list}", str([list(d) for d in disp_list]))
        act_script = act_script.replace("{all_times}", str(all_times))
        act_script = act_script.replace("{remote_point}", str(remote_point))
        act_script = act_script.replace("{top_index}", str(top_index))
        act_script = act_script.replace("{bottom_index}", str(bottom_index))
        act_script = act_script.replace("{ID_mekamesh}", _mekamesh_path.split('\\')[-1].split('.cdb')[0])
        with open(_act_script_path, 'w+') as f:
            f.write(act_script)

        _wb_script_simulation = wb_scripts.wb_script_simulation_EPP
        _wb_script_simulation = _wb_script_simulation.replace("{mekamesh_path}", _mekamesh_path)
        _wb_script_simulation = _wb_script_simulation.replace("{path_act}", _act_script_path)

        with open(_wb_script_path, 'w+') as f:
            f.write(_wb_script_simulation)

        _cmd = r'"C:\Program Files\ANSYS Inc\v211\Framework\bin\Win64\RunWB2.exe"  -B -R "%s"' % _wb_script_path
        print("\tCMD: ", _cmd)
        t0 = datetime.datetime.now()
        print("\tStarted at: ", t0)
        subprocess.check_call(_cmd, shell=True)
        t1 = datetime.datetime.now()
        print("\tDuration: ", t1 - t0)
    except subprocess.CalledProcessError as error:
        print(error)
        print("### ERROR : %s" % _mekamesh_path)

