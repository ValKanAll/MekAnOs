from module.Structure.Mesh import Mesh
import numpy as np
from functools import partial
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pycpd.rigid_registration import RigidRegistration
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from math import (asin, pi, atan2, cos)
from module.Converters.Displayer import add_points2graph
from module.Structure.STL import STL
from module.Converters.SetNamedSelections import add_endplates_ns


def rototranslate_mesh(mesh, rotomatrix, new_path=None):
    mesh.read()
    node_list = mesh.get_node_list()
    for node in node_list:
        coord = node.get_coord()
        new_coord = rotomatrix.dot(np.transpose(np.array([coord[0], coord[1], coord[2], 1])))
        node.set_coord(new_coord[0], new_coord[1], new_coord[2])
    mesh.write(new_path)
    return mesh


def visualize(iteration, error, X, Y, ax, flip):
    plt.cla()
    ax.scatter(X[:, 0],  X[:, 1], X[:, 2], color='red', label='Target', s=1)
    ax.scatter(Y[:, 0],  Y[:, 1], Y[:, 2], color='blue', label='Source', s=1)
    ax.text2D(0.87, 0.92, 'Iteration: {:d}\nQ: {:06.4f}'.format(
        iteration, error), horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize='x-small')
    ax.legend(loc='lower right', fontsize='xx-small')
    ax.set_title(flip)
    plt.draw()
    plt.pause(0.00001)


def fit_data(target_data, source_data, check=False, is_print_info=False):
    '''
    Fit data from source to target and also flips data around each axes
    :param target_data: (X) data points you wish to target, they do not move
    :param source_data: (Y) data points you wish to transform to fit the target, they are transformed
    :param check: if True, check the solution and shows it on a plotly graph with the target data
    :param is_print_info: if True, prints info and plots graphs
    :return: Result = rotation matrix (R), translation matrix (T), transformed data (Y_T)
            Y_T = R*Y + T, R may contain a flip around one axis
    '''

    fig = plt.figure()

# INIT SOLVE
    ax1 = fig.add_subplot(221, projection='3d')
    callback1 = partial(visualize, ax=ax1, flip='Init mesh')
    X = target_data
    Y = source_data
    reg = RigidRegistration(**{'X': X, 'Y': Y})
    TY_1, rot_mat_1, trans_mat_1, [q_1, iteration_1] = reg.register(callback1)

    if is_print_info:
        print("Init solved")
        print("Rotation matrix : \n", rot_mat_1)
        print("Translation : \n", trans_mat_1)
        print('Q : ', q_1)
        print('Number of iteration : ', iteration_1)
    else:
        print("Init solved")
        print('Q : ', q_1)
        print('Number of iteration : ', iteration_1)


# 180FLIP_Z SOLVE
    ax2 = fig.add_subplot(222, projection='3d')
    callback2 = partial(visualize, ax=ax2, flip='180 flip Z')
    rot_180_z = np.array([[-1.0, 0.0, 0.0],
                        [0.0, -1.0, 0.0],
                        [0.0, 0.0, 1.0]])

    Y_180_z = np.dot(Y, rot_180_z)
    reg = RigidRegistration(**{'X': X, 'Y': Y_180_z})
    TY_2, rot_mat_2, trans_mat_2, [q_2, iteration_2] = reg.register(callback2)
    rot_mat_z = np.dot(rot_180_z, rot_mat_2)  # take account of flip

    if is_print_info:
        print("180flip Z solved")
        print("Rotation matrix : \n", rot_mat_z)
        print("Translation : \n", trans_mat_2)
        print('Q : ', q_2)
        print('Number of iteration : ', iteration_2)
    else:
        print("180flip Z solved")
        print('Q : ', q_2)
        print('Number of iteration : ', iteration_2)


