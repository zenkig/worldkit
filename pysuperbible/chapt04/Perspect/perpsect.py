"""
// Perspect.cpp
// Demonstrates Perspective Projection
// OpenGL SuperBible
// Richard S. Wright Jr.
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

    # Rotation amounts
    xRot = 0.0
    yRot = 0.0

    def __init__(self, w, h, title='Pyglet App'):
        super(Window, self).__init__(w, h, title)

        # Light values and coordinates
        whiteLight = M3DVector4f(0.45, 0.45, 0.45, 1.0)
        sourceLight = M3DVector4f(0.25, 0.25, 0.25, 1.0)
        lightPos = M3DVector4f(-50.0, 25.0, 250.0, 0.0)

        glEnable(GL_DEPTH_TEST)	# Hidden surface removal
        glFrontFace(GL_CCW)		# Counter clock-wise polygons face out
        glEnable(GL_CULL_FACE)	# Do not calculate inside of jet

        # Enable lighting
        glEnable(GL_LIGHTING)

        # Setup and enable light 0
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, vecf(whiteLight))
        glLightfv(GL_LIGHT0,GL_AMBIENT, vecf(sourceLight))
        glLightfv(GL_LIGHT0,GL_DIFFUSE, vecf(sourceLight))
        glLightfv(GL_LIGHT0,GL_POSITION, vecf(lightPos))
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

        fZ = 100.0
        bZ = -100.0

        # Save the matrix state and do the rotations
        glPushMatrix()
        glTranslatef(0.0, 0.0, -300.0)
        glRotatef(self.xRot, 1.0, 0.0, 0.0)
        glRotatef(self.yRot, 0.0, 1.0, 0.0)

        # Set material color, Red
        glColor3f(1.0, 0.0, 0.0)

        # Front Face ///////////////////////////////////
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

        # Top length section ////////////////////////////
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
    
        # Insides /////////////////////////////
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
        glVertex3f(35.0, 35.0, bZ);
        glEnd()

        glFrontFace(GL_CCW)		# Counter clock-wise polygons face out

        # Restore the matrix state
        glPopMatrix()

    def _update(self, dt):
        pass

    def on_resize(self, w, h):
        # Prevent a divide by zero
        if h == 0:
            h = 1

        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)

        fAspect = w / h

        # Reset coordinate system
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Produce the perspective projection
        gluPerspective(60.0, fAspect, 1.0, 400.0)

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

        self.xRot %= 360
        self.yRot %= 360
    
    def on_close(self):
        pyglet.clock.unschedule(self._update)
        super(Window, self).on_close()

if __name__ == '__main__':
    window = Window(800, 600, 'Perspective Projection')
    pyglet.app.run()
