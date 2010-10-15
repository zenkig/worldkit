"""
// Spot.cpp
// OpenGL SuperBible
// Demonstrates OpenGL Spotlight
// Program by Richard S. Wright Jr.
## Pythonated for Pyglet by Gummbum
##
## Change to accommodate GLUT-vs-menus problem...
## GLUT: Warning in (unamed): cannot attach menus in game mode
## Menus have been replaced by keys:
##      s -> Toggle flat/smooth shading
##      t -> Cycle tesselation detail
##      h -> Print current value of shading and tesselation detail
"""


import sys

import pyglet
from pyglet.gl import *
from pyglet.window import key

# GLUT for shapes and menus
from OpenGL.GLUT import *

sys.path.append('../../lib')
from gltools import *
from math3d import *


# Flags for effects
MODE_FLAT = 1
MODE_SMOOTH = 2
MODE_VERYLOW = 3
MODE_MEDIUM = 4
MODE_VERYHIGH = 5
mode_names = (
    'None',
    'MODE_FLAT',
    'MODE_SMOOTH',
    'MODE_VERYLOW',
    'MODE_MEDIUM',
    'MODE_VERYHIGH',
)


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

    iShade = MODE_FLAT
    iTess = MODE_VERYLOW

    # Rotation amounts
    xRot = 0.0
    yRot = 0.0

    # Light values and coordinates
    lightPos = M3DVector4f(0.0, 0.0, 75.0, 1.0)
    specular = M3DVector4f(1.0, 1.0, 1.0, 1.0)
    specref =  M3DVector4f(1.0, 1.0, 1.0, 1.0)
    ambientLight = M3DVector4f(0.5, 0.5, 0.5, 1.0)
    spotDir = M3DVector3f(0.0, 0.0, -1.0)

    def __init__(self, w, h, title='Pyglet App'):
        super(Window, self).__init__(w, h, title)

        glEnable(GL_DEPTH_TEST) # Hidden surface removal
        glFrontFace(GL_CCW)     # Counter clock-wise polygons face out
        glEnable(GL_CULL_FACE)  # Do not try to display the back sides

        # Enable lighting
        glEnable(GL_LIGHTING)

        # Setup and enable light 0
        # Supply a slight ambient light so the objects can be seen
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, vecf(self.ambientLight))
        
        # The light is composed of just a diffuse and specular components
        glLightfv(GL_LIGHT0, GL_DIFFUSE, vecf(self.ambientLight))
        glLightfv(GL_LIGHT0, GL_SPECULAR, vecf(self.specular))
        glLightfv(GL_LIGHT0, GL_POSITION, vecf(self.lightPos))

        # Specific spot effects
        # Cut off angle is 60 degrees
        glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 50.0)

        # Enable this light in particular
        glEnable(GL_LIGHT0)

        # Enable color tracking
        glEnable(GL_COLOR_MATERIAL)
        
        # Set Material properties to follow glColor values
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

        # All materials hereafter have full specular reflectivity
        # with a high shine
        glMaterialfv(GL_FRONT, GL_SPECULAR, vecf(self.specref))
        glMateriali(GL_FRONT, GL_SHININESS, 128)


        # Black background
        glClearColor(0.0, 0.0, 0.0, 1.0)

        pyglet.clock.schedule_interval(self._update, 1.0/60.0)

    def on_draw(self):
        if self.iShade == MODE_FLAT:
            glShadeModel(GL_FLAT)
        else: # self.iShade == MODE_SMOOTH
            glShadeModel(GL_SMOOTH)

        self.clear()

        # First place the light 
        # Save the coordinate transformation
        glPushMatrix()
        # Rotate coordinate system
        glRotatef(self.yRot, 0.0, 1.0, 0.0)
        glRotatef(self.xRot, 1.0, 0.0, 0.0)

        # Specify new position and direction in rotated coords.
        glLightfv(GL_LIGHT0, GL_POSITION, vecf(self.lightPos))
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, vecf(self.spotDir))

        # Draw a red cone to enclose the light source
        glColor3ub(255,0,0)

        # Translate origin to move the cone out to where the light
        # is positioned.
        x,y,z = self.lightPos[:3]
        glTranslatef(x, y, z)
        glutSolidCone(4.0, 6.0, 15, 15)

        # Draw a smaller displaced sphere to denote the light bulb
        # Save the lighting state variables
        glPushAttrib(GL_LIGHTING_BIT)

        # Turn off lighting and specify a bright yellow sphere
        glDisable(GL_LIGHTING)
        glColor3ub(255,255,0)
        glutSolidSphere(3.0, 15, 15)

        # Restore lighting state variables
        glPopAttrib()

        # Restore coordinate transformations
        glPopMatrix()


        # Set material color and draw a sphere in the middle
        glColor3ub(0, 0, 255)

        if self.iTess == MODE_VERYLOW:
            glutSolidSphere(30.0, 7, 7)
        else:
            if self.iTess == MODE_MEDIUM:
                glutSolidSphere(30.0, 15, 15)
            else: # iTess == MODE_MEDIUM
                glutSolidSphere(30.0, 50, 50)

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

        # Establish viewing volume
        fAspect = w / h
        gluPerspective(35.0, fAspect, 1.0, 500.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -250.0)
    
    def on_key_press(self, sym, mods):
        if sym == key.UP:
            self.xRot-= 5.0
        elif sym == key.DOWN:
            self.xRot += 5.0
        elif sym == key.LEFT:
            self.yRot -= 5.0
        elif sym == key.RIGHT:
            self.yRot += 5.0
        elif sym == key.H:
            print 'Shading',mode_names[self.iShade]
            print 'Tesselation:',mode_names[self.iTess]
        elif sym == key.S:
            self.iShade += 1
            if self.iShade > MODE_SMOOTH:
                self.iShade = MODE_FLAT
            print 'Shading',mode_names[self.iShade]
        elif sym == key.T:
            self.iTess += 1
            if self.iTess > MODE_VERYHIGH:
                self.iTess = MODE_VERYLOW
            print 'Tesselation:',mode_names[self.iTess]
        else:
            super(Window, self).on_key_press(sym, mods)

        self.xRot %= 360.0
        self.yRot %= 360.0
    
    def on_close(self):
        pyglet.clock.unschedule(self._update)
        super(Window, self).on_close()

if __name__ == '__main__':
    window = Window(800, 600, 'Spot Light')
    pyglet.app.run()
