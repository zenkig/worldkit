"""
// Reflection.cpp
// OpenGL SuperBible
// Demonstrates using blending/transparency
// Program by Richard S. Wright Jr.
## Pythonated for Pyglet by Gummbum
## Added glut objects in display lists for speed.
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

    # Light and material Data
    fLightPos = gl_vec(GLfloat, -100.0, 100.0, 50.0, 1.0)  # Point source
    fLightPosMirror = gl_vec(GLfloat, -100.0, -100.0, 50.0, 1.0)
    fNoLight = gl_vec(GLfloat, 0.0, 0.0, 0.0, 0.0)
    fLowLight = gl_vec(GLfloat, 0.25, 0.25, 0.25, 1.0)
    fBrightLight = gl_vec(GLfloat, 1.0, 1.0, 1.0, 1.0)

    # GL display lists for shapes
    dlists = {}

    yRot = 0.0

    def __init__(self, w, h, title='Pyglet App'):
        super(Window, self).__init__(w, h, title)

        # Grayish background
        glClearColor(*self.fLowLight)
       
        # Cull backs of polygons
        glCullFace(GL_BACK)
        glFrontFace(GL_CCW)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        
        # Setup light parameters
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, self.fNoLight)
        glLightfv(GL_LIGHT0, GL_AMBIENT, self.fLowLight)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.fBrightLight)
        glLightfv(GL_LIGHT0, GL_SPECULAR, self.fBrightLight)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
         
        # Mostly use material tracking
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        glMateriali(GL_FRONT, GL_SHININESS, 128)
        
        self._make_display_list('sphere', self._draw_sphere)
        self._make_display_list('torus', self._draw_torus)
        self._make_display_list('ground', self._draw_ground)

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

        glPushMatrix()
        # Move light under floor to light the "reflected" world
        glLightfv(GL_LIGHT0, GL_POSITION, self.fLightPosMirror)
        glPushMatrix()
        glFrontFace(GL_CW)             # geometry is mirrored, swap orientation
        glScalef(1.0, -1.0, 1.0)
        self._draw_world()
        glFrontFace(GL_CCW)
        glPopMatrix()
    
        # Draw the ground transparently over the reflection
        glDisable(GL_LIGHTING)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
#        self._draw_ground()
        self._call_display_list('ground')
        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)
        
        # Restore correct lighting and draw the world correctly
        glLightfv(GL_LIGHT0, GL_POSITION, self.fLightPos)
        self._draw_world()
        glPopMatrix()

    def _draw_sphere(self):
        glutSolidSphere(0.1, 17, 9)

    def _draw_torus(self):
        gltDrawTorus(0.35, 0.15, 61, 37)
    
    def _draw_ground(self):
        fExtent = 20.0
        fStep = 0.5
        y = 0.0
        iBounce = 0
        
        glShadeModel(GL_FLAT)
        iStrip = -fExtent
        while iStrip <= fExtent:
            glBegin(GL_TRIANGLE_STRIP)
            iRun = fExtent
            while iRun >= -fExtent:
                if iBounce % 2 == 0:
                    fColor = 1.0
                else:
                    fColor = 0.0
                glColor4f(fColor, fColor, fColor, 0.5)
                glVertex3f(iStrip, y, iRun)
                glVertex3f(iStrip+fStep, y, iRun)
                iBounce += 1
                iRun -= fStep
            glEnd()
            iStrip += fStep
        glShadeModel(GL_SMOOTH)

    def _draw_world(self):
        glColor3f(1.0, 0.0, 0.0)
        glPushMatrix()
        glTranslatef(0.0, 0.5, -3.5)
    
        glPushMatrix()
        glRotatef(-self.yRot*2.0, 0.0, 1.0, 0.0)
        glTranslatef(1.0, 0.0, 0.0)
#        glutSolidSphere(0.1, 17, 9)
        self._call_display_list('sphere')
        glPopMatrix()

        glRotatef(self.yRot, 0.0, 1.0, 0.0)
#        gltDrawTorus(0.35, 0.15, 61, 37)
        self._call_display_list('torus')

        glPopMatrix()

    def _update(self, dt):
        self.yRot = (self.yRot + 1.0) % 360.0   # Update Rotation

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
        glTranslatef(0.0, -0.4, 0.0)
    
    def on_key_press(self, sym, mods):
        super(Window, self).on_key_press(sym, mods)
    
    def on_close(self):
        pyglet.clock.unschedule(self._update)
        super(Window, self).on_close()

if __name__ == '__main__':
    window = Window(800, 600, 'OpenGL Blending and Transparency')
    pyglet.app.run()
