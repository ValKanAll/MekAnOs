from module.Structure.Mesh import Mesh
from module.Reader.xml_reader import read_position_file
from module.Writer.xml_writer import write_position_file
import numpy as np
import random
import itertools
import scipy
import scipy.linalg
from Structure.STL import STL
from Geometry_modifyer.Displayer import add_points2graph
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from math import (pi, sqrt)
import math
import scipy.linalg


def sph2cart(az, el):
    '''Transform spherical coordinates to Cartesian'''
    cos_el = np.cos(el).reshape(-1, 1)
    cos_az = np.cos(az).reshape(-1, 1)
    sin_az = np.sin(az).reshape(-1, 1)
    sin_el = np.sin(el).reshape(-1, 1)
    cart = np.concatenate((cos_el * cos_az, cos_el * sin_az, sin_el), 1)
    return cart


def get_poles(path, sample=5000, distance=0.2, sample_dense_points=200):
    # Define spheric coord that represent a sphere of radius 1 and convert in cartesian coord
    N = 720
    az = np.deg2rad(np.linspace(1, 360, N))  # azimuth
    el = np.deg2rad(np.linspace(1, 360, N))  # elevation
    count_angle = np.array(list(itertools.product(az, el)))
    cart = sph2cart(count_angle[:, 0], count_angle[:, 1])
    cart = np.array(random.sample(list(cart), sample))

    # Read mesh
    stl_mesh = STL(path)

    # Get normal vectors of facets and normalize each
    print('Start normalize normal vectors...')
    vectors = np.array(random.sample(list(stl_mesh.normals), sample))  # stl_mesh.normals
    for v in vectors:
        v /= scipy.linalg.norm(np.array(v))
    print('Normalization done...')

    # For each sphere point, count the number of normal vectors inside a sphere of radius 'distance'
    spheric_count = []
    index = 0
    print('Start calculating dense zones...\n')
    for spheric_coord in cart:
        # Visual hint of advancement
        if index % (len(cart) // 100) == 0:
            print("\r" + "=" * (index // (len(cart) // 100) - 1) + "\t{}%".format(index // (len(cart) // 100) - 1),
                  end="")
        index += 1
        count = 0
        for v in vectors:
            if (spheric_coord - v).dot((spheric_coord - v).T) <= distance ** 2:
                count += 1
        spheric_count.append([count, spheric_coord])

    print("\r" + "=" * 100 + "\t{}%".format(100))

    # Get the densest zones
    sorted_spheric_count = sorted(spheric_count, key=lambda x: x[0], reverse=True)
    empty_poles = True
    while empty_poles:
        sample_spheric = sorted_spheric_count[:sample_dense_points]
        poles = np.array([x[1] for x in sample_spheric])
        print("\nDense zones calculated, sample_dense_points={}".format(sample_dense_points))

        # Sorting densest zones into 2 poles
        print("Sorting poles starting")
        k_ref = 0  # One point is chosen arbitrarily and can be changed if one pole is empty
        while empty_poles and k_ref < sample_dense_points:  # to make sure sorting poles doesn't get empty
            print('k_ref:', k_ref)
            pole_1 = []
            pole_2 = []
            for pole in poles:
                dist = (pole - poles[k_ref]).dot((pole - poles[k_ref]).T)
                if dist <= 2 * distance ** 2:
                    pole_1.append(pole)
                elif dist >= 4 - 2 * distance ** 2:
                    pole_2.append(pole)

            if len(pole_1) * len(pole_2) == 0:
                k_ref += 1
            else:
                empty_poles = False
        sample_dense_points += 50

    pole_1 = np.array(pole_1)
    pole_2 = np.array(pole_2)
    print("Poles sorted")

    return vectors, cart, poles, pole_1, pole_2


def get_threshold_from_points(points, origin, x_axis, y_axis, z_axis, endplate_height=3):
    # Get projections on direction
    proj = []
    mean_mesh = origin
    for point in points:
        rel_P = np.array(point) - mean_mesh
        n_P = scipy.linalg.norm(rel_P)
        cos_proj = rel_P.dot(z_axis.T)
        sin_proj = scipy.linalg.norm(np.cross(rel_P, z_axis))
        theta = np.sign(np.dot(y_axis, rel_P)) * np.arccos(np.dot(x_axis, rel_P.T) / n_P)

        proj.append(cos_proj)

    # Hist approximation of cos projection
    hist_y, hist_x = np.histogram(proj, bins=len(points) // 1000)
    x = []
    for i in range(len(hist_x) - 1):
        x.append((hist_x[i] + hist_x[i + 1]) / 2)
    x = np.array(x)
    poly = np.polyfit(x, hist_y, 10)

    # Get peaks by dividing hist in 2 parts and getting their max (best for flat surface)
    hist_y_1, hist_y_2 = hist_y[:len(hist_y) // 2], hist_y[len(hist_y) // 2:]
    x_1, x_2 = x[:len(hist_y) // 2], x[len(hist_y) // 2:]
    peak11, peak21 = x_1[list(hist_y_1).index(max(hist_y_1))], x_2[list(hist_y_2).index(max(hist_y_2))]

    # Get peaks from polynom via first derivation (best for irregular surface)
    peaks = np.polyder(np.poly1d(poly), 1).r
    peaks_real = [np.real(r) for r in peaks if np.imag(r) == 0.0]  # Get only real roots
    peaks_real.sort()
    up_peaks_list = []
    for peak in peaks_real:
        if np.polyder(np.poly1d(poly), 2)(peak) < 0:
            up_peaks_list.append(peak)
    peak12, peak22 = up_peaks_list[0], up_peaks_list[-1]

    # Average of both methods
    peak1 = (peak11 + peak12) / 2
    peak2 = (peak21 + peak22) / 2

    # Define threshold for endplates as roots of polynom derived twice (change of convexity)
    racines = np.polyder(np.poly1d(poly), 2).r
    racines_real = [np.real(r) for r in racines if np.imag(r) == 0.0]  # Get only real roots
    racines_real.sort()

    for i in range(len(racines_real)):
        if racines_real[i] >= peak1:
            thresh1 = min(peak1 + endplate_height,
                          racines_real[i] + endplate_height)
            break
    for j in range(len(racines_real)):
        if racines_real[-j - 1] <= peak2:
            thresh2 = max(peak2 - endplate_height,
                          racines_real[-j - 1] - endplate_height)
            break

    return thresh1, thresh2, x, hist_y, poly, peak1, peak2, peak11, peak21, peak12, peak22


def get_endplates_from_thresholds(points, origin, direction, thresh1, thresh2):
    endplate_1 = []
    endplate_2 = []
    points_without_endplates = []
    mean_mesh = origin
    while len(endplate_1) == 0 or len(endplate_2) == 0:
        for point in points:
            rel_P = np.array(point) - mean_mesh
            cos_proj = rel_P.dot(direction.T)
            if cos_proj >= thresh2:
                endplate_2.append(point)
            elif cos_proj <= thresh1:
                endplate_1.append(point)
            else:
                points_without_endplates.append(point)
        if len(endplate_1) == 0:
            thresh1 += 2
        if len(endplate_2) == 0:
            thresh2 -= 2

    endplate_1 = np.array(endplate_1)
    endplate_2 = np.array(endplate_2)
    points_without_endplates = np.array(points_without_endplates)

    return endplate_1, endplate_2, points_without_endplates


def detect_endplates2(path, sample=3000, distance=0.1, sample_dense_points=200, plot=1, order_polyfit=10, title=''):
    empty_endplates = True
    nb_try = 0
    while nb_try < 10 and empty_endplates:
        # Define spheric coord that represent a sphere of radius 1 and convert in cartesian coord
        N = 720
        az = np.deg2rad(np.linspace(1, 360, N))  # azimuth
        el = np.deg2rad(np.linspace(1, 360, N))  # elevation
        count_angle = np.array(list(itertools.product(az, el)))
        cart = sph2cart(count_angle[:, 0], count_angle[:, 1])
        cart = np.array(random.sample(list(cart), sample))

        # Read mesh
        stl_mesh = STL(path)

        # Get normal vectors of facets and normalize each
        print('Start normalize normal vectors...')
        vectors = np.array(random.sample(list(stl_mesh.normals), sample * 2))  # stl_mesh.normals
        for v in vectors:
            v /= scipy.linalg.norm(np.array(v))
        print('Normalization done...')

        # For each sphere point, count the number of normal vectors inside a sphere of radius 'distance'
        spheric_count = []
        index = 0
        print('Start calculating dense zones...\n')
        for spheric_coord in cart:
            # Visual hint of advancement
            if index % (len(cart) // 100) == 0:
                print("\r" + "=" * (index // (len(cart) // 100) - 1) + "\t{}%".format(index // (len(cart) // 100) - 1),
                      end="")
            index += 1
            count = 0
            for v in vectors:
                if (spheric_coord - v).dot((spheric_coord - v).T) <= distance ** 2:
                    count += 1
            spheric_count.append([count, spheric_coord])

        print("\r" + "=" * 100 + "\t{}%".format(100))

        # Get the densest zones
        sample_spheric = sorted(spheric_count, key=lambda x: x[0], reverse=True)[:sample_dense_points]
        poles = np.array([x[1] for x in sample_spheric])
        print("\nDense zones calculated")

        # Sorting densest zones into 2 poles
        print("Sorting poles starting")
        empty_poles = True
        k_ref = 0  # One point is chosen arbitrarily and can be changed if one pole is empty
        while empty_poles:  # to make sure sorting poles doesn't get empty
            print('k_ref:', k_ref)
            pole_1 = []
            pole_2 = []
            for pole in poles:
                dist = (pole - poles[k_ref]).dot((pole - poles[k_ref]).T)
                if dist <= 2 * distance ** 2:
                    pole_1.append(pole)
                elif dist >= 4 - 2 * distance ** 2:
                    pole_2.append(pole)

            if len(pole_1) * len(pole_2) == 0:
                k_ref += 1
            else:
                empty_poles = False

        pole_1 = np.array(pole_1)
        pole_2 = np.array(pole_2)
        print("Poles sorted")

        # Average poles in one point
        P_1 = np.array([pole_1[:, 0].mean(), pole_1[:, 1].mean(), pole_1[:, 2].mean()])
        P_2 = np.array([pole_2[:, 0].mean(), pole_2[:, 1].mean(), pole_2[:, 2].mean()])
        direction = (P_1 - P_2) / scipy.linalg.norm(np.array(P_1 - P_2))
        direction1 = P_1 / scipy.linalg.norm(np.array(P_1))
        direction2 = P_2 / scipy.linalg.norm(np.array(P_2))

        print("\tpole_1", P_1)
        print("\tpole_2", P_2)
        print("\tDirection", direction)

        # Get mesh points, mean coord and size
        points = stl_mesh.get_sample_points(sample)
        mean_mesh = np.array([points[:, 0].mean(), points[:, 1].mean(), points[:, 2].mean()])
        size_mesh = max(points[:, 0].max() - points[:, 0].min(),
                        points[:, 1].max() - points[:, 1].min(),
                        points[:, 2].max() - points[:, 2].min())

        # Get projections on direction
        proj = []
        proj_3D = []
        endplate_1 = []
        endplate_2 = []

        # Define temporary X and Y axis
        temp_xaxis = np.cross(np.array([1, 0, 0]), direction)
        temp_xaxis /= np.linalg.norm(temp_xaxis)
        temp_yaxis = np.cross(direction, temp_xaxis)

        for point in points:
            rel_P = np.array(point) - mean_mesh
            n_P = scipy.linalg.norm(rel_P)
            cos_proj = rel_P.dot(direction.T)
            sin_proj = scipy.linalg.norm(np.cross(rel_P, direction))
            theta = np.sign(np.dot(temp_yaxis, rel_P)) * np.arccos(np.dot(temp_xaxis, rel_P.T) / n_P)

            proj.append(cos_proj)


        # Hist approximation of cos projection
        hist_y, hist_x = np.histogram(proj, bins=1000)
        x = []
        for i in range(len(hist_x) - 1):
            x.append((hist_x[i] + hist_x[i + 1]) / 2)
        x = np.array(x)
        min_x, max_x = min(x), max(x)
        #x, y = filter(x, hist_y)
        poly = np.polyfit(x, hist_y, order_polyfit)

        '''# Get peaks from polynom via first derivation
        peaks = np.polyder(np.poly1d(poly), 1).r
        peaks_real = [np.real(r) for r in peaks if np.imag(r) == 0.0]  # Get only real roots
        peaks_real.sort()
        up_peaks_list = []
        for peak in peaks_real:
            if np.polyder(np.poly1d(poly), 2)(peak) < 0:
                up_peaks_list.append(peak)
        peak1, peak2 = up_peaks_list[0], up_peaks_list[-1]'''
        first_half = []
        second_half = []
        for i in range(len(x)):
            if x[i] <= (max_x+min_x)/2:
                first_half.append(hist_y[i])
            else:
                second_half.append(hist_y[i])
        peak1, peak2 = x[first_half.index(max(first_half))], x[len(first_half) + second_half.index(max(second_half))]
        print(min_x, max_x)
        print(first_half)
        print(second_half)
        # Define threshold for endplates as roots of polynom derived twice (change of convexity)
        racines = np.polyder(np.poly1d(poly), 2).r
        racines_real = [np.real(r) for r in racines if np.imag(r) == 0.0]  # Get only real roots
        racines_real.sort()

        print('Peak1 :', peak1)
        print('Peak2 :', peak2)

        for i in range(len(racines_real)):
            if racines_real[i] >= peak1:
                thresh1 = min(racines_real[i] + 1, peak1 + 10)
                break
        for j in range(len(racines_real)):
            if racines_real[-j - 1] <= peak2:
                thresh2 = max(racines_real[-j - 1] - 1, peak2 - 10)
                break

        print('Thresh1 :', thresh1)
        print('Thresh2 :', thresh2)

        # Get points of mesh that correspond to endplates
        for point in points:
            rel_P = np.array(point) - mean_mesh
            cos_proj = rel_P.dot(direction.T)
            if cos_proj >= thresh2:
                endplate_1.append(point)
            elif cos_proj <= thresh1:
                endplate_2.append(point)

        if len(endplate_1) * len(endplate_2) > 100:
            empty_endplates = False
        else:
            sample += 1000
            nb_try += 1

    if nb_try == 5:
        return ValueError

    endplate_1 = np.array(endplate_1)
    endplate_2 = np.array(endplate_2)

    # Fitting planes
    #fit1 = plane_from_points(endplate_1)
    #fit2 = plane_from_points(endplate_2)

    # plot raw data
    '''plt.figure()
    ax = plt.subplot(111, projection='3d')
    ax.scatter(endplate_1[:, 0],
               endplate_1[:, 1],
               endplate_1[:, 2], color='b')
    ax.scatter(endplate_2[:, 0],
               endplate_2[:, 1],
               endplate_2[:, 2], color='r')

    # plot plane
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    X, Y = np.meshgrid(np.arange(xlim[0], xlim[1], step=5),
                       np.arange(ylim[0], ylim[1], step=5))

    Z1 = np.zeros(X.shape)
    for r in range(X.shape[0]):
        for c in range(X.shape[1]):
            Z1[r, c] = fit1[0] * X[r, c] + fit1[1] * Y[r, c] + fit1[2]

    Z2 = np.zeros(X.shape)
    for r in range(X.shape[0]):
        for c in range(X.shape[1]):
            Z2[r, c] = fit2[0] * X[r, c] + fit2[1] * Y[r, c] + fit2[2]

    ax.plot_wireframe(X, Y, Z1, color='k')
    ax.plot_wireframe(X, Y, Z2, color='k')

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    #plt.show()'''

    if plot == 2:
        # Define figure
        fig = make_subplots(rows=3, cols=3, specs=[[{"type": "scene"}, {"type": "scene"}, {"type": "scene"}],
                                                   [{"type": "xy"}, {"rowspan": 2, "colspan": 2, "type": "scene"},
                                                    {}],
                                                   [{"type": "scene"}, {},
                                                    {}]])
        fig.update_layout(title_text=title)

        # (1, 1) : Sphere sampling, normal vectors and dense zones
        add_points2graph(fig, vectors, 'normal vectors', 1, 1, 1)
        add_points2graph(fig, cart, 'spheric coord', 2, 1, 1)
        add_points2graph(fig, poles, 'max_densities', 5, 1, 1)

        # (1, 2) : Normal vectors, poles and directions
        add_points2graph(fig, vectors, 'normal vectors', 1, 1, 2)
        add_points2graph(fig, pole_1, 'pole_1', 5, 1, 2)
        add_points2graph(fig, pole_2, 'pole_2', 5, 1, 2)
        fig.add_trace(go.Scatter3d(x=[P_1[0], P_2[0]], y=[P_1[1], P_2[1]], z=[P_1[2], P_2[2]],
                                   mode='lines', name="Pole line",
                                   line=dict(
                                       color='orange',
                                       width=5
                                   )), row=1, col=2)
        fig.add_trace(go.Scatter3d(x=[0, direction[0]], y=[0, direction[1]], z=[0, direction[2]],
                                   mode='lines', name="direction line",
                                   line=dict(
                                       color='red',
                                       width=5
                                   )), row=1, col=2)
        fig.add_trace(go.Scatter3d(x=[0, direction1[0]], y=[0, direction1[1]], z=[0, direction1[2]],
                                   mode='lines', name="direction 1",
                                   line=dict(
                                       color='black',
                                       width=5
                                   )), row=1, col=2)
        fig.add_trace(go.Scatter3d(x=[0, direction2[0]], y=[0, direction2[1]], z=[0, direction2[2]],
                                   mode='lines', name="direction 2",
                                   line=dict(
                                       color='black',
                                       width=5
                                   )), row=1, col=2)

        # (1, 3) : Plot directions on mesh
        add_points2graph(fig, points, 'Mesh', 1, 1, 3)
        fig.add_trace(go.Scatter3d(x=[mean_mesh[0], mean_mesh[0] + size_mesh / 2 * direction1[0]],
                                   y=[mean_mesh[1], mean_mesh[1] + size_mesh / 2 * direction1[1]],
                                   z=[mean_mesh[2], mean_mesh[2] + size_mesh / 2 * direction1[2]],
                                   mode='lines',
                                   name="direction line 1",
                                   line=dict(
                                       color='red',
                                       width=10
                                   )), 1, 3)
        fig.add_trace(go.Scatter3d(x=[mean_mesh[0], mean_mesh[0] + size_mesh / 2 * direction2[0]],
                                   y=[mean_mesh[1], mean_mesh[1] + size_mesh / 2 * direction2[1]],
                                   z=[mean_mesh[2], mean_mesh[2] + size_mesh / 2 * direction2[2]],
                                   mode='lines',
                                   name="direction line 2",
                                   line=dict(
                                       color='green',
                                       width=10
                                   )), 1, 3)

        fig.add_trace(
            go.Scatter3d(
                x=[mean_mesh[0] - size_mesh / 2 * direction2[0], mean_mesh[0] + size_mesh / 2 * direction2[0]],
                y=[mean_mesh[1] - size_mesh / 2 * direction2[1], mean_mesh[1] + size_mesh / 2 * direction2[1]],
                z=[mean_mesh[2] - size_mesh / 2 * direction2[2], mean_mesh[2] + size_mesh / 2 * direction2[2]],
                mode='lines',
                name="direction line",
                line=dict(
                    color='black',
                    width=5
                )), 1, 3)

        # (3, 1) : Plot projections depending on theta

        # (2, 1) : Hist approximation plot
        xp = np.linspace(min(x), max(x), 1000)
        fig.add_trace(go.Scatter(x=x, y=hist_y, name='hist'), row=2, col=1)
        fig.add_trace(go.Scatter(x=xp, y=np.poly1d(poly)(xp), name='P'), row=2, col=1)
        fig.add_trace(go.Scatter(x=xp, y=np.polyder(np.poly1d(poly), 2)(xp), name='P"'), row=2, col=1)
        fig.add_trace(go.Scatter(x=[thresh1, thresh1], y=[0, max(hist_y)], name='threshold 1'), row=2, col=1)
        fig.add_trace(go.Scatter(x=[thresh2, thresh2], y=[0, max(hist_y)], name='threshold 2'), row=2, col=1)

        # (2, 2) : Final result
        add_points2graph(fig, points, 'Mesh', 1, 2, 2)
        try:
            add_points2graph(fig, endplate_1, 'Endplate 1', 3, 2, 2)
            add_points2graph(fig, endplate_2, 'Endplate 2', 3, 2, 2)
        except IndexError:
            print('Endplate_1: ', endplate_1)
            print('Endplate_2: ', endplate_2)

        fig.show()

    elif plot == 1:
        # Define figure
        fig = make_subplots(rows=1, cols=1, specs=[[{"type": "scene"}]])
        fig.update_layout(title_text=title)
        add_points2graph(fig, points, 'Mesh', 1)
        try:
            add_points2graph(fig, endplate_1, 'Endplate 1', 3)
            add_points2graph(fig, endplate_2, 'Endplate 2', 3)
        except IndexError:
            print('Endplate_1: ', endplate_1)
            print('Endplate_2: ', endplate_2)
        fig.show()

    return direction, thresh1, thresh2


def plane_from_points2(points):
    # Plane defined by z = a*x + b*y + c
    # z = [x, y, 1].T * [a, b, c]
    # normal = [a, b, c]
    A = np.array([
        points[:, 0],
        points[:, 1],
        np.ones(points.shape[0])
    ]).T
    B = np.array([points[:, 2]]).T

    # Analytic solution
    # normal = (A.T * A)^-1 * A.T * B
    normal = np.dot(np.dot(np.linalg.inv(np.dot(A.T, A)), A.T), B)
    n = normal / np.linalg.norm(normal)
    # errors = B - np.dot(A, normal)
    # residual = np.linalg.norm(errors)

    V = points - np.dot(A, normal)
    dist_array = np.dot(V, n)
    proj_points = points - np.dot(dist_array, n.T)
    origin = np.array([proj_points[:, 0].mean(),
                       proj_points[:, 1].mean(),
                       proj_points[:, 2].mean()])
    print("ORIGIN : ", origin)
    print("n vector : ", n)
    x = np.array([[1, 0, 0]]).T - np.dot(n.T, np.array([[1, 0, 0]]).T) * n
    x /= np.linalg.norm(x)
    print("x vector : ", x)
    y = np.cross(n.T, x.T).T
    y /= np.linalg.norm(y)
    print("y vector : ", y)
    z = np.cross(x.T, y.T).T
    z /= np.linalg.norm(z)
    print("z vector : ", z)

    X = np.zeros(points.shape[0])
    Y = np.zeros(points.shape[0])
    Z = np.zeros(points.shape[0])
    T = np.zeros(points.shape[0])
    R = np.zeros(points.shape[0])

    # Define value to re-sample polar coordinates
    k = 50
    R_T_sampled = np.empty(k, dtype=object)
    for i in range(k):
        R_T_sampled[i] = []
    index = 0
    for point in points:
        v = np.array(point) - origin
        dist_z = np.dot(v, n)[0]
        dist_x = np.dot(v, x)[0]
        dist_y = np.dot(v, y)[0]
        theta = math.atan2(dist_y, dist_x)  # in radians
        r = sqrt(dist_x**2 + dist_y**2)

        X[index] = dist_x
        Y[index] = dist_y
        Z[index] = dist_z
        T[index] = theta
        R[index] = r

        R_T_sampled[math.floor(theta/(2*pi)*k)].append(r)

        index += 1
    R_max = []
    T_max = []
    X_max = []
    Y_max = []
    X_lim = []
    Y_lim = []
    lim = 0.9
    for i in range(k):
        try:
            R_max.append(max(R_T_sampled[i]))
            T_max.append(2*pi*i/k)
            X_max.append(max(R_T_sampled[i]) * math.cos(2 * pi * i / k))
            Y_max.append(max(R_T_sampled[i]) * math.sin(2 * pi * i / k))
            X_lim.append(lim*max(R_T_sampled[i]) * math.cos(2 * pi * i / k))
            Y_lim.append(lim*max(R_T_sampled[i]) * math.sin(2 * pi * i / k))
        except ValueError:
            pass


    plt.figure()
    plt.scatter(X, Y, label='projected_endplate')
    plt.scatter(X_max, Y_max, label='contour')
    plt.scatter(X_lim, Y_lim, label='contour limit')
    plt.scatter([0], [0], label='center')
    #plt.hist(dist_array, bins=100, label="dist_array")
    #plt.hist(D, bins=100, label="D")
    plt.legend()
    plt.show()

    return normal


def detect_endplate(path, sample=5000, distance=0.2, plot=1, endplate_height=3,
                    return_points=True, is_write_position_file=True):

    # get poles from normal vectors
    vectors, cart, poles, pole_1, pole_2 = get_poles(path, sample, distance)

    # Average poles in one point
    P_1 = np.array([pole_1[:, 0].mean(), pole_1[:, 1].mean(), pole_1[:, 2].mean()])
    P_2 = np.array([pole_2[:, 0].mean(), pole_2[:, 1].mean(), pole_2[:, 2].mean()])
    direction = (P_1 - P_2) / scipy.linalg.norm(np.array(P_1 - P_2))
    direction1 = P_1 / scipy.linalg.norm(np.array(P_1))
    direction2 = P_2 / scipy.linalg.norm(np.array(P_2))

    print("\tpole_1", P_1)
    print("\tpole_2", P_2)
    print("\tDirection", direction)

    # Define temporary X and Y axis
    temp_xaxis = np.cross(np.array([1, 0, 0]), direction)
    temp_xaxis /= np.linalg.norm(temp_xaxis)
    temp_yaxis = np.cross(direction, temp_xaxis)

    stl_mesh = STL(path)
    # Get mesh points, mean coord and size
    points = stl_mesh.get_sample_points(sample*5)
    mean_mesh = np.array([points[:, 0].mean(), points[:, 1].mean(), points[:, 2].mean()])
    size_mesh = max(points[:, 0].max() - points[:, 0].min(),
                    points[:, 1].max() - points[:, 1].min(),
                    points[:, 2].max() - points[:, 2].min())

    # get threshold values for endplates
    thresh1, thresh2, \
    x, hist_y, poly, \
    peak1, peak2, peak11, peak21, peak12, peak22 = get_threshold_from_points(points, mean_mesh, temp_xaxis, temp_yaxis, direction, endplate_height)

    # Get points of mesh that correspond to endplates
    endplate_1, endplate_2, _ = get_endplates_from_thresholds(points, mean_mesh, direction, thresh1, thresh2)

    # Fitting planes
    fit1, X1, Y1, Z_1, surface_1, max_dist_1 = plane_from_points(endplate_1)
    fit2, X2, Y2, Z_2, surface_2, max_dist_2 = plane_from_points(endplate_2)


    # Create planes
    k_plane = 10
    X, Y = np.meshgrid(np.arange(mean_mesh[0]-size_mesh/2, mean_mesh[0]+size_mesh/2, k_plane),
                       np.arange(mean_mesh[1]-size_mesh/2, mean_mesh[1]+size_mesh/2, k_plane))
    plane_1 = np.zeros(X.shape)
    plane_2 = np.zeros(X.shape)
    for r in range(X.shape[0]):
        for c in range(X.shape[1]):
            plane_1[r, c] = fit1[0] * X[r, c] + fit1[1] * Y[r, c] + fit1[2]
            plane_2[r, c] = fit2[0] * X[r, c] + fit2[1] * Y[r, c] + fit2[2]

    print('surface_1: ', surface_1)
    print('surface_2: ', surface_2)

    X1, X2 = np.array(X1), np.array(X2)
    Y1, Y2 = np.array(Y1), np.array(Y2)
    Z_vector = (np.array(Z_1) + np.array(Z_2)) / 2

    if surface_2 > surface_1 and max_dist_2 > max_dist_1:
        endplate_top, endplate_bottom = endplate_2, endplate_1
        Z_vector = -Z_vector
        Y_vector = -Y2
        X_vector = X2
        thresh1, thresh2 = -thresh2, -thresh1
    else:
        endplate_top, endplate_bottom = endplate_1, endplate_2
        Y_vector = Y1
        X_vector = X1

    # get threshold values for endplates
    thresh1b, thresh2b, \
    xb, hist_yb, polyb, \
    peak1b, peak2b, peak11b, peak21b, peak12b, peak22b = get_threshold_from_points(points, mean_mesh, X_vector, Y_vector,
                                                                             Z_vector, endplate_height)

    # Get points of mesh that correspond to endplates
    endplate_empty = True
    while endplate_empty:
        endplate_1b, endplate_2b, vertebra_without_endplates = get_endplates_from_thresholds(points, mean_mesh, Z_vector, thresh1b, thresh2b)
        if len(endplate_1b)*len(endplate_2b) != 0:
            endplate_empty = False
        else:
            if len(endplate_1b) == 0:
                thresh1b += 2
            else:
                thresh2b -= 2
        print('new thresh: ', thresh2b, thresh1b)

    if plot == 2:
        # Define figure
        fig = make_subplots(rows=3, cols=3, specs=[[{"type": "scene"}, {"type": "scene"}, {"type": "scene"}],
                                                   [{"type": "xy"}, {"rowspan": 2, "colspan": 2, "type": "scene"}, {}],
                                                   [{"type": "scene"}, {},
                                                    {}]])

        # (1, 1) : Sphere sampling, normal vectors and dense zones
        add_points2graph(fig, vectors, 'normal vectors', 1, 1, 1)
        add_points2graph(fig, cart, 'spheric coord', 2, 1, 1)
        add_points2graph(fig, poles, 'max_densities', 5, 1, 1)

        # (1, 2) : Normal vectors, poles and directions
        add_points2graph(fig, vectors, 'normal vectors', 1, 1, 2)
        add_points2graph(fig, pole_1, 'pole_1', 5, 1, 2)
        add_points2graph(fig, pole_2, 'pole_2', 5, 1, 2)
        fig.add_trace(go.Scatter3d(x=[P_1[0], P_2[0]], y=[P_1[1], P_2[1]], z=[P_1[2], P_2[2]],
                                   mode='lines', name="Pole line",
                                   line=dict(
                                          color='orange',
                                          width=5
                                      )), row=1, col=2)
        fig.add_trace(go.Scatter3d(x=[0, direction[0]], y=[0, direction[1]], z=[0, direction[2]],
                                   mode='lines', name="direction line",
                                   line=dict(
                                       color='red',
                                       width=5
                                   )), row=1, col=2)
        fig.add_trace(go.Scatter3d(x=[0, direction1[0]], y=[0, direction1[1]], z=[0, direction1[2]],
                                   mode='lines', name="direction 1",
                                   line=dict(
                                       color='black',
                                       width=5
                                   )), row=1, col=2)
        fig.add_trace(go.Scatter3d(x=[0, direction2[0]], y=[0, direction2[1]], z=[0, direction2[2]],
                                   mode='lines', name="direction 2",
                                   line=dict(
                                       color='black',
                                       width=5
                                   )), row=1, col=2)

        # (1, 3) : Plot directions on mesh
        add_points2graph(fig, points, 'Mesh', 1, 1, 3)
        fig.add_trace(go.Scatter3d(x=[mean_mesh[0], mean_mesh[0] + size_mesh / 2 * direction1[0]],
                                   y=[mean_mesh[1], mean_mesh[1] + size_mesh / 2 * direction1[1]],
                                   z=[mean_mesh[2], mean_mesh[2] + size_mesh / 2 * direction1[2]],
                                   mode='lines',
                                   name="direction line 1",
                                   line=dict(
                                       color='red',
                                       width=10
                                   )), 1, 3)
        fig.add_trace(go.Scatter3d(x=[mean_mesh[0], mean_mesh[0] + size_mesh / 2 * direction2[0]],
                                   y=[mean_mesh[1], mean_mesh[1] + size_mesh / 2 * direction2[1]],
                                   z=[mean_mesh[2], mean_mesh[2] + size_mesh / 2 * direction2[2]],
                                   mode='lines',
                                   name="direction line 2",
                                   line=dict(
                                       color='green',
                                       width=10
                                   )), 1, 3)

        fig.add_trace(
            go.Scatter3d(x=[mean_mesh[0] - size_mesh / 2 * direction2[0], mean_mesh[0] + size_mesh / 2 * direction2[0]],
                         y=[mean_mesh[1] - size_mesh / 2 * direction2[1], mean_mesh[1] + size_mesh / 2 * direction2[1]],
                         z=[mean_mesh[2] - size_mesh / 2 * direction2[2], mean_mesh[2] + size_mesh / 2 * direction2[2]],
                         mode='lines',
                         name="direction line",
                         line=dict(
                             color='black',
                             width=5
                         )), 1, 3)

        # (3, 1) : Plot projections depending on theta


        # (2, 1) : Hist approximation plot
        xp = np.linspace(min(x), max(x), 1000)
        fig.add_trace(go.Scatter(x=x, y=hist_y, name='hist'), row=2, col=1)
        #fig.add_trace(go.Scatter(x=x, y=y, name='hist_filtered'), row=2, col=1)
        fig.add_trace(go.Scatter(x=xp, y=np.poly1d(poly)(xp), name='P'), row=2, col=1)
        fig.add_trace(go.Scatter(x=xp, y=np.polyder(np.poly1d(poly), 2)(xp), name='P"'), row=2, col=1)
        fig.add_trace(go.Scatter(x=[thresh1, thresh1], y=[0, max(hist_y)], name='threshold 1'), row=2, col=1)
        fig.add_trace(go.Scatter(x=[thresh2, thresh2], y=[0, max(hist_y)], name='threshold 2'), row=2, col=1)
        fig.add_trace(go.Scatter(x=[peak1, peak1], y=[0, max(hist_y)], name='peak 1'), row=2, col=1)
        fig.add_trace(go.Scatter(x=[peak2, peak2], y=[0, max(hist_y)], name='peak 2'), row=2, col=1)
        fig.add_trace(go.Scatter(x=[peak11, peak11], y=[0, max(hist_y)], name='peak 11'), row=2, col=1)
        fig.add_trace(go.Scatter(x=[peak21, peak21], y=[0, max(hist_y)], name='peak 21'), row=2, col=1)
        fig.add_trace(go.Scatter(x=[peak12, peak12], y=[0, max(hist_y)], name='peak 12'), row=2, col=1)
        fig.add_trace(go.Scatter(x=[peak22, peak22], y=[0, max(hist_y)], name='peak 22'), row=2, col=1)

        # (2, 2) : Final result
        add_points2graph(fig, points, 'Mesh', 1, 2, 2)
        fig.add_trace(go.Surface(x=X, y=Y, z=plane_1, showscale=False, opacity=0.3), row=2, col=2)
        fig.add_trace(go.Surface(x=X, y=Y, z=plane_2, showscale=False, opacity=0.3), row=2, col=2)
        fig.add_trace(
            go.Scatter3d(x=[mean_mesh[0], mean_mesh[0] + size_mesh / 2 * X_vector[0]],
                         y=[mean_mesh[1], mean_mesh[1] + size_mesh / 2 * X_vector[1]],
                         z=[mean_mesh[2], mean_mesh[2] + size_mesh / 2 * X_vector[2]],
                         mode='lines',
                         name="X vector",
                         line=dict(
                             color='blue',
                             width=5
                         )), 2, 2)
        fig.add_trace(
            go.Scatter3d(x=[mean_mesh[0], mean_mesh[0] + size_mesh / 2 * Y_vector[0]],
                         y=[mean_mesh[1], mean_mesh[1] + size_mesh / 2 * Y_vector[1]],
                         z=[mean_mesh[2], mean_mesh[2] + size_mesh / 2 * Y_vector[2]],
                         mode='lines',
                         name="Y vector",
                         line=dict(
                             color='blue',
                             width=5
                         )), 2, 2)
        fig.add_trace(
            go.Scatter3d(x=[mean_mesh[0], mean_mesh[0] + size_mesh / 2 * Z_vector[0]],
                         y=[mean_mesh[1], mean_mesh[1] + size_mesh / 2 * Z_vector[1]],
                         z=[mean_mesh[2], mean_mesh[2] + size_mesh / 2 * Z_vector[2]],
                         mode='lines',
                         name="Z vector",
                         line=dict(
                             color='blue',
                             width=5
                         )), 2, 2)
        '''fig.add_trace(
            go.Scatter3d(x=[mean_mesh[0], mean_mesh[0] + size_mesh / 2 * X1[0]],
                         y=[mean_mesh[1], mean_mesh[1] + size_mesh / 2 * X1[1]],
                         z=[mean_mesh[2], mean_mesh[2] + size_mesh / 2 * X1[2]],
                         mode='lines',
                         name="X1 line",
                         line=dict(
                             color='blue',
                             width=5
                         )), 2, 2)
        fig.add_trace(
            go.Scatter3d(x=[mean_mesh[0], mean_mesh[0] + size_mesh / 2 * Y1[0]],
                         y=[mean_mesh[1], mean_mesh[1] + size_mesh / 2 * Y1[1]],
                         z=[mean_mesh[2], mean_mesh[2] + size_mesh / 2 * Y1[2]],
                         mode='lines',
                         name="Y1 line",
                         line=dict(
                             color='blue',
                             width=5
                         )), 2, 2)
        fig.add_trace(
            go.Scatter3d(x=[mean_mesh[0], mean_mesh[0] + size_mesh / 2 * Z_1[0]],
                         y=[mean_mesh[1], mean_mesh[1] + size_mesh / 2 * Z_1[1]],
                         z=[mean_mesh[2], mean_mesh[2] + size_mesh / 2 * Z_1[2]],
                         mode='lines',
                         name="Z1 line",
                         line=dict(
                             color='blue',
                             width=5
                         )), 2, 2)

        fig.add_trace(
            go.Scatter3d(x=[mean_mesh[0], mean_mesh[0] + size_mesh / 2 * X2[0]],
                         y=[mean_mesh[1], mean_mesh[1] + size_mesh / 2 * X2[1]],
                         z=[mean_mesh[2], mean_mesh[2] + size_mesh / 2 * X2[2]],
                         mode='lines',
                         name="X2 line",
                         line=dict(
                             color='red',
                             width=5
                         )), 2, 2)
        fig.add_trace(
            go.Scatter3d(x=[mean_mesh[0], mean_mesh[0] + size_mesh / 2 * Y2[0]],
                         y=[mean_mesh[1], mean_mesh[1] + size_mesh / 2 * Y2[1]],
                         z=[mean_mesh[2], mean_mesh[2] + size_mesh / 2 * Y2[2]],
                         mode='lines',
                         name="Y2 line",
                         line=dict(
                             color='red',
                             width=5
                         )), 2, 2)
        fig.add_trace(
            go.Scatter3d(x=[mean_mesh[0], mean_mesh[0] + size_mesh / 2 * Z_2[0]],
                         y=[mean_mesh[1], mean_mesh[1] + size_mesh / 2 * Z_2[1]],
                         z=[mean_mesh[2], mean_mesh[2] + size_mesh / 2 * Z_2[2]],
                         mode='lines',
                         name="Z2 line",
                         line=dict(
                             color='red',
                             width=5
                         )), 2, 2)'''

        try:
            add_points2graph(fig, endplate_top, 'Endplate TOP', 3, 2, 2)
            add_points2graph(fig, endplate_bottom, 'Endplate BOTTOM', 3, 2, 2)

            add_points2graph(fig, endplate_1b, 'Endplate BOTTOM B', 3, 2, 2)
            add_points2graph(fig, endplate_2b, 'Endplate TOP B', 3, 2, 2)
        except IndexError:
            print('Endplate_1: ', endplate_1)
            print('Endplate_2: ', endplate_2)

        fig.show()

    elif plot == 1:
        # Define figure
        fig = make_subplots(rows=1, cols=1, specs=[[{"type": "scene"}]])
        fig.update_layout(title={'text': path})
        add_points2graph(fig, points, 'Mesh', 1)
        fig.add_trace(go.Surface(x=X, y=Y, z=plane_1, showscale=False, opacity=0.3), row=1, col=1)
        fig.add_trace(go.Surface(x=X, y=Y, z=plane_2, showscale=False, opacity=0.3), row=1, col=1)
        fig.add_trace(
            go.Scatter3d(x=[mean_mesh[0], mean_mesh[0] + size_mesh / 2 * X_vector[0]],
                         y=[mean_mesh[1], mean_mesh[1] + size_mesh / 2 * X_vector[1]],
                         z=[mean_mesh[2], mean_mesh[2] + size_mesh / 2 * X_vector[2]],
                         mode='lines',
                         name="X vector",
                         line=dict(
                             color='blue',
                             width=5
                         )), 1, 1)
        fig.add_trace(
            go.Scatter3d(x=[mean_mesh[0], mean_mesh[0] + size_mesh / 2 * Y_vector[0]],
                         y=[mean_mesh[1], mean_mesh[1] + size_mesh / 2 * Y_vector[1]],
                         z=[mean_mesh[2], mean_mesh[2] + size_mesh / 2 * Y_vector[2]],
                         mode='lines',
                         name="Y vector",
                         line=dict(
                             color='blue',
                             width=5
                         )), 1, 1)
        fig.add_trace(
            go.Scatter3d(x=[mean_mesh[0], mean_mesh[0] + size_mesh / 2 * Z_vector[0]],
                         y=[mean_mesh[1], mean_mesh[1] + size_mesh / 2 * Z_vector[1]],
                         z=[mean_mesh[2], mean_mesh[2] + size_mesh / 2 * Z_vector[2]],
                         mode='lines',
                         name="Z vector",
                         line=dict(
                             color='blue',
                             width=5
                         )), 1, 1)
        try:
            add_points2graph(fig, endplate_top, 'Endplate TOP', 3)
            add_points2graph(fig, endplate_bottom, 'Endplate BOTTOM', 3)
            add_points2graph(fig, endplate_1b, 'Endplate BOTTOM B', 3)
            add_points2graph(fig, endplate_2b, 'Endplate TOP B', 3)
        except IndexError:
            print('Endplate_1: ', endplate_1)
            print('Endplate_2: ', endplate_2)

        fig.show()

    if is_write_position_file:
        print('Write position file')
        stl_name = path.split('/')[-1].replace('.stl', '')
        print('stl_name', stl_name)
        pstf_path = path.replace(".stl", ".pstf")
        # Format results into dict
        prop_dict = get_prop_dict_vertebrae(thresh1b, thresh2b, X_vector, Y_vector, Z_vector, mean_mesh)
        # Write position file
        write_position_file(pstf_path, path, prop_dict)

    if return_points:
        return points, endplate_1b, endplate_2b, vertebra_without_endplates

    else:
        return thresh1b, thresh2b, X_vector, Y_vector, Z_vector, mean_mesh


def plane_from_points(points, show=False):
    # Plane defined by z = a*x + b*y + c
    # z = [x, y, 1].T * [a, b, c]
    # normal = [a, b, c]
    A = np.array([
        points[:, 0],
        points[:, 1],
        np.ones(points.shape[0])
    ]).T
    B = np.array([points[:, 2]]).T
    # Equation : A.
    # Analytic solution
    # normal = (A.T * A)^-1 * A.T * B
    fit = np.dot(np.dot(np.linalg.inv(np.dot(A.T, A)), A.T), B)
    normal = np.array([fit[0], fit[1], [-1]])
    n = normal / np.linalg.norm(normal)
    print('normal: ', normal)
    # n = normal / np.linalg.norm(normal)
    # errors = B - np.dot(A, normal)
    # residual = np.linalg.norm(errors)
    # Plane points = np.dot(A,normal)

    V = points - np.dot(A, fit)  # Vectors of distance point to plane
    dist_array = np.dot(V, n)
    proj_points = points - np.dot(dist_array, n.T)
    origin = np.array([proj_points[:, 0].mean(),
                       proj_points[:, 1].mean(),
                       proj_points[:, 2].mean()])
    print("ORIGIN : ", origin)
    print("n vector : ", n)
    x = np.array([[1, 0, 0]]).T - np.dot(n.T, np.array([[1, 0, 0]]).T) * n
    x /= np.linalg.norm(x)
    print("x vector : ", x)
    y = np.cross(n.T, x.T).T
    y /= np.linalg.norm(y)
    print("y vector : ", y)
    z = np.cross(x.T, y.T).T
    z /= np.linalg.norm(z)
    print("z vector : ", z)

    X = np.zeros(points.shape[0])
    Y = np.zeros(points.shape[0])
    Z = np.zeros(points.shape[0])
    T = np.zeros(points.shape[0])
    R = np.zeros(points.shape[0])
    DZ = np.zeros(points.shape[0])

    # Define value to re-sample polar coordinates
    k = 100
    R_T_sampled = np.empty(k, dtype=object)  # Radius gathered by polar coordinates
    for i in range(k):
        R_T_sampled[i] = []
    index = 0
    for point in points:
        v = np.array(point) - origin  # point centered at plane barycentre
        dz = np.dot(np.array(point), n)[0]
        # point projection
        dist_z = np.dot(v, n)[0]
        dist_x = np.dot(v, x)[0]
        dist_y = np.dot(v, y)[0]
        theta = math.atan2(dist_y, dist_x)  # angle between v and x in radians
        r = sqrt(dist_x**2 + dist_y**2)  # distance to plane origin

        X[index] = dist_x
        Y[index] = dist_y
        Z[index] = dist_z
        T[index] = theta
        R[index] = r
        DZ[index] = dz

        R_T_sampled[math.floor(theta/(2*pi)*k)].append(r)

        index += 1
    R_max = []  # max radius = contour of projected points
    T_max = []  # angle (because some angle value can be empty of points)
    X_max = []
    Y_max = []
    X_lim = []
    Y_lim = []
    DZ_lim = []
    lim = 0.8
    surface = 0  # Define surface of projected endplate
    for i in range(k):
        try:
            R_max.append(max(R_T_sampled[i]))
            T_max.append(2*pi*i/k)
            X_max.append(max(R_T_sampled[i]) * math.cos(2 * pi * i / k))
            Y_max.append(max(R_T_sampled[i]) * math.sin(2 * pi * i / k))
            X_lim.append(lim*max(R_T_sampled[i]) * math.cos(2 * pi * i / k))
            Y_lim.append(lim*max(R_T_sampled[i]) * math.sin(2 * pi * i / k))
        except ValueError:
            pass

    # compute surface
    for i in range(len(T_max)-1):
        surface += (T_max[i+1]-T_max[i]) * (R_max[i] + R_max[i+1])/2

    # Radius is supposed to be a even function, let's find it's symmetry axis
    even_function_error = np.zeros(len(T_max))
    T_max_oriented = np.zeros(len(T_max))
    for i in range(len(T_max)):
        for j in range(len(T_max)):
            even_function_error[i] += (R_max[(j+i) % len(T_max)] - R_max[(i-j) % len(T_max)]) ** 2
        even_function_error[i] /= len(T_max)

    # Approximate error by a polynom andd get 2 minima
    poly = np.polyfit(T_max, even_function_error, 14)

    # Get peaks from polynom via first derivation
    peaks = np.polyder(np.poly1d(poly), 1).r
    peaks_real = [np.real(r) for r in peaks if np.imag(r) == 0.0]  # Get only real roots
    peaks_real.sort()
    down_peaks_list = []
    for peak in peaks_real:
        if np.polyder(np.poly1d(poly), 2)(peak) > 0 and min(T_max) <= peak <= max(T_max):  # get only minimum peaks
            down_peaks_list.append(peak)

    print('down_peak_list', down_peaks_list)
    down_peaks_list_R_max = []
    for down_peak in down_peaks_list:
        for i in range(len(T_max)-1):
            if T_max[i] <= down_peak <= T_max[i+1]:
                down_peaks_list_R_max.append((R_max[i] + R_max[i+1])/2)
                break
    down_peaks_2 = sorted(down_peaks_list, key=lambda p: down_peaks_list_R_max[down_peaks_list.index(p)], reverse=False)[:2]  # get two lowest min
    print('selected down peaks', down_peaks_2)

    # Posterior point is correspond to min radius
    down_peaks_2_R_max = [down_peaks_list_R_max[down_peaks_list.index(down_peak)] for down_peak in down_peaks_2]
    index_theta_Posterior = down_peaks_2_R_max.index(min(down_peaks_2_R_max))
    theta_Posterior, theta_Anterior = down_peaks_2[index_theta_Posterior], down_peaks_2[(index_theta_Posterior-1)%2]

    for i in range(len(T_max)):
        T_max_oriented[i] = (T_max[i] - theta_Anterior) % (2*pi)

    if show:
        plt.figure()
        plt.plot(T_max, np.poly1d(poly)(T_max), label='poly')
        plt.plot(T_max, even_function_error, label='error')
        plt.plot(T_max, R_max, label='radius')
        plt.plot(T_max_oriented, R_max, label='radius oriented')
        plt.legend()

    # Antero-Posterior lines
    AP_line_X = [max(R_max) * math.cos(theta_Anterior), max(R_max) * math.cos(theta_Posterior)]
    AP_line_Y = [max(R_max) * math.sin(theta_Anterior), max(R_max) * math.sin(theta_Posterior)]

    # Define new axis from antero-posterior angles (by rotation of x and y)
    x_AP = math.cos(theta_Anterior) * x + math.sin(theta_Anterior) * y
    x_AP /= np.linalg.norm(x_AP)
    y_AP = -math.sin(theta_Anterior) * x + math.cos(theta_Anterior) * y
    y_AP /= np.linalg.norm(y_AP)

    print('theta anterior: ', theta_Anterior)
    print('theta posterior: ', theta_Posterior)
    print('x_AP: ', x_AP)
    print('y_AP: ', y_AP)

    if show:
        plt.figure()
        plt.scatter(X, Y, label='projected_endplate')
        plt.scatter(X_max, Y_max, label='contour')
        plt.scatter(X_lim, Y_lim, label='contour limit')
        plt.scatter([0], [0], label='center')
        plt.plot(AP_line_X, AP_line_Y, label='Antero-Posterior line')
        plt.scatter(AP_line_X[0], AP_line_Y[0], label='Anterior')
        plt.scatter(AP_line_X[1], AP_line_Y[1], label='Posterior')
        plt.legend()
        plt.show()

    return fit, list(x_AP.T[0]), list(y_AP.T[0]), list(n.T[0]), surface, max(R_max)


def convert_array2str(array):
    res_str = ""
    for coord in array:
        res_str += str(coord) + '\t'
    return res_str[:-1]


def get_prop_dict_vertebrae(thresh1, thresh2, X_vector, Y_vector, Z_vector, mean_mesh):
    prop_dict = {"axis": {"X_vector": convert_array2str(X_vector),
                          "Y_vector": convert_array2str(Y_vector),
                          "Z_vector": convert_array2str(Z_vector)},
                 "origin": convert_array2str(mean_mesh),
                 "selections": {"TOP_ENDPLATE": {"measure": "z",
                                                 "function": "inferior or equal",
                                                 "value": thresh1},
                                "BOTTOM_ENDPLATE": {"measure": "z",
                                                    "function": "superior or equal",
                                                    "value": thresh2}}
                 }
    return prop_dict


def read_pstf_vertebra(pstf_path, plot=0, return_points=False):
    print("Reading : ", pstf_path)
    stl_path, X_vector, Y_vector, Z_vector, origin, selection_list = read_position_file(pstf_path)
    print('Mesh_path:', stl_path)
    stl_mesh = STL(stl_path)
    # Get mesh points, mean coord and size
    points = stl_mesh.get_sample_points(4000)
    size_mesh = max(points[:, 0].max() - points[:, 0].min(),
                   points[:, 1].max() - points[:, 1].min(),
                   points[:, 2].max() - points[:, 2].min())
    mean_mesh = [points[:, 0].mean(), points[:, 1].mean(), points[:, 2].mean()]
    thresh_1, thresh_2 = selection_list[0][3], selection_list[1][3]
    endplate_top, endplate_bottom, points_without_endplates = get_endplates_from_thresholds(points, origin, Z_vector, selection_list[0][3], selection_list[1][3])
    if plot == 1:
        fig = make_subplots(rows=1, cols=1, specs=[[{"type": "scene"}]])
        add_points2graph(fig, points, 'Mesh', 1)
        add_points2graph(fig, points_without_endplates, 'Cortical', 1)
        #fig.add_trace(go.Surface(x=X, y=Y, z=plane_1, showscale=False, opacity=0.3), row=1, col=1)
        #fig.add_trace(go.Surface(x=X, y=Y, z=plane_2, showscale=False, opacity=0.3), row=1, col=1)
        fig.add_trace(
            go.Scatter3d(x=[mean_mesh[0], mean_mesh[0] + size_mesh / 2 * X_vector[0]],
                         y=[mean_mesh[1], mean_mesh[1] + size_mesh / 2 * X_vector[1]],
                         z=[mean_mesh[2], mean_mesh[2] + size_mesh / 2 * X_vector[2]],
                         mode='lines',
                         name="X vector",
                         line=dict(
                             color='blue',
                             width=5
                         )), 1, 1)
        fig.add_trace(
            go.Scatter3d(x=[mean_mesh[0], mean_mesh[0] + size_mesh / 2 * Y_vector[0]],
                         y=[mean_mesh[1], mean_mesh[1] + size_mesh / 2 * Y_vector[1]],
                         z=[mean_mesh[2], mean_mesh[2] + size_mesh / 2 * Y_vector[2]],
                         mode='lines',
                         name="Y vector",
                         line=dict(
                             color='blue',
                             width=5
                         )), 1, 1)
        fig.add_trace(
            go.Scatter3d(x=[mean_mesh[0], mean_mesh[0] + size_mesh / 2 * Z_vector[0]],
                         y=[mean_mesh[1], mean_mesh[1] + size_mesh / 2 * Z_vector[1]],
                         z=[mean_mesh[2], mean_mesh[2] + size_mesh / 2 * Z_vector[2]],
                         mode='lines',
                         name="Z vector",
                         line=dict(
                             color='blue',
                             width=5
                         )), 1, 1)
        try:
            add_points2graph(fig, endplate_top, 'Endplate TOP', 3)
            add_points2graph(fig, endplate_bottom, 'Endplate BOTTOM', 3)
        except IndexError:
            print('Endplate_1: ', endplate_top)
            print('Endplate_2: ', endplate_bottom)

        fig.show()

    if return_points:
        return endplate_top, endplate_bottom, points_without_endplates
    else:
        return thresh_1, thresh_2, Z_vector, origin


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


def filter(t, data):
    # Setting standard filter requirements.
    order = 10
    fs = 50.0
    cutoff = 3.667

    # Filtering and plotting
    y = butter_lowpass_filter(data, cutoff, fs, order)

    plt.subplot(2, 1, 2)
    plt.plot(t, data, 'b-', label='data')
    plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
    plt.xlabel('Time [sec]')
    plt.grid()
    plt.legend()

    plt.subplots_adjust(hspace=0.35)
    plt.show()

    return t, y


def add_endplates_ns(mesh, pstf_path='', write=False):
    thresh_1, thresh_2, direction, origin = read_pstf_vertebra(pstf_path)
    print('Adding endplates to :', mesh.get_path())
    mesh.read()

    lonely_faces_nodes = mesh.get_lonely_faces_nodes()
    ns_list = mesh.get_named_selections_list()

    endplate_1 = []
    endplate_2 = []
    for node in lonely_faces_nodes:
        point = node.get_coord()
        rel_P = np.array(point) - origin
        cos_proj = rel_P.dot(direction.T)
        if cos_proj >= thresh_2:
            endplate_1.append(node.get_ID_node())
        elif cos_proj <= thresh_1:
            endplate_2.append(node.get_ID_node())

    # suppress duplicate of named selections
    temp_ns_list = []
    for ns in ns_list:
        if ns[0] not in ['ENDPLATE_TOP', 'ENDPLATE_BOTTOM']:
            temp_ns_list.append(ns)
    ns_list = temp_ns_list

    # add new endplates
    ns_list.append(['ENDPLATE_BOTTOM', endplate_1])
    ns_list.append(['ENDPLATE_TOP', endplate_2])

    mesh.set_named_selections_list(ns_list)

    if write:
        mesh.write()
    for ns in mesh.get_named_selections_list():
        print(ns[0], len(ns[1]))

    return mesh


def add_endplates_ns_from_param(mesh, direction, thresh1, thresh2, write=False):
    print('Adding endplates to :', mesh.get_path())
    mesh.read()
    node_list = mesh.get_node_list()
    node_coord = np.array([node.get_coord() for node in node_list])
    mean_mesh = np.array([node_coord[:, 0].mean(), node_coord[:, 1].mean(), node_coord[:, 2].mean()])
    lonely_faces_nodes = mesh.get_lonely_faces_nodes()
    ns_list = mesh.get_named_selections_list()

    endplate_1 = []
    endplate_2 = []
    for node in lonely_faces_nodes:
        point = node.get_coord()
        rel_P = np.array(point) - mean_mesh
        cos_proj = rel_P.dot(direction.T)
        if cos_proj >= thresh2:
            endplate_1.append(node.get_ID_node())
        elif cos_proj <= thresh1:
            endplate_2.append(node.get_ID_node())

    # suppress duplicate of named selections
    temp_ns_list = []
    for ns in ns_list:
        if ns[0] not in ['ENDPLATE_1', 'ENDPLATE_2']:
            temp_ns_list.append(ns)
    ns_list = temp_ns_list

    # add new endplates
    ns_list.append(['ENDPLATE_1', endplate_1])
    ns_list.append(['ENDPLATE_2', endplate_2])

    mesh.set_named_selections_list(ns_list)
    #new_path = mesh.get_path().split(".cdb")[0] + "_endplates.cdb"
    if write:
        mesh.write()
    for ns in mesh.get_named_selections_list():
        print(ns[0], len(ns[1]))

    return mesh


if __name__ == '__main__':

    is_Artorg = True

    if is_Artorg:
        cmd_workbench = r"C:\Users\U1033_BIOMECA\Desktop\Data_JPR\density_law_fitting\config_workbench.wbjn"
        script_act = r"C:\Users\U1033_BIOMECA\Desktop\Data_JPR\density_law_fitting\vertebra_analysis.py"

        sample_list = ['188', '192', '199', '203', '214', '217', '220', '224', '236', '240', '301']
        '''['188', '192', '195', '196', '199', '203', '204', '206', '208', '214', '217', '218', '220', '224',
                   '225', '226', '230', '231', '235', '236', '240', '248', '252', '256', '257', '260', '261', '264',
                   '268', '269', '273', '280', '281', '284', '285', '288', '289', '295', '298', '299', '301', '305',
                   '308', '309', '317']'''
        element_type_list = ['QT']
        size_list = ['1']
        location = 'VB'
        resolution = '294mic'
        seg_list = ['A', 'VA']

        for sample in sample_list:
            for seg in seg_list:
                for element_type in element_type_list:
                        for size in size_list:

                                mesh_save_path = r'E:\Artorg_data_2021_metastatic_vertebrae' + '\\' + sample + '\\' + sample + '_' + resolution + '_' + \
                                                  location + '_' + seg + '_' + element_type + '_' + size + 'mm.cdb'
                                stl_path = r'E:\Artorg_data_2021_metastatic_vertebrae' + '\\' + sample + '\\' + sample + '_' + resolution + '_' + \
                                                  location + '_' + seg + '.stl'

                                mesh = Mesh(path=mesh_save_path)
                                mesh.read()
                                mesh.get_lonely_faces_nodes()
                                for ns in mesh.get_named_selections_list():
                                    print(ns[0], len(ns[1]))
