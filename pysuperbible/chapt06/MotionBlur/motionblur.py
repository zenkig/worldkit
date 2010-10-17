"""
// MotionBlur.cpp
// OpenGL SuperBible
// Demonstrates Motion Blur with the Accumulation buffer
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

    yRot = 45.0
    
    # Light and material Data
    fLightPos = gl_vec(GLfloat, -100.0, 100.0, 50.0, 1.0)   # Point source
    fLightPosMirror = gl_vec(GLfloat, -100.0, -100.0, 50.0, 1.0)
    fNoLight = gl_vec(GLfloat, 0.0, 0.0, 0.0, 0.0)
    fLowLight = gl_vec(GLfloat, 0.25, 0.25, 0.25, 1.0)
    fBrightLight = gl_vec(GLfloat, 1.0, 1.0, 1.0, 1.0)

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
        glLightfv(GL_LIGHT0, GL_POSITION, self.fLightPos)
        
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
         
        # Mostly use material tracking
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        glMateriali(GL_FRONT, GL_SHININESS, 128)

        pyglet.clock.schedule_interval(self._update, 1.0/60.0)

    def on_draw(self):
        self.clear()
        
        fPasses = 10
        
        # Set the current rotation back a few degrees
        self.yRot = 35.0
                
        for fPass in range(fPasses):
            self.yRot += 1.0 / (fPass+1.0)
           
            # Draw sphere
            self._draw_geometry()
            
            # Accumulate to back buffer
            if fPass == 0.0:
                glAccum(GL_LOAD, 0.5)
            else:
                glAccum(GL_ACCUM, 0.5 * (1.0 / fPasses))

        # copy accumulation buffer to color buffer and
        # do the buffer Swap
        glAccum(GL_RETURN, 1.0)

    def _draw_geometry(self):
        self.clear()
        
        glPushMatrix()
        self._draw_ground()
        
        # Place the moving sphere
        glColor3f(1.0, 0.0, 0.0)
        glTranslatef(0.0, 0.5, -3.5)
        glRotatef(-(self.yRot * 2.0), 0.0, 1.0, 0.0)
        glTranslatef(1.0, 0.0, 0.0)
        glutSolidSphere(0.1, 17, 9)
        glPopMatrix()

    def _draw_ground(self):
        # Draw the ground as a series of triangle strips. The 
        # shading model and colors are set such that we end up 
        # with a black and white checkerboard pattern.
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
                glVertex3f(iStrip + fStep, y, iRun)
                iBounce += 1
                iRun -= fStep
            glEnd()
            iStrip += fStep
        glShadeModel(GL_SMOOTH)

    def _update(self, dt):
        pass

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
    window = Window(800, 600, 'Motion Blur with the Accumulation Buffer')
    pyglet.app.run()
