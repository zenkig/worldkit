"""
// Fogged.cpp
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

    # GL frame objects
    NUM_SPHERES = 30
    spheres = [None] * NUM_SPHERES
    frameCamera = GLFrame()
    
    # Rotation angle for animation
    yRot = 0.0
    
    # Movement
    forward = 0.0
    turn = 0.0
    right = 0.0
    
    # GL display lists for shapes
    dlists = {}
    
    # Light and material Data
    fLightPos = M3DVector4f(-100.0, 100.0, 50.0, 1.0)    # Point source
    fNoLight = M3DVector4f(0.0, 0.0, 0.0, 0.0)
    fLowLight = M3DVector4f(0.25, 0.25, 0.25, 1.0)
    fBrightLight = M3DVector4f(1.0, 1.0, 1.0, 1.0)
    
    # Shadow
    mShadowMatrix = M3DMatrix44f()

    def __init__(self, w, h, title='Pyglet App'):
        super(Window, self).__init__(w, h, title)
        
        # Calculate shadow matrix
        vPoints = [
            M3DVector3f(0.0, -0.4, 0.0),
            M3DVector3f(10.0, -0.4, 0.0),
            M3DVector3f(5.0, -0.4, -5.0),
        ]
        
        # Grayish background
        glClearColor(*self.fLowLight)

        # Setup Fog parameters
        glEnable(GL_FOG)                            # Turn Fog on
        glFogfv(GL_FOG_COLOR, self.fLowLight[:])    # Set fog color to match background
        glFogf(GL_FOG_START, 5.0)                   # How far away does the fog start
        glFogf(GL_FOG_END, 30.0)                    # How far away does the fog stop
        glFogi(GL_FOG_MODE, GL_LINEAR)              # Which fog equation do I use?

        # Cull backs of polygons
        glCullFace(GL_BACK)
        glFrontFace(GL_CCW)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        
        # Setup light parameters
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, vecf(self.fNoLight))
        glLightfv(GL_LIGHT0, GL_AMBIENT, vecf(self.fLowLight))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, vecf(self.fBrightLight))
        glLightfv(GL_LIGHT0, GL_SPECULAR, vecf(self.fBrightLight))
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        # Get the plane equation from three points on the ground
        vPlaneEquation = M3DVector4f()
        m3dGetPlaneEquation(vPlaneEquation, vPoints[0], vPoints[1], vPoints[2])

        # Calculate projection matrix to draw shadow on the ground
        m3dMakePlanarShadowMatrix(self.mShadowMatrix, vPlaneEquation, self.fLightPos)

        # Mostly use material tracking
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        glMateriali(GL_FRONT, GL_SHININESS, 128)
            
        # Randomly place the sphere inhabitants
        for iSphere in range(self.NUM_SPHERES):
            # Pick a random location between -20 and 20 at .1 increments
            s = GLFrame()
            x = rand() * 40 - 20
            z = rand() * 40 - 20
            s.SetOrigin(x, 0.0, z)
            self.spheres[iSphere] = s

        pyglet.clock.schedule_interval(self._update, 1.0/60.0)
        pyglet.clock.schedule_interval(self.fps, 2.0)
        
        self._make_display_lists()

    def fps(self, *args):
        print 'fps',pyglet.clock.get_fps()
    
    def _make_display_lists(self):
        dlists = self.dlists
        dlists['big sphere'] = glGenLists(1)
        glNewList(dlists['big sphere'], GL_COMPILE)
        glutSolidSphere(0.3, 17, 9)
        glEndList()

        dlists = self.dlists
        dlists['small sphere'] = glGenLists(1)
        glNewList(dlists['small sphere'], GL_COMPILE)
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
        self.frameCamera.ApplyCameraTransform()
        
        # Position light before any other transformations
        glLightfv(GL_LIGHT0, GL_POSITION, self.fLightPos[:])
        
        # Draw the ground
        glColor3f(0.60, .40, .10)
#        self._draw_ground()
        glCallList(self.dlists['ground'])
        
        # Draw shadows first
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glPushMatrix()
        glMultMatrixf(self.mShadowMatrix[:])
        self._draw_inhabitants(1)
        glPopMatrix()
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)
        
        # Draw inhabitants normally
        self._draw_inhabitants(0)

        glPopMatrix()

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
            glCallList(self.dlists['big sphere'])
            glPopMatrix()

        glPushMatrix()
        glTranslatef(0.0, 0.1, -2.5)
    
        if nShadow == 0:
            glColor3f(0.0, 0.0, 1.0)

        glPushMatrix()
        glRotatef(-self.yRot * 2.0, 0.0, 1.0, 0.0)
        glTranslatef(1.0, 0.0, 0.0)
#        glutSolidSphere(0.1, 17, 9)
        glCallList(self.dlists['small sphere'])
        glPopMatrix()
    
        if nShadow == 0:
            # Torus alone will be specular
            glColor3f(1.0, 0.0, 0.0)
            glMaterialfv(GL_FRONT, GL_SPECULAR, self.fBrightLight[:])
        
        glRotatef(self.yRot, 0.0, 1.0, 0.0)
#        gltDrawTorus(0.35, 0.15, 61, 37)
        glCallList(self.dlists['torus'])
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.fNoLight[:])
        glPopMatrix()

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
    window = Window(800, 600, 'OpenGL SphereWorld Demo + Lights and Shadow')
    pyglet.app.run()
