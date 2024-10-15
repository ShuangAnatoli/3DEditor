import numpy as np
import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import glfw
from pyrr import Matrix44
from obj_loader import load_obj
from shader_loader import compile_shader
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


def draw():
    # Render the mesh with normals
    glBegin(GL_TRIANGLES)
    for face, normal in zip(faces, face_normals):
        glNormal3fv(normal)
        for vertex_idx in face:
            glVertex3fv(vertices[vertex_idx])
    glEnd()


# Load shader programs
flat_shader_program = None
phong_shader_program = None

# Shading mode (0 for flat, 1 for Phong)
current_shading_mode = 0

def key_callback(window, key, scancode, action, mods):
    global current_shading_mode
    if key == glfw.KEY_S and action == glfw.PRESS:
        current_shading_mode = (current_shading_mode + 1) % 2

def render_scene(vertices, faces, normals, shader_program):
    # Use the selected shader program
    glUseProgram(shader_program)

    # Set up matrices and light source
    model = Matrix44.identity()
    view = Matrix44.look_at([0.0, 0.0, 3.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0])
    projection = Matrix44.perspective_projection(45, 800/600, 0.1, 100)

    # Pass matrices and lighting to the shader
    glUniformMatrix4fv(glGetUniformLocation(shader_program, "model"), 1, GL_FALSE, model)
    glUniformMatrix4fv(glGetUniformLocation(shader_program, "view"), 1, GL_FALSE, view)
    glUniformMatrix4fv(glGetUniformLocation(shader_program, "projection"), 1, GL_FALSE, projection)
    glUniform3f(glGetUniformLocation(shader_program, "lightPos"), 2.0, 4.0, 3.0)
    glUniform3f(glGetUniformLocation(shader_program, "viewPos"), 0.0, 0.0, 3.0)
    glUniform3f(glGetUniformLocation(shader_program, "lightColor"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(shader_program, "objectColor"), 1.0, 0.5, 0.31)

    # Render the object using the active shader program
    # (OpenGL rendering code goes here)

def main():
    global flat_shader_program, phong_shader_program

    # Initialize GLFW
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Flat and Phong Shading", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    # Load the shaders
    flat_shader_program = compile_shader("shaders/flat_vertex_shader.glsl", "shaders/flat_fragment_shader.glsl")
    phong_shader_program = compile_shader("shaders/phong_vertex_shader.glsl", "shaders/phong_fragment_shader.glsl")

    # Load the mesh (vertices, faces, and normals)
    vertices, faces, normals = load_obj("../models/bunny.obj")

    # Main render loop
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Switch between shading modes based on current_shading_mode
        if current_shading_mode == 0:
            render_scene(vertices, faces, normals, flat_shader_program)  # Flat shading
        else:
            render_scene(vertices, faces, normals, phong_shader_program)  # Phong shading

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()