"""
// Pyramid.cpp
// Demonstrates Simple Texture Mapping
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

    # Textures
    image = None
    texture = None

    # GL display lists stored by name
    dlists = {}

    # Motion
    xRot = 0.0
    xTurn = 0.0
    yRot = 0.0
    yTurn = 0.0

    def __init__(self, w, h, title='Pyglet App'):
        super(Window, self).__init__(w, h, title)

        # Light values and coordinates
        whiteLight = gl_vec(GLfloat, 0.05, 0.05, 0.05, 1.0)
        sourceLight = gl_vec(GLfloat, 0.25, 0.25, 0.25, 1.0)
        lightPos = gl_vec(GLfloat, -10., 5.0, 5.0, 1.0)

        glEnable(GL_DEPTH_TEST) # Hidden surface removal
        glFrontFace(GL_CCW)     # Counter clock-wise polygons face out
        glEnable(GL_CULL_FACE)  # Do not calculate inside of jet

        # Enable lighting
        glEnable(GL_LIGHTING)

        # Setup and enable light 0
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, whiteLight)
        glLightfv(GL_LIGHT0, GL_AMBIENT, sourceLight)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, sourceLight)
        glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
        glEnable(GL_LIGHT0)

        # Enable color tracking
        glEnable(GL_COLOR_MATERIAL)
        
        # Set Material properties to follow glColor values
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

        # Black blue background
        glClearColor(0.0, 0.0, 0.0, 1.0)
        
        # Load texture
        self.image = pyglet.image.load('Stone.tga')
        self.texture = self.image.get_texture().id
        
        glEnable(GL_TEXTURE_2D);

        pyglet.clock.schedule_interval(self._update, 1.0/60.0)

    def _make_display_list(self, name, func):
        dlists = self.dlists
        dlists[name] = glGenLists(1)
        glNewList(dlists[name], GL_COMPILE)
        func()
        glEndList()
    
    def _call_display_list(self, name):
        glCallList(self.dlists[name])

    def on_draw(self):
        self.clear()

        vNormal = [0.0] * 3
        vCorners = [
            [0.0, .80, 0.0],    # Top           0
            [-0.5, 0.0, -.50],  # Back left     1
            [0.5, 0.0, -0.50],  # Back right    2
            [0.5, 0.0, 0.5],    # Front right   3
            [-0.5, 0.0, 0.5],   # Front left    4
        ]

        # Save the matrix state and do the rotations
        glPushMatrix()

        # Move object back and do in-place rotation
        glTranslatef(0.0, -0.25, -4.0)
        glRotatef(self.xRot, 1.0, 0.0, 0.0)
        glRotatef(self.yRot, 0.0, 1.0, 0.0)

        # Draw the Pyramid
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_TRIANGLES)
        # Bottom section - two triangles
        glNormal3f(0.0, -1.0, 0.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3fv(vCorners[2])
        
        glTexCoord2f(0.0, 0.0)
        glVertex3fv(vCorners[4])
        
        glTexCoord2f(0.0, 1.0)
        glVertex3fv(vCorners[1])
        
        
        glTexCoord2f(1.0, 1.0)
        glVertex3fv(vCorners[2])
        
        glTexCoord2f(1.0, 0.0)
        glVertex3fv(vCorners[3])
        
        glTexCoord2f(0.0, 0.0)
        glVertex3fv(vCorners[4])
        
        # Front Face
        m3dFindNormal(vNormal, vCorners[0], vCorners[4], vCorners[3])
        glNormal3fv(vNormal)
        glTexCoord2f(0.5, 1.0)
        glVertex3fv(vCorners[0])
        glTexCoord2f(0.0, 0.0)
        glVertex3fv(vCorners[4])
        glTexCoord2f(1.0, 0.0)
        glVertex3fv(vCorners[3])
        
        # Left Face
        m3dFindNormal(vNormal, vCorners[0], vCorners[1], vCorners[4])
        glNormal3fv(vNormal)
        glTexCoord2f(0.5, 1.0)
        glVertex3fv(vCorners[0])
        glTexCoord2f(0.0, 0.0)
        glVertex3fv(vCorners[1])
        glTexCoord2f(1.0, 0.0)
        glVertex3fv(vCorners[4])

        # Back Face
        m3dFindNormal(vNormal, vCorners[0], vCorners[2], vCorners[1])
        glNormal3fv(vNormal)
        glTexCoord2f(0.5, 1.0)
        glVertex3fv(vCorners[0])
        
        glTexCoord2f(0.0, 0.0)
        glVertex3fv(vCorners[2])
        
        glTexCoord2f(1.0, 0.0)
        glVertex3fv(vCorners[1])
        
        # Right Face
        m3dFindNormal(vNormal, vCorners[0], vCorners[3], vCorners[2])
        glNormal3fv(vNormal)
        glTexCoord2f(0.5, 1.0)
        glVertex3fv(vCorners[0])
        glTexCoord2f(0.0, 0.0)
        glVertex3fv(vCorners[3])
        glTexCoord2f(1.0, 0.0)
        glVertex3fv(vCorners[2])
        glEnd()
    
        # Restore the matrix state
        glPopMatrix()

    def _update(self, dt):
        if self.xTurn != 0.0:
            self.xRot = (self.xRot + self.xTurn) % 360.0
        if self.yTurn != 0.0:
            self.yRot = (self.yRot + self.yTurn) % 360.0

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
        gluPerspective(35.0, fAspect, 1.0, 40.0)
            
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    
    def on_key_press(self, sym, mods):
        if sym == key.UP:
            self.xTurn = -5.0
        elif sym == key.DOWN:
            self.xTurn = 5.0
        elif sym == key.LEFT:
            self.yTurn = -5.0
        elif sym == key.RIGHT:
            self.yTurn = 5.0
        else:
            super(Window, self).on_key_press(sym, mods)
    
    def on_key_release(self, sym, mods):
        if sym == key.UP:
            self.xTurn = 0.0
        elif sym == key.DOWN:
            self.xTurn = 0.0
        elif sym == key.LEFT:
            self.yTurn = 0.0
        elif sym == key.RIGHT:
            self.yTurn = 0.0

    def on_close(self):
        pyglet.clock.unschedule(self._update)
        super(Window, self).on_close()


if __name__ == '__main__':
    window = Window(800, 600, 'Textured Pyramid')
    pyglet.app.run()
