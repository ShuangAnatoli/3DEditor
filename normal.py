import numpy as np

vertices = []
faces = []

with open("../models/bunny.obj") as file:
    for line in file:
        if line.startswith('v '):
            parts = line.split()
            vertex = list(map(float, parts[1:4]))
            vertices.append(vertex)
        elif line.startswith('f '):
            parts = line.split()
            face = [int(p.split('/')[0]) - 1 for p in parts[1:]]
            faces.append(face)

print(vertices)


# ----------------------------------------------------------------
# Flat face normal
def compute_face_normals(vertices, faces):
    face_normals = []
    for face in faces:
        v1, v2, v3 = [np.array(vertices[i]) for i in face]
        normal = np.cross(v2 - v1, v3 - v1)
        normal = normal / np.linalg.norm(normal)
        face_normals.append(normal)
    return face_normals


# Smoothed normal


def compute_vertex_normals(vertices, faces, face_normals):
    vertex_normals = np.zeros((len(vertices), 3))

    # Accumulate normals for each vertex
    for i, face in enumerate(faces):
        for vertex in face:
            vertex_normals[vertex] += face_normals[i]

    # Normalize the vertex normals, but handle zero-length vectors
    def safe_normalize(v):
        norm = np.linalg.norm(v)
        if norm > 1e-6:
            return v / norm
        else:
            return np.zeros(3)  # Return a zero vector if the normal length is too small

    # Apply safe normalization to all vertex normals
    vertex_normals = np.array([safe_normalize(n) for n in vertex_normals])

    return vertex_normals


print("normal")
face_normals = compute_face_normals(vertices, faces)

print(compute_vertex_normals(vertices, faces, face_normals))
