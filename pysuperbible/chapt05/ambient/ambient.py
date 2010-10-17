"""
// Ambient.cpp
// OpenGL SuperBible
// Beginning of OpenGL lighting sample
// Demonstrates Ambient Lighting
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

    # Rotation amounts
    xRot = 0.0
    yRot = 0.0

    def __init__(self, w, h, title='Pyglet App'):
        super(Window, self).__init__(w, h, title)

        # Light values
        # Bright white light
        ambientLight = gl_vec(GLfloat, 1.0, 1.0, 1.0, 1.0)

        glEnable(GL_DEPTH_TEST) # Hidden surface removal
        glEnable(GL_CULL_FACE)  # Do not calculate inside of jet
        glFrontFace(GL_CCW)     # Counter clock-wise polygons face out

        # Lighting stuff
        glEnable(GL_LIGHTING)   # Enable lighting	

        # Set light model to use ambient light specified by ambientLight
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambientLight)

        glEnable(GL_COLOR_MATERIAL) # Enable Material color tracking

        # Front material ambient and diffuse colors track glColor
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

        # Nice light blue
        glClearColor(0.0, 0.0, 1.0, 1.0)

        pyglet.clock.schedule_interval(self._update, 1.0/60.0)

    def on_draw(self):
        self.clear()

        # Save the matrix state
        glPushMatrix()
        glRotatef(self.xRot, 1.0, 0.0, 0.0)
        glRotatef(self.yRot, 0.0, 1.0, 0.0)

        # Nose Cone ##############
        # Bright Green
        glColor3ub(0, 255, 0)
        glBegin(GL_TRIANGLES)
        glVertex3f(0.0, 0.0, 60.0)
        glVertex3f(-15.0, 0.0, 30.0)
        glVertex3f(15.0, 0.0, 30.0)

        glVertex3f(15.0, 0.0, 30.0)
        glVertex3f(0.0, 15.0, 30.0)
        glVertex3f(0.0, 0.0, 60.0)

        glVertex3f(0.0, 0.0, 60.0)
        glVertex3f(0.0, 15.0, 30.0)
        glVertex3f(-15.0, 0.0, 30.0)

        # Body of the Plane ############
        # light gray
        glColor3ub(192,192,192)
        glVertex3f(-15.0, 0.0, 30.0)
        glVertex3f(0.0, 15.0, 30.0)
        glVertex3f(0.0, 0.0, -56.0)

        glVertex3f(0.0, 0.0, -56.0)
        glVertex3f(0.0, 15.0, 30.0)
        glVertex3f(15.0, 0.0, 30.0)	

        glVertex3f(15.0, 0.0, 30.0)
        glVertex3f(-15.0, 0.0, 30.0)
        glVertex3f(0.0, 0.0, -56.0)


        # ######################/
        # Left wing
        # Dark gray
        glColor3ub(64,64,64)
        glVertex3f(0.0, 2.0, 27.0)
        glVertex3f(-60.0, 2.0, -8.0)
        glVertex3f(60.0, 2.0, -8.0)

        glVertex3f(60.0, 2.0, -8.0)
        glVertex3f(0.0, 7.0, -8.0)
        glVertex3f(0.0, 2.0, 27.0)

        glVertex3f(60.0, 2.0, -8.0)
        glVertex3f(-60.0, 2.0, -8.0)
        glVertex3f(0.0, 7.0, -8.0)


        # Other wing top section
        glVertex3f(0.0, 2.0, 27.0)
        glVertex3f(0.0, 7.0, -8.0)
        glVertex3f(-60.0, 2.0, -8.0)

        # Tail section###############/
        # Bottom of back fin
        glColor3ub(255,255,0)
        glVertex3f(-30.0, -0.50, -57.0)
        glVertex3f(30.0, -0.50, -57.0)
        glVertex3f(0.0, -0.50, -40.0)

        # top of left side
        glVertex3f(0.0, -0.5, -40.0)
        glVertex3f(30.0, -0.5, -57.0)
        glVertex3f(0.0, 4.0, -57.0)

        # top of right side
        glVertex3f(0.0, 4.0, -57.0)
        glVertex3f(-30.0, -0.5, -57.0)
        glVertex3f(0.0, -0.5, -40.0)

        # back of bottom of tail
        glVertex3f(30.0, -0.5, -57.0)
        glVertex3f(-30.0, -0.5, -57.0)
        glVertex3f(0.0, 4.0, -57.0)


        # Top of Tail section left
        glColor3ub(255,0,0)
        glVertex3f(0.0, 0.5, -40.0)
        glVertex3f(3.0, 0.5, -57.0)
        glVertex3f(0.0, 25.0, -65.0)

        glVertex3f(0.0, 25.0, -65.0)
        glVertex3f(-3.0, 0.5, -57.0)
        glVertex3f(0.0, 0.5, -40.0)


        # Back of horizontal section
        glVertex3f(3.0, 0.5, -57.0)
        glVertex3f(-3.0, 0.5, -57.0)
        glVertex3f(0.0, 25.0, -65.0)
        glEnd()

        glPopMatrix()

    def _update(self, dt):
        pass

    def on_resize(self, w, h):
        nRange = 80.0
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
            self.xRot -= 5.0
        if sym == key.DOWN:
            self.xRot += 5.0
        if sym == key.LEFT:
            self.yRot -= 5.0
        if sym == key.RIGHT:
            self.yRot += 5.0
        else:
            super(Window, self).on_key_press(sym, mods)
    
        self.xRot %= 360.0
        self.yRot %= 360.0
    
    def on_close(self):
        pyglet.clock.unschedule(self._update)
        super(Window, self).on_close()

if __name__ == '__main__':
    window = Window(800, 600, 'Ambient Light Jet')
    pyglet.app.run()