# 180FLIP_Y SOLVE
    ax3 = fig.add_subplot(223, projection='3d')
    callback3 = partial(visualize, ax=ax3, flip='180 flip Y')
    rot_180_y = np.array([[-1.0, 0.0, 0.0],
                          [0.0, 1.0, 0.0],
                          [0.0, 0.0, -1.0]])
    Y_180_y = np.dot(Y, rot_180_y)
    reg = RigidRegistration(**{'X': X, 'Y': Y_180_y})
    TY_3, rot_mat_3, trans_mat_3, [q_3, iteration_3] = reg.register(callback3)
    rot_mat_y = np.dot(rot_180_y, rot_mat_3)  # take account of flip

    if is_print_info:
        print("180flip Y solved")
        print("Rotation matrix : \n", rot_mat_y)
        print("Translation : \n", trans_mat_3)
        print('Q : ', q_3)
        print('Number of iteration : ', iteration_3)
    else:
        print("180flip Y solved")
        print('Q : ', q_3)
        print('Number of iteration : ', iteration_3)

# 180FLIP_X SOLVE
    ax4 = fig.add_subplot(224, projection='3d')
    callback4 = partial(visualize, ax=ax4, flip='180 flip X')
    rot_180_x = np.array([[1, 0, 0],
                          [0, -1, 0],
                          [0, 0, -1]])
    Y_180_x = np.dot(Y, rot_180_x)
    reg = RigidRegistration(**{'X': X, 'Y': Y_180_x})
    TY_4, rot_mat_4, trans_mat_4, [q_4, iteration_4] = reg.register(callback4)
    rot_mat_x = np.dot(rot_180_x, rot_mat_4)  # take account of flip

    if is_print_info:
        print("180flip X solved")
        print("Rotation matrix : \n", rot_mat_x)
        print("Translation : \n", trans_mat_4)
        print('Q : ', q_4)
        print('Number of iteration : ', iteration_4)
    else:
        print("180flip X solved")
        print('Q : ', q_4)
        print('Number of iteration : ', iteration_4)


# FIND BEST SOLUTION
    min_q = min([q_1, q_2, q_3, q_4])
    print("### Min Q: ", min_q)
    if min_q == q_1:
        print("Best resolution is: INIT")
        print("Rotation matrix : \n", rot_mat_1)
        print("Translation : \n", trans_mat_1)
        print('Q : ', q_1)
        print('Number of iteration : ', iteration_1)
        result = rot_mat_1, trans_mat_1, TY_1

    elif min_q == q_2:
        print("Best resolution is: FLIP Z")
        print("Rotation matrix : \n", rot_mat_z)
        print("Translation : \n", trans_mat_2)
        print('Q : ', q_2)
        print('Number of iteration : ', iteration_2)
        result = rot_mat_z, trans_mat_2,  TY_2

    elif min_q == q_3:
        print("Best resolution is: FLIP Y")
        print("Rotation matrix : \n", rot_mat_y)
        print("Translation : \n", trans_mat_3)
        print('Q : ', q_3)
        print('Number of iteration : ', iteration_3)
        result = rot_mat_y, trans_mat_3, TY_3

    elif min_q == q_4:
        print("Best resolution is: FLIP X")
        print("Rotation matrix : \n", rot_mat_x)
        print("Translation : \n", trans_mat_4)
        print('Q : ', q_4)
        print('Number of iteration : ', iteration_4)
        result = rot_mat_x, trans_mat_4, TY_4

    if check:
        # check the solution and plot it
        reg = RigidRegistration(**{'X': X, 'Y': np.dot(Y, result[0]) + result[1]})
        res2, rot_mat, trans_mat, [_, _] = reg.register()
        print("### Checking results")
        print(rot_mat, trans_mat)

        layout = go.Layout(scene=dict(aspectmode='data'))  # equal scale step
        fig = go.Figure(layout=layout)
        add_points2graph(fig, X, 'X')
        add_points2graph(fig, np.dot(Y, result[0]) + result[1], 'Y*R+T')
        add_points2graph(fig, result[2], 'TY')
        add_points2graph(fig, res2, 'TY_2')
        fig.show()

    #plt.show()

    return result


