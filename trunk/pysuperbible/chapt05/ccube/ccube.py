"""
// ccube.cpp
// OpenGL SuperBible
// Demonstrates primative RGB Color Cube
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

        # Black background
        glClearColor(0.0, 0.0, 0.0, 1.0)

        glEnable(GL_DEPTH_TEST)	
#        glEnable(GL_DITHER)
#        glShadeModel(GL_SMOOTH)

        pyglet.clock.schedule_interval(self._update, 1.0/60.0)

    def on_draw(self):
        self.clear()

        glPushMatrix();

        glRotatef(self.xRot, 1.0, 0.0, 0.0);
        glRotatef(self.yRot, 0.0, 1.0, 0.0);

        # Draw six quads
        glBegin(GL_QUADS);
        # Front Face
        # White
        glColor3ub(255, 255, 255);
        glVertex3f(50.0,50.0,50.0);

        # Yellow
        glColor3ub(255, 255, 0);
        glVertex3f(50.0,-50.0,50.0);

        # Red
        glColor3ub(255, 0, 0);
        glVertex3f(-50.0,-50.0,50.0);

        # Magenta
        glColor3ub(255, 0, 255);
        glVertex3f(-50.0,50.0,50.0);

    
        # Back Face
        # Cyan
        glColor3f(0.0, 1.0, 1.0);
        glVertex3f(50.0,50.0,-50.0);

        # Green
        glColor3f(0.0, 1.0, 0.0);
        glVertex3f(50.0,-50.0,-50.0);
        
        # Black
        glColor3f(0.0, 0.0, 0.0);
        glVertex3f(-50.0,-50.0,-50.0);

        # Blue
        glColor3f(0.0, 0.0, 1.0);
        glVertex3f(-50.0,50.0,-50.0);
    
        # Top Face
        # Cyan
        glColor3f(0.0, 1.0, 1.0);
        glVertex3f(50.0,50.0,-50.0);

        # White
        glColor3f(1.0, 1.0, 1.0);
        glVertex3f(50.0,50.0,50.0);

        # Magenta
        glColor3f(1.0, 0.0, 1.0);
        glVertex3f(-50.0,50.0,50.0);

        # Blue
        glColor3f(0.0, 0.0, 1.0);
        glVertex3f(-50.0,50.0,-50.0);
    
        # Bottom Face
        # Green
        glColor3f(0.0, 1.0, 0.0);
        glVertex3f(50.0,-50.0,-50.0);

        # Yellow
        glColor3f(1.0, 1.0, 0.0);
        glVertex3f(50.0,-50.0,50.0);

        # Red
        glColor3f(1.0, 0.0, 0.0);
        glVertex3f(-50.0,-50.0,50.0);

        # Black
        glColor3f(0.0, 0.0, 0.0);
        glVertex3f(-50.0,-50.0,-50.0);
    
        # Left face
        # White
        glColor3f(1.0, 1.0, 1.0);
        glVertex3f(50.0,50.0,50.0);

        # Cyan
        glColor3f(0.0, 1.0, 1.0);
        glVertex3f(50.0,50.0,-50.0);

        # Green
        glColor3f(0.0, 1.0, 0.0);
        glVertex3f(50.0,-50.0,-50.0);

        # Yellow
        glColor3f(1.0, 1.0, 0.0);
        glVertex3f(50.0,-50.0,50.0);
    
        # Right face
        # Magenta
        glColor3f(1.0, 0.0, 1.0);
        glVertex3f(-50.0,50.0,50.0);

        # Blue
        glColor3f(0.0, 0.0, 1.0);
        glVertex3f(-50.0,50.0,-50.0);

        # Black
        glColor3f(0.0, 0.0, 0.0);
        glVertex3f(-50.0,-50.0,-50.0);

        # Red
        glColor3f(1.0, 0.0, 0.0);
        glVertex3f(-50.0,-50.0,50.0);
        glEnd();

        glPopMatrix();

    def _update(self, dt):
        pass

    def on_resize(self, w, h):
        # Prevent a divide by zero
        if h == 0:
            h = 1

        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)

        # Reset coordinate system
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        fAspect = w / h
        gluPerspective(35.0, fAspect, 1.0, 1000.0)
         
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -400.0)
    
    def on_key_press(self, sym, mods):
        if sym == key.UP:
            self.xRot -= 5.0
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
    window = Window(800, 600, 'RGB Cube')
    pyglet.app.run()
