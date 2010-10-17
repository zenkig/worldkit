"""
// SphereWorld.cpp
// OpenGL SuperBible
// Demonstrates an immersive 3D environment using actors
// and a camera.
// Program by Richard S. Wright Jr.
## Pythonated for Pyglet by Gummbum
## Added glut objects in display lists for speed.
## Added QWASDE keys to turn/move/strafe.
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


class Window(pyglet.window.Window):

    # GL frame objects
    NUM_SPHERES = 50
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

    def __init__(self, w, h, title='Pyglet App'):
        super(Window, self).__init__(w, h, title)

        # Bluish background
        glClearColor(0.0, 0.0, .50, 1.0)
             
        # Draw everything as wire frame
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        
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
        dlists['sphere'] = glGenLists(1)
        glNewList(dlists['sphere'], GL_COMPILE)
        glutSolidSphere(0.1, 13, 26)
        glEndList()

        dlists['torus'] = glGenLists(1)
        glNewList(dlists['torus'], GL_COMPILE)
        gltDrawTorus(0.35, 0.15, 40, 20)
        glEndList()
    
        dlists['ground'] = glGenLists(1)
        glNewList(dlists['ground'], GL_COMPILE)
        DrawGround()
        glEndList()
    
    def on_draw(self, *args):
        self.clear()

        glPushMatrix()
        self.frameCamera.ApplyCameraTransform()
        
        # Draw the ground
#        DrawGround()
        glCallList(self.dlists['ground'])
        
        # Draw the randomly located spheres
        for i in range(self.NUM_SPHERES):
            glPushMatrix()
            self.rot_mat = self.spheres[i].ApplyActorTransform()
#            glutSolidSphere(0.1, 13, 4)
            glCallList(self.dlists['sphere'])
            glPopMatrix()

        glPushMatrix()
        glTranslatef(0.0, 0.0, -2.5)

        glPushMatrix()
        glRotatef(-self.yRot*2.0, 0.0, 1.0, 0.0)
        glTranslatef(1.0, 0.0, 0.0)
#        glutSolidSphere(0.1, 13, 4)
        glCallList(self.dlists['sphere'])
        glPopMatrix()

        glRotatef(self.yRot, 0.0, 1.0, 0.0)
#        gltDrawTorus(0.35, 0.15, 40, 4)
        glCallList(self.dlists['torus'])
        glPopMatrix()
        glPopMatrix()

    def _update(self, dt):
        self.yRot = (self.yRot + 0.5) % 360.0
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
            self.forward = 0.1
        elif sym in (key.DOWN,key.S):
            self.forward = -0.1
        elif sym in (key.LEFT,key.A):
            self.turn = 0.1
        elif sym in (key.RIGHT,key.D):
            self.turn = -0.1
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

def DrawGround():
    """Draw a gridded ground"""
    fExtent = 20
    fStep = 1
    y = -0.4
    
    glBegin(GL_LINES)
    for iLine in range(-fExtent, fExtent+1, fStep):
        glVertex3f(iLine, y, fExtent)    # Draw Z lines
        glVertex3f(iLine, y, -fExtent)
        glVertex3f(fExtent, y, iLine)
        glVertex3f(-fExtent, y, iLine)
    glEnd()


if __name__ == '__main__':
    window = Window(800, 600, 'OpenGL SphereWorld Demo')
    pyglet.app.run()