def euler_angles_from_rot_mat(rot_mat, is_deg=False):
    '''
    Illustration of the rotation matrix / sometimes called 'orientation' matrix
    R = [
           R11 , R12 , R13,
           R21 , R22 , R23,
           R31 , R32 , R33
        ]
    REMARKS:
    1. this implementation is meant to make the mathematics easy to be deciphered
    from the script, not so much on 'optimized' code.
    You can then optimize it to your own style.

    2. I have utilized naval rigid body terminology here whereby;
    2.1 roll -> rotation about x-axis
    2.2 pitch -> rotation about the y-axis
    2.3 yaw -> rotation about the z-axis (this is pointing 'upwards')
    Transform 3x3 matrix in euler angles
    :param rot_mat: rotation matrix as 3x3 matrix
    :param is_deg: default results are in radians, if True they will be in degrees
    :return: euler angles Th_x (roll), Th_y (pitch), Th_z (yaw) in radians (default)
    '''
    R11, R12, R13 = rot_mat[0]
    R21, R22, R23 = rot_mat[1]
    R31, R32, R33 = rot_mat[2]

    if R31 != 1 and R31 != -1:
        pitch_1 = -1 * asin(R31)
        pitch_2 = pi - pitch_1
        roll_1 = atan2(R32 / cos(pitch_1), R33 / cos(pitch_1))
        roll_2 = atan2(R32 / cos(pitch_2), R33 / cos(pitch_2))
        yaw_1 = atan2(R21 / cos(pitch_1), R11 / cos(pitch_1))
        yaw_2 = atan2(R21 / cos(pitch_2), R11 / cos(pitch_2))

        # IMPORTANT NOTE here, there is more than one solution but we choose the first for this case for simplicity !
        # You can insert your own domain logic here on how to handle both solutions appropriately (see the reference publication link for more info).
        pitch = pitch_1
        roll = roll_1
        yaw = yaw_1
    else:
        yaw = 0  # anything (we default this to zero)
        if R31 == -1:
            pitch = pi / 2
            roll = yaw + atan2(R12, R13)
        else:
            pitch = -pi / 2
            roll = -1 * yaw + atan2(-1 * R12, -1 * R13)

    # convert from radians to degrees
    if is_deg:
        roll = roll * 180 / pi
        pitch = pitch * 180 / pi
        yaw = yaw * 180 / pi

    return roll, pitch, yaw


def fit_data_and_transform(target_path, source_path, save_path=None, check=False):
    """
    Fit data from source to target with Coherent Point Drift (CPD) method
    and also flips data around each axes to make sure of the orientation
    and saves the result as a new mesh

    :param target_path: path to target stl (which will NOT be transformed)
    :param source_path: path to source stl (which will be transformed)
    :param save_path: if not None the new mesh will be saved at this path address
    :param check: if True will plot meshes to see if they fit
    :return: source stl mesh from source path transformed to fit target
    """

    source_stl = STL(source_path)
    target_stl = STL(target_path)

    r, t, yt = fit_data(
        target_data=target_stl.get_sample_points(),
        source_data=source_stl.get_sample_points(),
        check=check,
        is_print_info=check)

    new_stl = source_stl.transform_stl(r, t, True)

    if check:
        X = target_stl.get_sample_points()
        new_stl_points = new_stl.get_sample_points()

        layout = go.Layout(scene=dict(aspectmode='data'))  # equal scale step
        fig = go.Figure(layout=layout)
        add_points2graph(fig, yt, 'transformed source from CPD')
        add_points2graph(fig, new_stl_points, 'transformed source from new stl')
        add_points2graph(fig, X, 'source')
        fig.show()

    if save_path or save_path == "":
        if save_path == "":
            save_path = source_path.split('.stl')[0] + '_transformed.stl'
            print(save_path)
        new_stl.save(save_path)

    return new_stl


