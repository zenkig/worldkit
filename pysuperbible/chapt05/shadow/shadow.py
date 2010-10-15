"""
// Shadow.cpp
// OpenGL SuperBible
// Demonstrates simple planar shadows
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

    # Light values and coordinates
    ambientLight = [0.3, 0.3, 0.3, 1.0]
    diffuseLight = [0.7, 0.7, 0.7, 1.0]
    specular = [1.0, 1.0, 1.0, 1.0]
    lightPos = [-75.0, 150.0, -50.0, 0.0]
    specref =  [1.0, 1.0, 1.0, 1.0]

    # Transformation matrix to project shadow
    shadowMat = M3DMatrix44f()

    def __init__(self, w, h, title='Pyglet App'):
        super(Window, self).__init__(w, h, title)

        # Any three points on the ground (counter clockwise order)
        points = [
            [-30.0, -149.0, -20.0],
            [-30.0, -149.0, 20.0],
            [40.0, -149.0, 20.0],
        ]

        glEnable(GL_DEPTH_TEST)	# Hidden surface removal
        glFrontFace(GL_CCW)		# Counter clock-wise polygons face out
        glEnable(GL_CULL_FACE)		# Do not calculate inside of jet

        # Setup and enable light 0
        glLightfv(GL_LIGHT0,GL_AMBIENT, self.ambientLight)
        glLightfv(GL_LIGHT0,GL_DIFFUSE, self.diffuseLight)
        glLightfv(GL_LIGHT0,GL_SPECULAR, self.specular)
        glLightfv(GL_LIGHT0,GL_POSITION, self.lightPos)
        glEnable(GL_LIGHT0)

        # Enable color tracking
        glEnable(GL_COLOR_MATERIAL)
        
        # Set Material properties to follow glColor values
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

        # All materials hereafter have full specular reflectivity
        # with a high shine
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.specref)
        glMateriali(GL_FRONT, GL_SHININESS, 128)

        # Light blue background
        glClearColor(0.0, 0.0, 1.0, 1.0)

        # Get the plane equation from three points on the ground
        vPlaneEquation = M3DVector4f()
        m3dGetPlaneEquation(vPlaneEquation, points[0], points[1], points[2])

        # Calculate projection matrix to draw shadow on the ground
        m3dMakePlanarShadowMatrix(self.shadowMat, vPlaneEquation, self.lightPos)
        
        glEnable(GL_NORMALIZE)

        pyglet.clock.schedule_interval(self._update, 1.0/60.0)

    def on_draw(self):
        self.clear()

        # Draw the ground, we do manual shading to a darker green
        # in the background to give the illusion of depth
        glBegin(GL_QUADS)
        glColor3ub(0,32,0)
        glVertex3f(400.0, -150.0, -200.0)
        glVertex3f(-400.0, -150.0, -200.0)
        glColor3ub(0,255,0)
        glVertex3f(-400.0, -150.0, 200.0)
        glVertex3f(400.0, -150.0, 200.0)
        glEnd()

        # Save the matrix state and do the rotations
        glPushMatrix()

        # Draw jet at new orientation, put light in correct position
        # before rotating the jet
        glEnable(GL_LIGHTING)
        glLightfv(GL_LIGHT0, GL_POSITION, self.lightPos)
        glRotatef(self.xRot, 1.0, 0.0, 0.0)
        glRotatef(self.yRot, 0.0, 1.0, 0.0)

        self._draw_jet(0)

        # Restore original matrix state
        glPopMatrix()	

        # Get ready to draw the shadow and the ground
        # First disable lighting and save the projection state
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glPushMatrix()

        # Multiply by shadow projection matrix
        glMultMatrixf(list(self.shadowMat))

        # Now rotate the jet around in the new flattend space
        glRotatef(self.xRot, 1.0, 0.0, 0.0)
        glRotatef(self.yRot, 0.0, 1.0, 0.0)

        # Pass true to indicate drawing shadow
        self._draw_jet(1)	

        # Restore the projection to normal
        glPopMatrix()

        # Draw the light source
        glPushMatrix()
        glTranslatef(*self.lightPos[:3])
        glColor3ub(255,255,0)
        glutSolidSphere(5.0, 10, 10)
        glPopMatrix()

        # Restore lighting state variables
        glEnable(GL_DEPTH_TEST)

    def _draw_jet(self, nShadow):
        vNormal = [0.0] * 3     # Storeage for calculated surface normal

        # Nose Cone #############################
        # Set material color, note we only have to set to black
        # for the shadow once
        if nShadow == 0:
            glColor3ub(128, 128, 128)
        else:
            glColor3ub(0,0,0)

        # Nose Cone - Points straight down
        # Set material color
        glBegin(GL_TRIANGLES)
        glNormal3f(0.0, -1.0, 0.0)
        glNormal3f(0.0, -1.0, 0.0)
        glVertex3f(0.0, 0.0, 60.0)
        glVertex3f(-15.0, 0.0, 30.0)
        glVertex3f(15.0, 0.0, 30.0)

        # Verticies for this panel
        vPoints = [
            [15.0, 0.0,  30.0],
            [0.0,  15.0, 30.0],
            [0.0,  0.0,  60.0],
        ]

        # Calculate the normal for the plane
        m3dFindNormal(vNormal, vPoints[0], vPoints[1], vPoints[2])
        glNormal3fv(vNormal)
        glVertex3fv(vPoints[0])
        glVertex3fv(vPoints[1])
        glVertex3fv(vPoints[2])

        vPoints = [
            [0.0, 0.0, 60.0],
            [0.0, 15.0, 30.0],
            [-15.0, 0.0, 30.0],
        ]

        m3dFindNormal(vNormal, vPoints[0], vPoints[1], vPoints[2])
        glNormal3fv(vNormal)
        glVertex3fv(vPoints[0])
        glVertex3fv(vPoints[1])
        glVertex3fv(vPoints[2])

        # Body of the Plane ########################
        vPoints = [
            [-15.0, 0.0, 30.0],
            [0.0, 15.0, 30.0],
            [0.0, 0.0, -56.0],
        ]

        m3dFindNormal(vNormal, vPoints[0], vPoints[1], vPoints[2])
        glNormal3fv(vNormal)
        glVertex3fv(vPoints[0])
        glVertex3fv(vPoints[1])
        glVertex3fv(vPoints[2])

        vPoints = [
            [0.0, 0.0, -56.0],
            [0.0, 15.0, 30.0],
            [15.0,0.0,30.0],
        ]
    
        m3dFindNormal(vNormal, vPoints[0], vPoints[1], vPoints[2])
        glNormal3fv(vNormal)
        glVertex3fv(vPoints[0])
        glVertex3fv(vPoints[1])
        glVertex3fv(vPoints[2])
    
        glNormal3f(0.0, -1.0, 0.0)
        glVertex3f(15.0, 0.0, 30.0)
        glVertex3f(-15.0, 0.0, 30.0)
        glVertex3f(0.0, 0.0, -56.0)
    
        # #############################################
        # Left wing
        # Large triangle for bottom of wing
        vPoints = [
            [0.0,2.0,27.0],
            [-60.0, 2.0, -8.0],
            [60.0, 2.0, -8.0],
        ]

        m3dFindNormal(vNormal, vPoints[0], vPoints[1], vPoints[2])
        glNormal3fv(vNormal)
        glVertex3fv(vPoints[0])
        glVertex3fv(vPoints[1])
        glVertex3fv(vPoints[2])

        vPoints = [
            [60.0, 2.0, -8.0],
            [0.0, 7.0, -8.0],
            [0.0, 2.0, 27.0],
        ]
                
        m3dFindNormal(vNormal, vPoints[0], vPoints[1], vPoints[2])
        glNormal3fv(vNormal)
        glVertex3fv(vPoints[0])
        glVertex3fv(vPoints[1])
        glVertex3fv(vPoints[2])

        vPoints = [
            [60.0, 2.0, -8.0],
            [-60.0, 2.0, -8.0],
            [0.0, 7.0, -8.0],
        ]

        m3dFindNormal(vNormal, vPoints[0], vPoints[1], vPoints[2])
        glNormal3fv(vNormal)
        glVertex3fv(vPoints[0])
        glVertex3fv(vPoints[1])
        glVertex3fv(vPoints[2])

        vPoints = [
            [0.0, 2.0, 27.0],
            [0.0, 7.0, -8.0],
            [-60.0, 2.0, -8.0],
        ]

        m3dFindNormal(vNormal, vPoints[0], vPoints[1], vPoints[2])
        glNormal3fv(vNormal)
        glVertex3fv(vPoints[0])
        glVertex3fv(vPoints[1])
        glVertex3fv(vPoints[2])
                
                        
        # Tail section ##############################
        # Bottom of back fin
        glNormal3f(0.0, -1.0, 0.0)
        glVertex3f(-30.0, -0.50, -57.0)
        glVertex3f(30.0, -0.50, -57.0)
        glVertex3f(0.0, -0.50, -40.0)

        vPoints = [
            [0.0, -0.5, -40.0],
            [30.0, -0.5, -57.0],
            [0.0, 4.0, -57.0],
        ]

        m3dFindNormal(vNormal, vPoints[0], vPoints[1], vPoints[2])
        glNormal3fv(vNormal)
        glVertex3fv(vPoints[0])
        glVertex3fv(vPoints[1])
        glVertex3fv(vPoints[2])

        vPoints = [
            [0.0, 4.0, -57.0],
            [-30.0, -0.5, -57.0],
            [0.0, -0.5, -40.0],
        ]

        m3dFindNormal(vNormal, vPoints[0], vPoints[1], vPoints[2])
        glNormal3fv(vNormal)
        glVertex3fv(vPoints[0])
        glVertex3fv(vPoints[1])
        glVertex3fv(vPoints[2])

        vPoints = [
            [30.0, -0.5, -57.0],
            [-30.0, -0.5, -57.0],
            [0.0, 4.0, -57.0],
        ]

        m3dFindNormal(vNormal, vPoints[0], vPoints[1], vPoints[2])
        glNormal3fv(vNormal)
        glVertex3fv(vPoints[0])
        glVertex3fv(vPoints[1])
        glVertex3fv(vPoints[2])

        vPoints = [
            [0.0, 0.5, -40.0],
            [3.0, 0.5, -57.0],
            [0.0, 25.0, -65.0],
        ]

        m3dFindNormal(vNormal, vPoints[0], vPoints[1], vPoints[2])
        glNormal3fv(vNormal)
        glVertex3fv(vPoints[0])
        glVertex3fv(vPoints[1])
        glVertex3fv(vPoints[2])

        vPoints = [
            [0.0, 25.0, -65.0],
            [-3.0, 0.5, -57.0],
            [0.0, 0.5, -40.0],
        ]

        m3dFindNormal(vNormal, vPoints[0], vPoints[1], vPoints[2])
        glNormal3fv(vNormal)
        glVertex3fv(vPoints[0])
        glVertex3fv(vPoints[1])
        glVertex3fv(vPoints[2])

        vPoints = [
            [3.0, 0.5, -57.0],
            [-3.0, 0.5, -57.0],
            [0.0, 25.0, -65.0],
        ]

        m3dFindNormal(vNormal, vPoints[0], vPoints[1], vPoints[2])
        glNormal3fv(vNormal)
        glVertex3fv(vPoints[0])
        glVertex3fv(vPoints[1])
        glVertex3fv(vPoints[2])

        glEnd()

    def _update(self, dt):
        pass

    def on_resize(self, w, h):
        # Prevent a divide by zero
        if h == 0:
            h = 1

        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)

        # Reset coordinate system
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        fAspect = w / h
        gluPerspective(60.0, fAspect, 200.0, 500.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Move out Z axis so we can see everything
        glTranslatef(0.0, 0.0, -400.0)
        glLightfv(GL_LIGHT0, GL_POSITION, self.lightPos)
    
    def on_key_press(self, sym, mods):
        if sym == key.UP:
            self.xRot -= 5.0
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
    window = Window(800, 600, 'Shadow')
    pyglet.app.run()
