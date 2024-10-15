from OpenGL.GL import *


def compile_shader(vertex_path, fragment_path):
    # Compile vertex shader
    with open(vertex_path, 'r') as f:
        vertex_code = f.read()
    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader, vertex_code)
    glCompileShader(vertex_shader)

    # Compile fragment shader
    with open(fragment_path, 'r') as f:
        fragment_code = f.read()
    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader, fragment_code)
    glCompileShader(fragment_shader)

    # Link shader program
    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)

    # Clean up shaders (they are no longer needed after linking)
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return shader_program
