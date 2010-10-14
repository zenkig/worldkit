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
            
        glLoadMatrixf(vecf(transformationMatrix))

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
