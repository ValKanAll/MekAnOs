import numpy as np
from stl import mesh
import random


class STL:
    def __init__(self, path):
        self.path = path
        self.stl_mesh = mesh.Mesh.from_file(self.path)
        self.triangles = self.stl_mesh.points
        self.normals = self.stl_mesh.normals

    def triangles(self):
        return self.stl_mesh.points

    def normals(self):
        return self.stl_mesh.normals

    def mesh(self):
        return self.stl_mesh

    def get_sample_points(self, population=1000):
        '''
        Gets x, y, z list of coordinates from stl file
        :param path: stl_path in str type
        :param stl_mesh: if not path, stl_mesh is given of type Mesh
        :param population: number of points considered
        :return: numpy array points list of coordinates (x, y, z)
        '''

        points = []
        for triangle in self.triangles:
            points.append((triangle[0:3] + triangle[3:6] + triangle[6:9])/3)  # center of triangle

        points = np.array(random.sample(points, population))  # returns np.array of n=population samples from points

        return points

    def transform_stl(self, R, T, return_new=False):
        '''
        Transform stl from rotation (R) and translation (T)
        :param R: rotation matrix as 3x3 matrix
        :param T: translation as 3x1 matrix
        :param return_new: if True returns another mesh with applied transformation and leave the origin one unchanged
        :return: New stl with applied rotation and translation
        '''
        R = R.T
        RT_matrix = np.array([
            [R[0][0], R[0][1], R[0][2], T[0]],
            [R[1][0], R[1][1], R[1][2], T[1]],
            [R[2][0], R[2][1], R[2][2], T[2]],
            [0, 0, 0, 1]
        ])
        if return_new:
            data = self.stl_mesh.data
            new_mesh = mesh.Mesh(data.copy())  # copy data from init mesh
            new_mesh.transform(RT_matrix)
            return new_mesh

        else:
            self.stl_mesh.transform(RT_matrix)
            return self.stl_mesh

