"""
// Smoother.cpp
// OpenGL SuperBible
// Demonstrates point, line, and polygon smoothing
// Program by Richard S. Wright Jr.
## Pythonated for Pyglet by Gummbum
"""


from math import cos, sin
from random import random as rand
import sys

import pyglet
from pyglet.gl import *
from pyglet.window import key

# GLUT for shapes
from OpenGL.GLUT import *

sys.path.append('../../lib')
from gltools import *
from math3d import *
from glframe import GLFrame


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

    # Array of small stars
    SMALL_STARS = 100
    vSmallStars = [None] * SMALL_STARS      # M3DVector2f

    MEDIUM_STARS = 40
    vMediumStars = [None] * MEDIUM_STARS    # M3DVector2f

    LARGE_STARS = 15
    vLargeStars = [None] * LARGE_STARS      # M3DVector2f

    SCREEN_X = 800
    SCREEN_Y = 600

    mode = 1

    def __init__(self, title='Pyglet App'):
        super(Window, self).__init__(self.SCREEN_X, self.SCREEN_Y, title)

        # Populate star list
        for i in range(self.SMALL_STARS):
            s = M3DVector2f()
            s.x = rand() * self.SCREEN_X
            s.y = rand() * (self.SCREEN_Y - 100) + 100.0
            self.vSmallStars[i] = s
                
        # Populate star list
        for i in range(self.MEDIUM_STARS):
            s = M3DVector2f()
            s.x = rand() * self.SCREEN_X * 10 / 10.0
            s.y = rand() * (self.SCREEN_Y - 100) +100.0
            self.vMediumStars[i] = s

        # Populate star list
        for i in range(self.LARGE_STARS):
            s = M3DVector2f()
            s.x = rand() * self.SCREEN_X * 10 / 10.0
            s.y = rand() * (self.SCREEN_Y - 100) * 10.0 / 10.0 + 100.0
            self.vLargeStars[i] = s
                
                
        # Black background
        glClearColor(0.0, 0.0, 0.0, 1.0)

        # Set drawing color to white
        glColor3f(0.0, 0.0, 0.0)

    def on_draw(self):
        self.clear()

        x = 700.0     # Location and radius of moon
        y = 500.0
        r = 50.0
        angle = 0.0   # Another looping variable
             
        # Everything is white
        glColor3f(1.0, 1.0, 1.0)
        
        # Draw small stars
        glPointSize(1.0)
        glBegin(GL_POINTS)
        for i in range(self.SMALL_STARS):
            glVertex2f(*self.vSmallStars[i])
        glEnd()
            
        # Draw medium sized stars
        glPointSize(3.05)
        glBegin(GL_POINTS)
        for i in range(self.MEDIUM_STARS):
            glVertex2f(*self.vMediumStars[i])
        glEnd()
        
        # Draw largest stars
        glPointSize(5.5)
        glBegin(GL_POINTS)
        for i in range(self.LARGE_STARS):
            glVertex2f(*self.vLargeStars[i])
        glEnd()
        
        # Draw the "moon"
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(x, y)
        angle = 0.0
        while angle < 2.0 * 3.141592:
            glVertex2f(x+cos(angle)*r, y+sin(angle)*r)
            glVertex2f(x+r, y)
            angle += 0.1
        glEnd()

        # Draw distant horizon
        glLineWidth(3.5)
        glBegin(GL_LINE_STRIP)
        glVertex2f(0.0, 25.0)
        glVertex2f(50.0, 100.0)
        glVertex2f(100.0, 25.0)
        glVertex2f(225.0, 125.0)
        glVertex2f(300.0, 50.0)
        glVertex2f(375.0, 100.0)
        glVertex2f(460.0, 25.0)
        glVertex2f(525.0, 100.0)
        glVertex2f(600.0, 20.0)
        glVertex2f(675.0, 70.0)
        glVertex2f(750.0, 25.0)
        glVertex2f(800.0, 90.0)    
        glEnd()

    def _update_mode(self):
        if self.mode == 0:
            # Turn on antialiasing, and give hint to do the best
            # job possible.
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glEnable(GL_BLEND)
            glEnable(GL_POINT_SMOOTH)
            glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
            glEnable(GL_LINE_SMOOTH)
            glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
            glEnable(GL_POLYGON_SMOOTH)
            glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
        else:
            # Turn off blending and all smoothing
            glDisable(GL_BLEND)
            glDisable(GL_LINE_SMOOTH)
            glDisable(GL_POINT_SMOOTH)
            glDisable(GL_POLYGON_SMOOTH)

    def on_resize(self, w, h):
        # Prevent a divide by zero
        if h == 0:
            h = 1

        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)

        # Reset projection matrix stack
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Establish clipping volume (left, right, bottom, top, near, far)
        gluOrtho2D(0.0, self.SCREEN_X, 0.0, self.SCREEN_Y)


        # Reset Model view matrix stack
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    
    def on_key_press(self, sym, mods):
        if sym == key.SPACE:
            self.mode += 1
            if self.mode > 1:
                self.mode = 0
            self._update_mode()
        else:
            super(Window, self).on_key_press(sym, mods)
    
    def on_close(self):
        super(Window, self).on_close()

if __name__ == '__main__':
    window = Window('Smoothing Out The Jaggies')
    pyglet.app.run()