def fit_data_and_rotate_mesh(target_stl_path, source_stl_path, init_mesh_path, transformed_mesh_path, check=False):
    """
        Fit data from source to target with Coherent Point Drift (CPD) method
        and also flips data around each axes to make sure of the orientation
        and saves the result as a new mesh

        :param target_stl_path: path to target stl (which will NOT be transformed)
        :param source_stl_path: path to source stl (which will be transformed)
        :param save_path: if not None the new mesh will be saved at this path address
        :param check: if True will plot meshes to see if they fit
        :return: source stl mesh from source path transformed to fit target
        """

    source_stl = STL(source_stl_path)
    target_stl = STL(target_stl_path)

    r, t, yt = fit_data(
        target_data=target_stl.get_sample_points(),
        source_data=source_stl.get_sample_points(),
        check=check,
        is_print_info=check)

    R = r.T
    RT_matrix = np.array([
        [R[0][0], R[0][1], R[0][2], t[0]],
        [R[1][0], R[1][1], R[1][2], t[1]],
        [R[2][0], R[2][1], R[2][2], t[2]],
        [0, 0, 0, 1]])

    init_mesh = Mesh(path=init_mesh_path)
    init_mesh_points = init_mesh.get_sample_node_list()
    trans_mesh = rototranslate_mesh(init_mesh, RT_matrix, new_path=transformed_mesh_path)
    trans_mesh_points = trans_mesh.get_sample_node_list()
    print(trans_mesh.get_path())

    if check:
        X = target_stl.get_sample_points()

        layout = go.Layout(scene=dict(aspectmode='data'))  # equal scale step
        fig = go.Figure(layout=layout)
        #add_points2graph(fig, init_mesh_points, 'init source mesh')
        add_points2graph(fig, yt, 'transformed source from CPD')
        add_points2graph(fig, trans_mesh_points, 'transformed mesh')
        add_points2graph(fig, X, 'source')
        fig.show()

    return trans_mesh


if __name__ == '__main__':
    is_WL = True


    if is_WL:
        project_folder_init = "E:\Data_pre-defect_2021-03-19\L1"
        project_folder_end = "E:\Data_pre-defect_HRpQCT"
        sample_list = ['01_2005_L1',
                       '01_2006_L1',
                       '02_2006_L1',
                       '2a_2005_L1',
                       '2b_2005_L1',
                       '03_2006_L1',
                       '04_2006_L1',
                       '05_2006_L1',
                       '06_2006_L1',
                       '08_2006_L1',
                       '10_2006_L1']
        #               'USOD18433_L1',
         #              'USOD20307_L1']
        resolution_list = ['FOV20']
        location_list = ['VB']
        mesh_param_list = ['QH_1mm',
                           'QT_1mm',
                        'QV_1mm']

        index_patient = 0
        for patient in sample_list:
            for resolution in resolution_list:
                for location in location_list:
                    for param in mesh_param_list:
                        init_mesh_path = project_folder_init + "\\" + patient + "\\" + resolution + "\Mesh\\" + patient + "_" + resolution + "_" + location + "_" + param + ".cdb"
                        init_mesh = Mesh(path=init_mesh_path)
                        source_stl_path = project_folder_init + "\\" + patient + "\\" + r"FOV20\3DSlicer\\" + patient + "_" + "FOV20" + "_" + location + ".stl"
                        add_endplates_ns(init_mesh, source_stl_path)

                        target_stl_path = project_folder_init + "\\" + patient + "\\" + r"FOV20\3DSlicer\\" + patient + "_" + "HRpQCT" + "_" + location + ".stl"
                        mesh_end_410 = project_folder_end + "\\" + patient + "\Mesh\\" + patient + "_410mic_" + location + "_" + param + ".cdb"
                        mesh_end_738 = project_folder_end + "\\" + patient + "\Mesh\\" + patient + "_738mic_" + location + "_" + param + ".cdb"
                        trans_mesh = fit_data_and_rotate_mesh(target_stl_path=target_stl_path,
                                                 source_stl_path=source_stl_path,
                                                 init_mesh_path=init_mesh_path,
                                                 transformed_mesh_path=mesh_end_410,
                                                 check=True)
                        trans_mesh.write(new_path=mesh_end_738)

            index_patient += 1
