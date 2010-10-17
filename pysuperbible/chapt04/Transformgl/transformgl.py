"""
// Transformgl.c
// OpenGL SuperBible
// Demonstrates letting OpenGL do the transformations
// Program by Richard S. Wright Jr.
## Pythonated for Pyglet by Gummbum
"""


import sys

import pyglet
from pyglet.gl import *

sys.path.append('../../lib')
from math3d import *
from gltools import *


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

    yRot = 0.0

    def __init__(self, w, h, title='Pyglet app'):
        super(Window, self).__init__(w, h, title)
        
        # Bluish background
        glClearColor(0.0, 0.0, 0.50, 1.0 )
             
        # Draw everything as wire frame
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        
        pyglet.clock.schedule_interval(self._update, 1.0/60.0)

    def _update(self, *args):
        # Rotation angle for animation
        self.yRot = (self.yRot + 0.5) % 360.0
    
    def on_draw(self):
        self.clear()

        rotationMatrix = M3DMatrix44f()
        translationMatrix = M3DMatrix44f()
        transformationMatrix = M3DMatrix44f()

        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
        # Build a rotation matrix
        m3dRotationMatrix44(
            transformationMatrix, m3dDegToRad(self.yRot), 0.0, 1.0, 0.0)
        transformationMatrix[12] = 0.0
        transformationMatrix[13] = 0.0
        transformationMatrix[14] = -2.5
            
        glLoadMatrixf(gl_vec(GLfloat, transformationMatrix[:]))

        gltDrawTorus(0.35, 0.15, 40, 20)

    def on_resize(self, w, h):
        # Prevent a divide by zero, when window is too short
        # (you cant make a window of zero width).
        if h == 0:
            h = 1

        glViewport(0, 0, w, h)
            
        fAspect = w / h

        # Reset the coordinate system before modifying
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        # Set the clipping volume
        gluPerspective(35.0, fAspect, 1.0, 50.0)
            
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def on_close(self):
        pyglet.clock.unschedule(self._update)
        super(Window, self).on_close()


if __name__ == '__main__':
    window = Window(800, 600, 'OpenGL Transformations Demo')
    pyglet.app.run()
