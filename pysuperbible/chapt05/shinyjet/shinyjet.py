"""
// ShinyJet.cpp
// OpenGL SuperBible
// Demonstrates OpenGL Lighting
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

    xRot = 0.0
    yRot = 0.0

    def __init__(self, w, h, title='Pyglet App'):
        super(Window, self).__init__(w, h, title)

        # Light values and coordinates
        ambientLight = [0.3, 0.3, 0.3, 1.0]
        diffuseLight = [0.7, 0.7, 0.7, 1.0]
        specular = [1.0, 1.0, 1.0, 1.0]
        specref = [1.0, 1.0, 1.0, 1.0]

        glEnable(GL_DEPTH_TEST) # Hidden surface removal
        glFrontFace(GL_CCW)     # Counter clock-wise polygons face out
        glEnable(GL_CULL_FACE)  # Do not calculate inside of jet

        # Enable lighting
        glEnable(GL_LIGHTING)

        # Setup and enable light 0
        glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLight)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLight)
        glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
        glEnable(GL_LIGHT0)

        # Enable color tracking
        glEnable(GL_COLOR_MATERIAL)
        
        # Set Material properties to follow glColor values
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

        # All materials hereafter have full specular reflectivity
        # with a high shine
        glMaterialfv(GL_FRONT, GL_SPECULAR, specref)
        glMateriali(GL_FRONT, GL_SHININESS, 128)
        
        # Light blue background
        glClearColor(0.0, 0.0, 1.0, 1.0)
        
        glEnable(GL_NORMALIZE)

        pyglet.clock.schedule_interval(self._update, 1.0/60.0)

    def on_draw(self):
        self.clear()

        vNormal = M3DVector3f()    # Storeage for calculated surface normal

        # Save the matrix state and do the rotations
        glPushMatrix()
        glRotatef(self.xRot, 1.0, 0.0, 0.0)
        glRotatef(self.yRot, 0.0, 1.0, 0.0)

        # Nose Cone - Points straight down
        # Set material color
        glColor3ub(128, 128, 128)
        glBegin(GL_TRIANGLES)
        glNormal3f(0.0, -1.0, 0.0)
        glNormal3f(0.0, -1.0, 0.0)
        glVertex3f(0.0, 0.0, 60.0)
        glVertex3f(-15.0, 0.0, 30.0)
        glVertex3f(15.0,0.0,30.0)
                
    
        # Verticies for this panel
        vPoints = [
            M3DVector3f(15.0, 0.0,  30.0),
            M3DVector3f(0.0,  15.0, 30.0),
            M3DVector3f(0.0,  0.0,  60.0),
        ]

        # Calculate the normal for the plane
        m3dFindNormal(vNormal, vPoints[0], vPoints[1], vPoints[2])
        glNormal3fv(list(vNormal))
        glVertex3f(*vPoints[0])
        glVertex3f(*vPoints[1])
        glVertex3f(*vPoints[2])

        vPoints = [
            M3DVector3f(0.0, 0.0, 60.0),
            M3DVector3f(0.0, 15.0, 30.0),
            M3DVector3f(-15.0, 0.0, 30.0),
        ]

        m3dFindNormal(vNormal, vPoints[0], vPoints[1], vPoints[2])
        glNormal3fv(list(vNormal))
        glVertex3f(*vPoints[0])
        glVertex3f(*vPoints[1])
        glVertex3f(*vPoints[2])

        # Body of the Plane ############
        vPoints = [
            M3DVector3f(-15.0, 0.0, 30.0),
            M3DVector3f(0.0, 15.0, 30.0),
            M3DVector3f(0.0, 0.0, -56.0),
        ]

        m3dFindNormal(vNormal, vPoints[0], vPoints[1], vPoints[2])
        glNormal3fv(list(vNormal))
        glVertex3f(*vPoints[0])
        glVertex3f(*vPoints[1])
        glVertex3f(*vPoints[2])
                    
        vPoints = [
            M3DVector3f(0.0, 0.0, -56.0),
            M3DVector3f(0.0, 15.0, 30.0),
            M3DVector3f(15.0, 0.0, 30.0),
        ]
    
        m3dFindNormal(vNormal, vPoints[0], vPoints[1], vPoints[2])
        glNormal3fv(list(vNormal))
        glVertex3f(*vPoints[0])
        glVertex3f(*vPoints[1])
        glVertex3f(*vPoints[2])
    
        glNormal3f(0.0, -1.0, 0.0)
        glVertex3f(15.0, 0.0, 30.0)
        glVertex3f(-15.0, 0.0, 30.0)
        glVertex3f(0.0, 0.0, -56.0)
    
        # ######################/
        # Left wing
        # Large triangle for bottom of wing
        vPoints = [
            M3DVector3f(0.0, 2.0, 27.0),
            M3DVector3f(-60.0, 2.0, -8.0),
            M3DVector3f(60.0, 2.0, -8.0),
        ]

        m3dFindNormal(vNormal, vPoints[0], vPoints[1], vPoints[2])
        glNormal3fv(list(vNormal))
        glVertex3f(*vPoints[0])
        glVertex3f(*vPoints[1])
        glVertex3f(*vPoints[2])

        vPoints = [
            M3DVector3f(60.0, 2.0, -8.0),
            M3DVector3f(0.0, 7.0, -8.0),
            M3DVector3f(0.0,2.0,27.0),
        ]
                
        m3dFindNormal(vNormal, vPoints[0], vPoints[1], vPoints[2])
        glNormal3fv(list(vNormal))
        glVertex3f(*vPoints[0])
        glVertex3f(*vPoints[1])
        glVertex3f(*vPoints[2])

        vPoints = [
            M3DVector3f(60.0, 2.0, -8.0),
            M3DVector3f(-60.0, 2.0, -8.0),
            M3DVector3f(0.0,7.0,-8.0),
        ]

        m3dFindNormal(vNormal, vPoints[0], vPoints[1], vPoints[2])
        glNormal3fv(list(vNormal))
        glVertex3f(*vPoints[0])
        glVertex3f(*vPoints[1])
        glVertex3f(*vPoints[2])

        vPoints = [
            M3DVector3f(0.0,2.0,27.0),
            M3DVector3f(0.0, 7.0, -8.0),
            M3DVector3f(-60.0, 2.0, -8.0),
        ]

        m3dFindNormal(vNormal, vPoints[0], vPoints[1], vPoints[2])
        glNormal3fv(list(vNormal))
        glVertex3f(*vPoints[0])
        glVertex3f(*vPoints[1])
        glVertex3f(*vPoints[2])

        # Tail section ###############
        # Bottom of back fin
        glNormal3f(0.0, -1.0, 0.0)
        glVertex3f(-30.0, -0.50, -57.0)
        glVertex3f(30.0, -0.50, -57.0)
        glVertex3f(0.0,-0.50,-40.0)

        vPoints = [
            M3DVector3f(0.0,-0.5,-40.0),
            M3DVector3f(30.0, -0.5, -57.0),
            M3DVector3f(0.0, 4.0, -57.0),
        ]

        m3dFindNormal(vNormal, vPoints[0], vPoints[1], vPoints[2])
        glNormal3fv(list(vNormal))
        glVertex3f(*vPoints[0])
        glVertex3f(*vPoints[1])
        glVertex3f(*vPoints[2])

        vPoints = [
            M3DVector3f(0.0, 4.0, -57.0),
            M3DVector3f(-30.0, -0.5, -57.0),
            M3DVector3f(0.0,-0.5,-40.0),
        ]

        m3dFindNormal(vNormal, vPoints[0], vPoints[1], vPoints[2])
        glNormal3fv(list(vNormal))
        glVertex3f(*vPoints[0])
        glVertex3f(*vPoints[1])
        glVertex3f(*vPoints[2])

        vPoints = [
            M3DVector3f(30.0,-0.5,-57.0),
            M3DVector3f(-30.0, -0.5, -57.0),
            M3DVector3f(0.0, 4.0, -57.0),
        ]

        m3dFindNormal(vNormal, vPoints[0], vPoints[1], vPoints[2])
        glNormal3fv(list(vNormal))
        glVertex3f(*vPoints[0])
        glVertex3f(*vPoints[1])
        glVertex3f(*vPoints[2])

        vPoints = [
            M3DVector3f(0.0,0.5,-40.0),
            M3DVector3f(3.0, 0.5, -57.0),
            M3DVector3f(0.0, 25.0, -65.0),
        ]

        m3dFindNormal(vNormal, vPoints[0], vPoints[1], vPoints[2])
        glNormal3fv(list(vNormal))
        glVertex3f(*vPoints[0])
        glVertex3f(*vPoints[1])
        glVertex3f(*vPoints[2])

        vPoints = [
            M3DVector3f(0.0, 25.0, -65.0),
            M3DVector3f(-3.0, 0.5, -57.0),
            M3DVector3f(0.0,0.5,-40.0),
        ]

        m3dFindNormal(vNormal, vPoints[0], vPoints[1], vPoints[2])
        glNormal3fv(list(vNormal))
        glVertex3f(*vPoints[0])
        glVertex3f(*vPoints[1])
        glVertex3f(*vPoints[2])

        vPoints = [
            M3DVector3f(3.0, 0.5, -57.0),
            M3DVector3f(-3.0, 0.5, -57.0),
            M3DVector3f(0.0, 25.0, -65.0),
        ]

        m3dFindNormal(vNormal, vPoints[0], vPoints[1], vPoints[2])
        glNormal3fv(list(vNormal))
        glVertex3f(*vPoints[0])
        glVertex3f(*vPoints[1])
        glVertex3f(*vPoints[2])

        glEnd()
                
        # Restore the matrix state
        glPopMatrix()

    def _update(self, dt):
        pass

    def on_resize(self, w, h):
        lightPos = [-50.0, 50.0, 100.0, 1.0]

        # Prevent a divide by zero
        if h == 0:
            h = 1

        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)

        # Reset coordinate system
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        fAspect = w / h
        gluPerspective(45.0, fAspect, 1.0, 225.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
        glTranslatef(0.0, 0.0, -150.0)
    
    def on_key_press(self, sym, mods):
        if sym == key.UP:
            self.xRot-= 5.0
        elif sym == key.DOWN:
            self.xRot += 5.0
        elif sym == key.LEFT:
            self.yRot -= 5.0
        elif sym == key.RIGHT:
            self.yRot += 5.0
        else:
            super(Window, self).on_key_press(sym, mods)
        self.xRot %= 360.0
        self.yRot %= 360.0
    
    def on_close(self):
        pyglet.clock.unschedule(self._update)
        super(Window, self).on_close()

if __name__ == '__main__':
    window = Window(800, 600, 'Shiny Jet')
    pyglet.app.run()
