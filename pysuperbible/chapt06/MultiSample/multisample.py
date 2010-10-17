"""
// multisample.cpp
// OpenGL SuperBible
// Demonstrates an immersive 3D environment using actors
// and a camera. This version adds lights and material properties
// and shadows.
// Program by Richard S. Wright Jr.
## Pythonated for Pyglet by Gummbum
"""


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

    # GL frame objects
    NUM_SPHERES = 50
    spheres = [None] * NUM_SPHERES
    frameCamera = GLFrame()

    # Light and material Data
    fLightPos   = gl_vec(GLfloat, -100.0, 100.0, 50.0, 1.0)    # Point source
    fNoLight = gl_vec(GLfloat, 0.0, 0.0, 0.0, 0.0)
    fLowLight = gl_vec(GLfloat, 0.25, 0.25, 0.25, 1.0)
    fBrightLight = gl_vec(GLfloat, 1.0, 1.0, 1.0, 1.0)

    mShadowMatrix = [0.0] * 16

    # Rotation angle for animation
    yRot = 0.0
    
    # Movement
    forward = 0.0
    turn = 0.0
    right = 0.0
    
    # GL display lists for shapes
    dlists = {}

    def __init__(self, w, h, title='Pyglet App'):
        super(Window, self).__init__(w, h, title)

        # Grayish background
        glClearColor(*self.fLowLight)
             
        # Cull backs of polygons
        glCullFace(GL_BACK);
        glFrontFace(GL_CCW);
        glEnable(GL_CULL_FACE);
        glEnable(GL_DEPTH_TEST);
        
        # Setup light parameters
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, self.fNoLight);
        glLightfv(GL_LIGHT0, GL_AMBIENT, self.fLowLight);
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.fBrightLight);
        glLightfv(GL_LIGHT0, GL_SPECULAR, self.fBrightLight);
        glEnable(GL_LIGHTING);
        glEnable(GL_LIGHT0);

        # Calculate shadow matrix
        vPoints = [
            [0.0, -0.4, 0.0],
            [10.0, -0.4, 0.0],
            [5.0, -0.4, -5.0],
        ]
        
        # Get the plane equation from three points on the ground
        vPlaneEquation = M3DVector4f()
        m3dGetPlaneEquation(vPlaneEquation, vPoints[0], vPoints[1], vPoints[2]);

        # Calculate projection matrix to draw shadow on the ground
        m3dMakePlanarShadowMatrix(self.mShadowMatrix, vPlaneEquation, self.fLightPos)
        self.mShadowMatrix = gl_vec(GLfloat, self.mShadowMatrix)

        # Mostly use material tracking
        glEnable(GL_COLOR_MATERIAL);
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE);
        glMateriali(GL_FRONT, GL_SHININESS, 128);
            
        # Randomly place the sphere inhabitants
        for iSphere in range(self.NUM_SPHERES):
            # Pick a random location between -20 and 20 at .1 increments
            s = GLFrame()
            x = rand() * 40 - 20
            z = rand() * 40 - 20
            s.SetOrigin(x, 0.0, z)
            self.spheres[iSphere] = s

        glEnable(GL_MULTISAMPLE)  # This is actually on by default

        self._make_display_list('small sphere', self._draw_small_sphere)
        self._make_display_list('big sphere', self._draw_big_sphere)
        self._make_display_list('torus', self._draw_torus)
        self._make_display_list('ground', self._draw_ground)

        pyglet.clock.schedule_interval(self._update, 1.0/60.0)
        pyglet.clock.schedule_interval(self.fps, 2.0)
        
    def fps(self, *args):
        print 'fps',pyglet.clock.get_fps()

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
        self.frameCamera.ApplyCameraTransform()
        
        # Position light before any other transformations
        glLightfv(GL_LIGHT0, GL_POSITION, self.fLightPos)
        
        # Draw the ground
        glColor3f(0.60, .40, .10)
