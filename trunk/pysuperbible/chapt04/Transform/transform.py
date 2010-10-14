"""
// Transform.cpp
// OpenGL SuperBible
// Demonstrates manual transformations
// Program by Richard S. Wright Jr.
## Pythonated for Pyglet by Gummbum
"""


from math import cos, sin
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

    # Rotation angle for animation
    yRot = 0.0

    def __init__(self, w, h, title='Pyglet App'):
        super(Window, self).__init__(w, h, title)

        # Bluish background
        glClearColor(0.0, 0.0, 0.50, 1.0)
             
        # Draw everything as wire frame
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        pyglet.clock.schedule_interval(self._update, 1.0/60.0)

    def on_draw(self):
        self.clear()

        transformationMatrix = M3DMatrix44f()   # Storage for rotation matrix
            
        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Build a rotation matrix
        m3dRotationMatrix44(
            transformationMatrix, m3dDegToRad(self.yRot), 0.0, 1.0, 0.0)
        transformationMatrix[12] = 0.0
        transformationMatrix[13] = 0.0
        transformationMatrix[14] = -2.5
            
        DrawTorus(transformationMatrix)

    def _update(self, dt):
        self.yRot = (self.yRot + 0.5) % 360.0
    
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


def DrawTorus(mTransform):
    """Draw a torus (doughnut), using the current 1D texture for light shading"""
    majorRadius = 0.35
    minorRadius = 0.15
    numMajor = 40
    numMinor = 20
    objectVertex = M3DVector3f()         # Vertex in object/eye space
    transformedVertex = M3DVector3f()    # New Transformed vertex   
    majorStep = 2.0*M3D_PI / numMajor
    minorStep = 2.0*M3D_PI / numMinor
    
    for i in range(numMajor):
        a0 = i * majorStep;
        a1 = a0 + majorStep;
        x0 = cos(a0)
        y0 = sin(a0)
        x1 = cos(a1)
        y1 = sin(a1)

        glBegin(GL_TRIANGLE_STRIP);
        for j in range(numMinor+1):
            b = j * minorStep
            c = cos(b)
            r = minorRadius * c + majorRadius
            z = minorRadius * sin(b)

            # First point
            objectVertex[0] = x0*r
            objectVertex[1] = y0*r
            objectVertex[2] = z
            m3dTransformVector3(transformedVertex, objectVertex, mTransform)
            glVertex3fv(vecf(transformedVertex))

            # Second point
            objectVertex[0] = x1*r
            objectVertex[1] = y1*r
            objectVertex[2] = z
            m3dTransformVector3(transformedVertex, objectVertex, mTransform)
            glVertex3fv(vecf(transformedVertex))
        glEnd()


if __name__ == '__main__':
    window = Window(800, 600, 'Manual Transformations Demo')
    pyglet.app.run()
