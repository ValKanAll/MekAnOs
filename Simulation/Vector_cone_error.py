import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import numpy as np


end_point = [0.0, 0.0, 0.0]


def rotate_error_cone(v, n=8, cone_angle=5, plot=False):
    '''

    :param v:
    :param n:
    :param cone_angle: angle in degrees
    :return:
    '''
    # normalize vector
    norm = np.linalg.norm(v)
    v /= norm
    a, b, c = v

    print('Direction_vector: ', v)

    # circle definition
    alpha_list = [2*math.pi*k/n for k in range(n)]
    cone_angle_rad = 2*math.pi*cone_angle/360
    circle_init = [np.array([math.cos(alpha)*math.sin(cone_angle_rad),
                            math.sin(alpha)*math.sin(cone_angle_rad),
                            math.cos(cone_angle_rad)]) for alpha in alpha_list]


    # first rotation around y
    cos_phi = c
    phi = math.acos(cos_phi)
    sin_phi = math.sin(phi)
    rot_y = np.array([[cos_phi, 0.0, sin_phi],
                      [0.0, 1.0, 0.0],
                      [-sin_phi, 0.0, cos_phi]])

    # second rotation around z
    if abs(c) != 1.0:
        cos_theta = a / sin_phi
        sin_theta = b / sin_phi
        rot_z = np.array([[cos_theta, -sin_theta, 0.0],
                          [sin_theta, cos_theta, 0.0],
                          [0.0, 0.0, 1.0]])
        rot_total = rot_z.dot(rot_y)

    else:
        rot_total = c*np.array([[1.0, 0.0, 0.0],
                              [0.0, 1.0, 0.0],
                              [0.0, 0.0, 1.0]])

    circle_rotated = [norm*rot_total.dot(circle_v) for circle_v in circle_init]

    if plot:
        plt.figure()
        ax = plt.subplot(111, projection='3d')
        for circle_init_v in circle_init:
            ax.plot3D([end_point[0]-circle_init_v[0], end_point[0]],
                [end_point[1]-circle_init_v[1], end_point[1]],
                [end_point[2]-circle_init_v[2], end_point[2]], color='b', linewidth=1)
        for circle_rot_v in circle_rotated:
            ax.plot3D([end_point[0] - circle_rot_v[0], end_point[0]],
                      [end_point[1] - circle_rot_v[1], end_point[1]],
                      [end_point[2] - circle_rot_v[2], end_point[2]], color='r', linewidth=1)
            #ax.quiver(0, 0, 0, circle_rot_v[0], circle_rot_v[1], circle_rot_v[2], color='r')
            #print(np.linalg.norm(circle_rot_v))

        '''ax.scatter([circle_init_v[0] for circle_init_v in circle_init],
                   [circle_init_v[1] for circle_init_v in circle_init],
                   [circle_init_v[2] for circle_init_v in circle_init], color='b')
        ax.scatter([circle_rot_v[0] for circle_rot_v in circle_rotated],
                   [circle_rot_v[1] for circle_rot_v in circle_rotated],
                   [circle_rot_v[2] for circle_rot_v in circle_rotated], color='r')'''

        set_axes_equal(ax)
        plt.show()

    return circle_rotated


def set_axes_equal(ax):
    '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().
    '''

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])


#rotate_error_cone([1, 1, 1], 20, 5)