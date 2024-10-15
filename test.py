import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *


def load_obj(filename):
    vertices = []
    faces = []

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v '):  # Vertex
                parts = line.split()
                vertex = list(map(float, parts[1:4]))
                vertices.append(vertex)
            elif line.startswith('f '):  # Face
                parts = line.split()
                face = [int(part.split('/')[0]) - 1 for part in parts[1:]]  # OBJ indices are 1-based
                faces.append(face)

    return np.array(vertices, dtype=np.float32), faces


def compute_flat_normals(vertices, faces):
    normals = np.zeros(vertices.shape, dtype=np.float32)

    for face in faces:
        v0 = vertices[face[0]]
        v1 = vertices[face[1]]
        v2 = vertices[face[2]]

        edge1 = v1 - v0
        edge2 = v2 - v0

        normal = np.cross(edge1, edge2)
        normal = normal / np.linalg.norm(normal)

        for vertex_index in face:
            normals[vertex_index] += normal

    # Normalize normals
    normals = normals / np.linalg.norm(normals, axis=1)[:, np.newaxis]
    return normals


def render(vertices, normals):
    glBegin(GL_TRIANGLES)
    for i in range(len(vertices)):
        glNormal3fv(normals[i])  # Use vertex normals
        glVertex3fv(vertices[i])
    glEnd()


def setup_lighting():
    # Enable lighting
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Set the light position
    light_position = [1.0, 1.0, 1.0, 0.0]  # Directional light
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    # Set light properties
    ambient_light = [0.2, 0.2, 0.2, 1.0]  # Ambient light
    diffuse_light = [1.0, 1.0, 1.0, 1.0]  # Diffuse light
    specular_light = [1.0, 1.0, 1.0, 1.0]  # Specular light

    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_light)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular_light)

    # Set material properties
    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient_light)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse_light)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular_light)
    glMaterialf(GL_FRONT, GL_SHININESS, 50.0)  # Shininess factor


def main():
    if not glfw.init():
        return

    window = glfw.create_window(640, 480, "Bunny OBJ Model", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    # Load bunny.obj
    vertices, faces = load_obj("../models/bunny.obj")
    normals = compute_flat_normals(vertices, faces)

    # Set the initial rotation angles
    angle_x, angle_y = 0.0, 0.0

    # Scale factor
    scale_factor = 0.5  # Adjust this value to scale the model up or down
    vertices *= scale_factor  # Scale the model

    # Enable depth testing for 3D effects
    glEnable(GL_DEPTH_TEST)

    # Set up perspective projection
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, 640 / 480, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

    # Set up lighting
    setup_lighting()

    # Main loop
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Load identity matrix
        glLoadIdentity()

        # Move the camera back
        glTranslatef(0.0, 0.0, -3.0)

        # Apply rotations
        glRotatef(angle_x, 1.0, 0.0, 0.0)  # Rotate around X-axis
        glRotatef(angle_y, 0.0, 1.0, 0.0)  # Rotate around Y-axis

        render(vertices, normals)

        glfw.swap_buffers(window)
        glfw.poll_events()

        # Check for keyboard input
        if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
            angle_x += 1.0  # Rotate up
        if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
            angle_x -= 1.0  # Rotate down
        if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
            angle_y -= 1.0  # Rotate left
        if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
            angle_y += 1.0  # Rotate right

    glfw.terminate()


if __name__ == "__main__":
    main()