#        self._draw_ground()
        self._call_display_list('ground')
        
        # Draw shadows first
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glPushMatrix()
        glMultMatrixf(self.mShadowMatrix)
        self._draw_inhabitants(1)
        glPopMatrix()
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)
        
        # Draw inhabitants normally
        self._draw_inhabitants(0)

        glPopMatrix()

    def _draw_inhabitants(self, nShadow):
        # Draw random inhabitants and the rotating torus/sphere duo

        # Draw the randomly located spheres
        if nShadow == 0:
            glColor3f(0.0, 1.0, 0.0)
        else:
            glColor3f(0.0, 0.0, 0.0)

        for i in range(self.NUM_SPHERES):
            glPushMatrix()
            self.spheres[i].ApplyActorTransform()
#            glutSolidSphere(0.3, 17, 9)
            self._call_display_list('big sphere')
            glPopMatrix()

        glPushMatrix()
        glTranslatef(0.0, 0.1, -2.5)
    
        if nShadow == 0:
            glColor3f(0.0, 0.0, 1.0)

        glPushMatrix()
        glRotatef(-self.yRot * 2.0, 0.0, 1.0, 0.0)
        glTranslatef(1.0, 0.0, 0.0)
#        glutSolidSphere(0.1, 17, 9)
        self._call_display_list('small sphere')
        glPopMatrix()
    
        if nShadow == 0:
            # Torus alone will be specular
            glColor3f(1.0, 0.0, 0.0)
            glMaterialfv(GL_FRONT, GL_SPECULAR, self.fBrightLight)
        
        glRotatef(self.yRot, 0.0, 1.0, 0.0)
#        gltDrawTorus(0.35, 0.15, 61, 37)
        self._call_display_list('torus')
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.fNoLight)
        glPopMatrix()

    def _draw_small_sphere(self):
        glutSolidSphere(0.1, 17, 9)

    def _draw_big_sphere(self):
        glutSolidSphere(0.3, 17, 9)

    def _draw_torus(self):
        gltDrawTorus(0.35, 0.15, 61, 37)

    def _draw_ground(self):
        # Draw the ground as a series of triangle strips
        fExtent = 20.0
        fStep = 1.0
        y = -0.4
        
        iStrip = -fExtent
        while iStrip <= fExtent:
            glBegin(GL_TRIANGLE_STRIP)
            glNormal3f(0.0, 1.0, 0.0)   # All Point up
            iRun = fExtent
            while iRun >= -fExtent:
                glVertex3f(iStrip, y, iRun)
                glVertex3f(iStrip + fStep, y, iRun)
                iRun -= fStep
            glEnd()
            iStrip += fStep

    def _update(self, dt):
        self.yRot = (self.yRot + 2.0) % 360.0
        if self.forward != 0.0:
            self.frameCamera.MoveForward(self.forward*2.0)
        if self.turn != 0.0:
            self.frameCamera.RotateLocalY(self.turn)
        if self.right != 0.0:
            self.frameCamera.MoveRight(self.right)

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
    
    def on_key_press(self, sym, mods):
        if sym in (key.UP,key.W):
            self.forward = 0.075
        elif sym in (key.DOWN,key.S):
            self.forward = -0.075
        elif sym in (key.LEFT,key.A):
            self.turn = 0.075
        elif sym in (key.RIGHT,key.D):
            self.turn = -0.075
        elif sym == key.Q:
            self.right = 0.1
        elif sym == key.E:
            self.right = -0.1
        else:
            super(Window, self).on_key_press(sym, mods)
    
    def on_key_release(self, sym, mods):
        if sym in (key.UP,key.W):
            self.forward = 0.0
        elif sym in (key.DOWN,key.S):
            self.forward = 0.0
        elif sym in (key.LEFT,key.A):
            self.turn = 0.0
        elif sym in (key.RIGHT,key.D):
            self.turn = 0.0
        elif sym == key.Q:
            self.right = 0.0
        elif sym == key.E:
            self.right = 0.0
    
    def on_close(self):
        pyglet.clock.unschedule(self._update)
        pyglet.clock.unschedule(self.fps)
        super(Window, self).on_close()

if __name__ == '__main__':
    window = Window(800, 600, 'OpenGL SphereWorld Demo Multisamples')
    pyglet.app.run()
