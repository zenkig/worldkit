"""
// Atom.cpp
// OpenGL SuperBible
// Demonstrates OpenGL coordinate transformation
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


class Window(pyglet.window.Window):

    # Angle of revolution around the nucleus
    fElect1 = 0.0

    def __init__(self, w, h, title='Pyglet App'):
        super(Window, self).__init__(w, h, title)

        glEnable(GL_DEPTH_TEST)	    # Hidden surface removal
        glFrontFace(GL_CCW)		    # Counter clock-wise polygons face out
        glEnable(GL_CULL_FACE)		# Do not calculate inside of jet

        # Black background
        glClearColor(0.0, 0.0, 0.0, 1.0)
        
        pyglet.clock.schedule_interval(self._update, 1.0/60.0)

    def on_draw(self):
        self.clear()

        fElect1 = self.fElect1

        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Reset the modelview matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Translate the whole scene out and into view	
        # This is the initial viewing transformation
        glTranslatef(0.0, 0.0, -100.0)

        # Red Nucleus
        glColor3ub(255, 0, 0)
        glutSolidSphere(10.0, 15, 15)

        # Yellow Electrons
        glColor3ub(255,255,0)

        # First Electron Orbit
        # Save viewing transformation
        glPushMatrix()

        # Rotate by angle of revolution
        glRotatef(fElect1, 0.0, 1.0, 0.0)

        # Translate out from origin to orbit distance
        glTranslatef(90.0, 0.0, 0.0)

        # Draw the electron
        glutSolidSphere(6.0, 15, 15)

        # Restore the viewing transformation
        glPopMatrix()

        # Second Electron Orbit
        glPushMatrix()
        glRotatef(45.0, 0.0, 0.0, 1.0)
        glRotatef(fElect1, 0.0, 1.0, 0.0)
        glTranslatef(-70.0, 0.0, 0.0)
        glutSolidSphere(6.0, 15, 15)
        glPopMatrix()

        # Third Electron Orbit
        glPushMatrix()
        glRotatef(360.0-45.0,0.0, 0.0, 1.0)
        glRotatef(fElect1, 0.0, 1.0, 0.0)
        glTranslatef(0.0, 0.0, 60.0)
        glutSolidSphere(6.0, 15, 15)
        glPopMatrix()

    def _update(self, dt):
        # Increment the angle of revolution
        self.fElect1 = (self.fElect1 + 1.0) % 360.0

    def on_resize(self, w, h):
        nRange = 100.0

        # Prevent a divide by zero
        if h == 0:
            h = 1

        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)

        # Reset coordinate system
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Establish clipping volume (left, right, bottom, top, near, far)
        if w <= h:
            glOrtho(
                -nRange, nRange,
                nRange*h/w, -nRange*h/w,
                -nRange*2.0, nRange*2.0)
        else:
            glOrtho(
                -nRange*w/h, nRange*w/h,
                nRange, -nRange,
                -nRange*2.0, nRange*2.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def on_close(self):
        pyglet.clock.unschedule(self._update)
        super(Window, self).on_close()


if __name__ == '__main__':
    window = Window(800, 600, 'OpenGL Atom')
    pyglet.app.run()
