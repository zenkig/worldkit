"""
// Toon.cpp
// OpenGL SuperBible
// Demonstrates Cell/Toon shading with a 1D texture
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
from glframe import GLFrame


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

    # Rotation angle
    yRot = 0.0

    # Vector pointing towards the light
    vLightDir = [-1.0, 1.0, 1.0]

    def __init__(self, w, h, title='Pyglet App'):
        super(Window, self).__init__(w, h, title)

        # Load a 1D texture with toon shaded values
        # Green, greener...
        toonTable = [
            [0, 32, 0],
            [0, 64, 0],
            [0, 128, 0],
            [0, 192, 0],
        ]

        # Bluish background
        glClearColor(0.0, 0.0, .50, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
            
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage1D(GL_TEXTURE_1D, 0, GL_RGB, 4, 0, GL_RGB, GL_UNSIGNED_BYTE, toonTable)
        
        glEnable(GL_TEXTURE_1D)

        pyglet.clock.schedule_interval(self._update, 1.0/60.0)

    def on_draw(self):
        self.clear()

        glPushMatrix()
        glTranslatef(0.0, 0.0, -2.5)
        glRotatef(self.yRot, 0.0, 1.0, 0.0)
        self.toonDrawTorus(0.35, 0.15, 50, 25, self.vLightDir)
        glPopMatrix()
        
        # Rotate 1/2 degree more each frame
        self.yRot = (self.yRot + 0.5) % 360.0

    def toonDrawTorus(self, majorRadius, minorRadius,  numMajor, numMinor, vLightDir):
        # Draw a torus (doughnut), using the current 1D texture for light shading
        mInvertedLight = M3DMatrix44f()
        vNewLight = M3DVector3f()
        vNormal = M3DVector3f()
        majorStep = 2.0*M3D_PI / numMajor
        minorStep = 2.0*M3D_PI / numMinor

        # Get the modelview matrix
        mModelViewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    
        # Instead of transforming every normal and then dotting it with
        # the light vector, we will transform the light into object 
        # space by multiplying it by the inverse of the modelview matrix
## IMPASSE: m3dInvertMatrix44 using array pointer math. Too complicated
## to want to pursue right now. Anyway, possibly a job for numpy.
        m3dInvertMatrix44(mInvertedLight, mModelViewMatrix)
        m3dTransformVector3(vNewLight, vLightDir, mInvertedLight)
        vNewLight[0] -= mInvertedLight[12]
        vNewLight[1] -= mInvertedLight[13]
        vNewLight[2] -= mInvertedLight[14]
        m3dNormalizeVector(vNewLight)
    
        # Draw torus as a series of triangle strips
        for i in range(numMajor):
            a0 = i * majorStep
            a1 = a0 + majorStep
            x0 = cos(a0)
            y0 = sin(a0)
            x1 = cos(a1)
            y1 = sin(a1)

            glBegin(GL_TRIANGLE_STRIP)
            for j in range(numMinor+1):
                b = j * minorStep
                c = cos(b)
                r = minorRadius * c + majorRadius
                z = minorRadius * sin(b)

                # First point
                vNormal[0] = x0*c
                vNormal[1] = y0*c
                vNormal[2] = z/minorRadius
                m3dNormalizeVector(vNormal)
                
                # Texture coordinate is set by intensity of light
                glTexCoord1f(m3dDotProduct(vNewLight, vNormal))
                glVertex3f(x0*r, y0*r, z)

                # Second point
                vNormal[0] = x1*c
                vNormal[1] = y1*c
                vNormal[2] = z/minorRadius
                m3dNormalizeVector(vNormal)
                
                # Texture coordinate is set by intensity of light
                glTexCoord1f(m3dDotProduct(vNewLight, vNormal))
                glVertex3f(x1*r, y1*r, z)
            glEnd()

    def _update(self, dt):
        pass

    def on_resize(self, w, h):
        # Prevent a divide by zero, when window is too short
        # (you cant make a window of zero width).
        if h == 0:
                h = 1;

        glViewport(0, 0, w, h)
            
        fAspect = w / h

        # Reset the coordinate system before modifying
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        # Set the clipping volume
        gluPerspective(35.0, fAspect, 1.0, 50.0)
            
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    
    def on_key_press(self, sym, mods):
        super(Window, self).on_key_press(sym, mods)
    
    def on_close(self):
        pyglet.clock.unschedule(self._update)
        super(Window, self).on_close()


if __name__ == '__main__':
    window = Window(800, 600, 'Toon/Cell Shading Demo')
    pyglet.app.run()
