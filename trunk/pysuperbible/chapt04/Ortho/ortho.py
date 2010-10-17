"""
// Ortho.cpp
// OpenGL SuperBible
// Richard S. Wright Jr.
// Demonstrates Orthographic Projection
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

    xRot = 0.0
    yRot = 0.0

    def __init__(self, w, h, title='Pyglet App'):
        super(Window, self).__init__(w, h, title)

        # Light values and coordinates
        whiteLight = gl_vec(GLfloat, 0.45, 0.45, 0.45, 1.0)
        sourceLight = gl_vec(GLfloat, 0.25, 0.25, 0.25, 1.0)
        lightPos = gl_vec(GLfloat, -50., 25.0, 250.0, 0.0)

        glEnable(GL_DEPTH_TEST) # Hidden surface removal
        glFrontFace(GL_CCW)     # Counter clock-wise polygons face out
        glEnable(GL_CULL_FACE)  # Do not calculate inside of jet

        # Enable lighting
        glEnable(GL_LIGHTING)

        # Setup and enable light 0
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, whiteLight)
        glLightfv(GL_LIGHT0,GL_AMBIENT, sourceLight)
        glLightfv(GL_LIGHT0,GL_DIFFUSE, sourceLight)
        glLightfv(GL_LIGHT0,GL_POSITION, lightPos)
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

        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        fZ = 100.0
        bZ = -100.0

        # Save the matrix state and do the rotations
        glPushMatrix()
        glRotatef(self.xRot, 1.0, 0.0, 0.0)
        glRotatef(self.yRot, 0.0, 1.0, 0.0)

        # Set material color, Red
        glColor3f(1.0, 0.0, 0.0)

        # Front Face #################
        glBegin(GL_QUADS)
        # Pointing straight out Z
        glNormal3f(0.0, 0.0, 1.0)	

        # Left Panel
        glVertex3f(-50.0, 50.0, fZ)
        glVertex3f(-50.0, -50.0, fZ)
        glVertex3f(-35.0, -50.0, fZ)
        glVertex3f(-35.0,50.0,fZ)

        # Right Panel
        glVertex3f(50.0, 50.0, fZ)
        glVertex3f(35.0, 50.0, fZ)
        glVertex3f(35.0, -50.0, fZ)
        glVertex3f(50.0,-50.0,fZ)

        # Top Panel
        glVertex3f(-35.0, 50.0, fZ)
        glVertex3f(-35.0, 35.0, fZ)
        glVertex3f(35.0, 35.0, fZ)
        glVertex3f(35.0, 50.0,fZ)

        # Bottom Panel
        glVertex3f(-35.0, -35.0, fZ)
        glVertex3f(-35.0, -50.0, fZ)
        glVertex3f(35.0, -50.0, fZ)
        glVertex3f(35.0, -35.0,fZ)

        # Top length section ##############
        # Normal points up Y axis
        glNormal3f(0.0, 1.0, 0.0)
        glVertex3f(-50.0, 50.0, fZ)
        glVertex3f(50.0, 50.0, fZ)
        glVertex3f(50.0, 50.0, bZ)
        glVertex3f(-50.0,50.0,bZ)
        
        # Bottom section
        glNormal3f(0.0, -1.0, 0.0)
        glVertex3f(-50.0, -50.0, fZ)
        glVertex3f(-50.0, -50.0, bZ)
        glVertex3f(50.0, -50.0, bZ)
        glVertex3f(50.0, -50.0, fZ)

        # Left section
        glNormal3f(1.0, 0.0, 0.0)
        glVertex3f(50.0, 50.0, fZ)
        glVertex3f(50.0, -50.0, fZ)
        glVertex3f(50.0, -50.0, bZ)
        glVertex3f(50.0, 50.0, bZ)

        # Right Section
        glNormal3f(-1.0, 0.0, 0.0)
        glVertex3f(-50.0, 50.0, fZ)
        glVertex3f(-50.0, 50.0, bZ)
        glVertex3f(-50.0, -50.0, bZ)
        glVertex3f(-50.0, -50.0, fZ)
        glEnd()

        glFrontFace(GL_CW)		# clock-wise polygons face out

        glBegin(GL_QUADS)
        # Back section
        # Pointing straight out Z
        glNormal3f(0.0, 0.0, -1.0)	

        # Left Panel
        glVertex3f(-50.0, 50.0, bZ)
        glVertex3f(-50.0, -50.0, bZ)
        glVertex3f(-35.0, -50.0, bZ)
        glVertex3f(-35.0,50.0,bZ)

        # Right Panel
        glVertex3f(50.0, 50.0, bZ)
        glVertex3f(35.0, 50.0, bZ)
        glVertex3f(35.0, -50.0, bZ)
        glVertex3f(50.0,-50.0,bZ)

        # Top Panel
        glVertex3f(-35.0, 50.0, bZ)
        glVertex3f(-35.0, 35.0, bZ)
        glVertex3f(35.0, 35.0, bZ)
        glVertex3f(35.0, 50.0,bZ)

        # Bottom Panel
        glVertex3f(-35.0, -35.0, bZ)
        glVertex3f(-35.0, -50.0, bZ)
        glVertex3f(35.0, -50.0, bZ)
        glVertex3f(35.0, -35.0,bZ)
    
        # Insides ##############
        glColor3f(0.75, 0.75, 0.75)

        # Normal points up Y axis
        glNormal3f(0.0, 1.0, 0.0)
        glVertex3f(-35.0, 35.0, fZ)
        glVertex3f(35.0, 35.0, fZ)
        glVertex3f(35.0, 35.0, bZ)
        glVertex3f(-35.0,35.0,bZ)
        
        # Bottom section
        glNormal3f(0.0, 1.0, 0.0)
        glVertex3f(-35.0, -35.0, fZ)
        glVertex3f(-35.0, -35.0, bZ)
        glVertex3f(35.0, -35.0, bZ)
        glVertex3f(35.0, -35.0, fZ)

        # Left section
        glNormal3f(1.0, 0.0, 0.0)
        glVertex3f(-35.0, 35.0, fZ)
        glVertex3f(-35.0, 35.0, bZ)
        glVertex3f(-35.0, -35.0, bZ)
        glVertex3f(-35.0, -35.0, fZ)

        # Right Section
        glNormal3f(-1.0, 0.0, 0.0)
        glVertex3f(35.0, 35.0, fZ)
        glVertex3f(35.0, -35.0, fZ)
        glVertex3f(35.0, -35.0, bZ)
        glVertex3f(35.0, 35.0, bZ)
        glEnd()

        glFrontFace(GL_CCW)		# Counter clock-wise polygons face out

        # Restore the matrix state
        glPopMatrix()

    def _update(self, dt):
        pass

    def on_resize(self, w, h):
        nRange = 120.0
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
                -nRange*h/w, nRange*h/w,
                -nRange*2.0, nRange*2.0)
        else:
            glOrtho(
                -nRange*w/h, nRange*w/h,
                -nRange, nRange,
                -nRange*2.0, nRange*2.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    
    def on_key_press(self, sym, mods):
        if sym == key.UP:
            self.xRot-= 5.0
        elif sym == key.DOWN:
            self.xRot += 5.0
        elif sym == key.LEFT:
            self.yRot -= 5.0
        elif sym == key.RIGHT:
            self.yRot += 5.0
        else:
            super(Window, self).on_key_press(sym, mods)
        self.xRot %= 360.0
        self.yRot %= 360.0
    
    def on_close(self):
        pyglet.clock.unschedule(self._update)
        super(Window, self).on_close()

if __name__ == '__main__':
    window = Window(800, 600, 'Ortho')
    pyglet.app.run()
