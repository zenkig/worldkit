"""
// Triangle.cpp
// OpenGL SuperBible
// Demonstrates OpenGL color triangle
// Program by Richard S. Wright Jr.
## Pythonated for Pyglet by Gummbum
"""


import sys

import pyglet
from pyglet.gl import *
from pyglet.window import key

# GLUT for shapes
from OpenGL.GLUT import *

sys.path.append('../../lib')
from gltools import *
from math3d import *


def vecf(*args):
    """return ctypes array of GLfloat for Pyglet's OpenGL interface.
    args -> Either vararg floats, or args[0] as an interable float container
    If using module OpenGL.GL directly you don't need this conversion.
    """
    if len(args) > 1:
        return (GLfloat * len(args))(*args)
    else:
        return (GLfloat * len(args[0]))(*args[0])


class Window(pyglet.window.Window):

    def __init__(self):
        super(Window, self).__init__(800, 600, 'RGB Triangle')

        # Black background
        glClearColor(0.0, 0.0, 0.0, 1.0 )

        pyglet.clock.schedule_interval(self._update, 1.0/60.0)

    def on_draw(self):
        self.clear()

        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT)

        # Enable smooth shading
        glShadeModel(GL_SMOOTH)

        # Draw the triangle
        glBegin(GL_TRIANGLES)
        # Red Apex
        glColor3ub(255,0,0)
        glVertex3f(0.0,200.0,0.0)

        # Green on the right bottom corner
        glColor3ub(0,255,0)
        glVertex3f(200.0,-70.0,0.0)

        # Blue on the left bottom corner
        glColor3ub(0,0,255)
        glVertex3f(-200.0, -70.0, 0.0)
        glEnd();

    def _update(self, dt):
        pass

    def on_resize(self, w, h):
        # Prevent a divide by zero, when window is too short
        # (you cant make a window of zero width).
        if h == 0:
            h = 1

        # Set the viewport to be the entire window
        glViewport(0, 0, w, h)

        # Reset the coordinate system before modifying
        glLoadIdentity()


        # Keep the square square.

        # Window is higher than wide
        if w <= h:
            windowHeight = 250.0*h/w
            windowWidth = 250.0
        else:
            # Window is wider than high
            windowWidth = 250.0*w/h
            windowHeight = 250.0

        # Set the clipping volume
        glOrtho(
            -windowWidth, windowWidth,
            -windowHeight, windowHeight,
            1.0, -1.0)
    
    def on_key_press(self, sym, mods):
        super(Window, self).on_key_press(sym, mods)
    
    def on_close(self):
        pyglet.clock.unschedule(self._update)
        super(Window, self).on_close()

if __name__ == '__main__':
    window = Window()
    pyglet.app.run()
