"""
// Jet.cpp
// A hand modeled Jet airplane
// OpenGL SuperBible
// Beginning of OpenGL lighting sample
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

    xRot = 0.0
    yRot = 0.0

    def __init__(self, w, h, title='Pyglet App'):
        super(Window, self).__init__(w, h, title)

        glEnable(GL_DEPTH_TEST) # Hidden surface removal
        glEnable(GL_CULL_FACE)  # Do not calculate inside of jet
        glFrontFace(GL_CCW)     # Counter clock-wise polygons face out

        # Nice light blue
        glClearColor(0.0, 0.0, 05., 1.0)

        pyglet.clock.schedule_interval(self._update, 1.0/60.0)

    def on_draw(self):
        self.clear()

        # Save matrix state and do the rotation
        glPushMatrix()
        glRotatef(self.xRot, 1.0, 0.0, 0.0)
        glRotatef(self.yRot, 0.0, 1.0, 0.0)

        # Nose Cone ##############
        # White
        glColor3ub(255, 255, 255)
        glBegin(GL_TRIANGLES)
        glVertex3f(0.0, 0.0, 60.0)
        glVertex3f(-15.0, 0.0, 30.0)
        glVertex3f(15.0,0.0,30.0)

        # Black
        glColor3ub(0,0,0)
        glVertex3f(15.0,0.0,30.0)
        glVertex3f(0.0, 15.0, 30.0)
        glVertex3f(0.0, 0.0, 60.0)
    
        # Red
        glColor3ub(255,0,0)
        glVertex3f(0.0, 0.0, 60.0)
        glVertex3f(0.0, 15.0, 30.0)
        glVertex3f(-15.0,0.0,30.0)

        # Body of the Plane ############
        # Green
        glColor3ub(0,255,0)
        glVertex3f(-15.0,0.0,30.0)
        glVertex3f(0.0, 15.0, 30.0)
        glVertex3f(0.0, 0.0, -56.0)
        
        glColor3ub(255,255,0)
        glVertex3f(0.0, 0.0, -56.0)
        glVertex3f(0.0, 15.0, 30.0)
        glVertex3f(15.0,0.0,30.0)	
    
        glColor3ub(0, 255, 255)
        glVertex3f(15.0,0.0,30.0)
        glVertex3f(-15.0, 0.0, 30.0)
        glVertex3f(0.0, 0.0, -56.0)
    
        # ##############

        # Left wing

        glColor3ub(128,128,128)
        glVertex3f(0.0,2.0,27.0)
        glVertex3f(-60.0, 2.0, -8.0)
        glVertex3f(60.0, 2.0, -8.0)
    
        glColor3ub(64,64,64)
        glVertex3f(60.0, 2.0, -8.0)
        glVertex3f(0.0, 7.0, -8.0)
        glVertex3f(0.0,2.0,27.0)
    
        glColor3ub(192,192,192)
        glVertex3f(60.0, 2.0, -8.0)
        glVertex3f(-60.0, 2.0, -8.0)
        glVertex3f(0.0,7.0,-8.0)
    
        # Other wing top section
        glColor3ub(64,64,64)
        glVertex3f(0.0,2.0,27.0)
        glVertex3f(0.0, 7.0, -8.0)
        glVertex3f(-60.0, 2.0, -8.0)

        glColor3ub(255,128,255)
        glVertex3f(-30.0, -0.50, -57.0)
        glVertex3f(30.0, -0.50, -57.0)
        glVertex3f(0.0,-0.50,-40.0)
    
        # top of left side
        glColor3ub(255,128,0)
        glVertex3f(0.0,-0.5,-40.0)
        glVertex3f(30.0, -0.5, -57.0)
        glVertex3f(0.0, 4.0, -57.0)
    
        # top of right side
        glColor3ub(255,128,0)
        glVertex3f(0.0, 4.0, -57.0)
        glVertex3f(-30.0, -0.5, -57.0)
        glVertex3f(0.0,-0.5,-40.0)
    
        # back of bottom of tail
        glColor3ub(255,255,255)
        glVertex3f(30.0,-0.5,-57.0)
        glVertex3f(-30.0, -0.5, -57.0)
        glVertex3f(0.0, 4.0, -57.0)
    
        # Top of Tail section left
        glColor3ub(255,0,0)
        glVertex3f(0.0,0.5,-40.0)
        glVertex3f(3.0, 0.5, -57.0)
        glVertex3f(0.0, 25.0, -65.0)
    
        glColor3ub(255,0,0)
        glVertex3f(0.0, 25.0, -65.0)
        glVertex3f(-3.0, 0.5, -57.0)
        glVertex3f(0.0,0.5,-40.0)

        # Back of horizontal section
        glColor3ub(128,128,128)
        glVertex3f(3.0,0.5,-57.0)
        glVertex3f(-3.0, 0.5, -57.0)
        glVertex3f(0.0, 25.0, -65.0)
    
        glEnd() # Of Jet

        glPopMatrix()

    def _update(self, dt):
        pass

    def on_resize(self, w, h):
        nRange = 80.0
        #/ Prevent a divide by zero
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
                -nRange, nRange)
        else:
            glOrtho(
                -nRange*w/h, nRange*w/h,
                -nRange, nRange,
                -nRange, nRange)

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
    window = Window(800, 600, 'Jet')
    pyglet.app.run()
