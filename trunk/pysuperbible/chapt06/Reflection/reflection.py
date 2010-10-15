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

    # Light and material Data
    fLightPos = [-100.0, 100.0, 50.0, 1.0]  # Point source
    fLightPosMirror = [-100.0, -100.0, 50.0, 1.0]
    fNoLight = [0.0, 0.0, 0.0, 0.0]
    fLowLight = [0.25, 0.25, 0.25, 1.0]
    fBrightLight = [1.0, 1.0, 1.0, 1.0]

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
        
        self._make_display_lists()

        pyglet.clock.schedule_interval(self._update, 1.0/60.0)

    def _make_display_lists(self):
        dlists = self.dlists
        dlists['sphere'] = glGenLists(1)
        glNewList(dlists['sphere'], GL_COMPILE)
        glutSolidSphere(0.1, 17, 9)
        glEndList()

        dlists['torus'] = glGenLists(1)
        glNewList(dlists['torus'], GL_COMPILE)
        gltDrawTorus(0.35, 0.15, 61, 37)
        glEndList()

        dlists['ground'] = glGenLists(1)
        glNewList(dlists['ground'], GL_COMPILE)
        self._draw_ground()
        glEndList()

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
        glCallList(self.dlists['ground'])
        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)
        
        # Restore correct lighting and draw the world correctly
        glLightfv(GL_LIGHT0, GL_POSITION, self.fLightPos)
        self._draw_world()
        glPopMatrix()

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
        glCallList(self.dlists['sphere'])
        glPopMatrix()

        glRotatef(self.yRot, 0.0, 1.0, 0.0)
#        gltDrawTorus(0.35, 0.15, 61, 37)
        glCallList(self.dlists['torus'])

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
