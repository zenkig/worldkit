"""
// Solar.cpp
// OpenGL SuperBible
// Demonstrates OpenGL nested coordinate transformations
// and perspective
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


def gl_vec(typ, *args):
    """return ctypes array of GLwhatever for Pyglet's OpenGL interface. (This
    seems to work for all types, but it does almost no type conversion. Just
    think in terms of "C without type casting".)
    typ -> ctype or GL name for ctype; see pyglet.gl.GLenum through GLvoid
    args -> Either vararg, or args[0] as an iterable container
    Examples:
        # Float
        ar = gl_vec(GLfloat, 0.0, 1.0, 0.0)
        ar = gl_vec(GLfloat, [0.0, 1.0, 0.0])
        # Unsigned byte
        ar = gl_vec(GLubyte, 'a','b','c')
        ar = gl_vec(GLubyte, 'abc')
        ar = gl_vec(GLubyte, ['a','b','c'])
        ar = gl_vec(GLubyte, 97, 98, 99)
    """
    if len(args) == 1:
        if isinstance(args[0],(tuple,list)):
            args = args[0]
        elif isinstance(args[0],str) and len(args[0]) > 1:
            args = args[0]
    if isinstance(args[0], str) and typ is GLubyte:
        return (typ * len(args))(*[ord(c) for c in args])
    else:
        return (typ * len(args))(*args)


class Window(pyglet.window.Window):

    # Lighting values
    whiteLight = gl_vec(GLfloat, 0.2, 0.2, 0.2, 1.0)
    sourceLight = gl_vec(GLfloat, 0.8, 0.8, 0.8, 1.0)
    lightPos = gl_vec(GLfloat, 0.0, 0.0, 0.0, 1.0)

    fEarthRot = 0.0
    fMoonRot = 0.0

    def __init__(self, w, h, title='Pyglet App'):
        super(Window, self).__init__(w, h, title)

        # Light values and coordinates
        glEnable(GL_DEPTH_TEST) # Hidden surface removal
        glFrontFace(GL_CCW)     # Counter clock-wise polygons face out
        glEnable(GL_CULL_FACE)  # Do not calculate inside of jet

        # Enable lighting
        glEnable(GL_LIGHTING)

        # Setup and enable light 0
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, self.whiteLight)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.sourceLight)
        glLightfv(GL_LIGHT0, GL_POSITION, self.lightPos)
        glEnable(GL_LIGHT0)

        # Enable color tracking
        glEnable(GL_COLOR_MATERIAL)
        
        # Set Material properties to follow glColor values
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

        # Black blue background
        glClearColor(0.0, 0.0, 0.0, 1.0)

        pyglet.clock.schedule_interval(self._update, 1.0/60.0)

    def on_draw(self):
        self.clear()

        # Earth and Moon angle of revolution
        fMoonRot = 0.0
        fEarthRot = 0.0

        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Save the matrix state and do the rotations
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

        # Translate the whole scene out and into view	
        glTranslatef(0.0, 0.0, -300.0)
        
        # Set material color, Red
        # Sun
        glDisable(GL_LIGHTING)
        glColor3ub(255, 255, 0)
        glutSolidSphere(15.0, 30, 17)
        glEnable(GL_LIGHTING)

        # Move the light after we draw the sun!
        glLightfv(GL_LIGHT0, GL_POSITION, self.lightPos)

        # Rotate coordinate system
        glRotatef(self.fEarthRot, 0.0, 1.0, 0.0)

        # Draw the Earth
        glColor3ub(0,0,255)
        glTranslatef(105.0,0.0,0.0)
        glutSolidSphere(15.0, 30, 17)

        # Rotate from Earth based coordinates and draw Moon
        glColor3ub(200,200,200)
        glRotatef(self.fMoonRot,0.0, 1.0, 0.0)
        glTranslatef(30.0, 0.0, 0.0)

        glutSolidSphere(6.0, 30, 17)

        # Restore the matrix state
        glPopMatrix()	# Modelview matrix

    def _update(self, dt):
        # Step earth orbit 5 degrees
        self.fEarthRot = (self.fEarthRot + 1.0) % 360.0
        self.fMoonRot = (self.fMoonRot + 3.0) % 360.0

    def on_resize(self, w, h):
        # Prevent a divide by zero
        if h == 0:
            h = 1

        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)

        # Calculate aspect ratio of the window
        fAspect = w / h

        # Set the perspective coordinate system
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # field of view of 45 degrees, near and far planes 1.0 and 425
        gluPerspective(45.0, fAspect, 1.0, 425.0)

        # Modelview matrix reset
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

if __name__ == '__main__':
    window = Window(800, 600, 'Earth/Moon/Sun System')
    pyglet.app.run()
