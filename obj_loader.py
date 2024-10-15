import numpy as np


def load_obj(filename):
    vertices = []
    faces = []
    normals = []

    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('v '):
                vertices.append([float(i) for i in line.split()[1:4]])
            elif line.startswith('f '):
                face = [int(i.split('/')[0]) - 1 for i in line.split()[1:]]
                faces.append(face)
            elif line.startswith('vn '):
                normals.append([float(i) for i in line.split()[1:4]])

    return np.array(vertices, dtype=np.float32), np.array(faces, dtype=np.int32), np.array(normals, dtype=np.float32)
