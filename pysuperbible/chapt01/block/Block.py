"""
// Block.py, from Block.cpp
// OpenGL SuperBible, Chapter 1
// Demonstrates an assortment of basic 3D concepts
// Program by Richard S. Wright Jr.
## Pythonated for Pyglet by Gummbum
"""


import sys

import pyglet
from pyglet.gl import *
from pyglet.window import key

# GLUT for wireframes
from OpenGL.GLUT import *

sys.path.append('../../lib')
from math3d import *


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

    nStep = 0
    lightAmbient = gl_vec(GLfloat, 0.2, 0.2, 0.2, 1.0)
    lightDiffuse = gl_vec(GLfloat, 0.7, 0.7, 0.7, 1.0)
    lightSpecular = gl_vec(GLfloat, 0.9, 0.9, 0.9)
    materialColor = gl_vec(GLfloat, 0.8, 0.0, 0.0)
    vLightPos = gl_vec(GLfloat, -80.0, 120.0, 100.0, 0.0)
    ground = [
        [0.0, -25.0, 0.0],
        [10.0, -25.0, 0.0],
        [10.0, -25.0, -10.0],
    ]
    textures = []
    mCubeTransform = [0.0] * 16
    pPlane = M3DVector4f()

    def __init__(self):
        super(Window, self).__init__()
        self.images = [
            pyglet.image.load('floor.tga'),
            pyglet.image.load('Block4.tga'),
            pyglet.image.load('Block5.tga'),
            pyglet.image.load('Block6.tga'),
        ]
        self.textures[:] = [im.get_texture().id for im in self.images]

    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:
            self.nStep += 1
            if self.nStep > 5:
                self.nStep = 0

    def on_draw(self):
        self.clear()
        glShadeModel(GL_SMOOTH)
        glEnable(GL_NORMALIZE)
        
        glPushMatrix()
        
        # Draw plane that the cube rests on
        glDisable(GL_LIGHTING)
        if self.nStep == 5:
            self._draw_tabletop_textured()
        else:
            self._draw_tabletop_colored()

        # Set drawing color to Red
        glColor3f(1.0, 0.0, 0.0)

        # Enable lighting when step > 2
        if self.nStep > 2:
            self._enable_lighting()

        # Move the cube slightly forward and to the left
        glTranslatef(-10.0, 0.0, 10.0)

        # Draw image depending on nStep
        if self.nStep == 0:
            # Just draw the wire framed cube
            glutWireCube(50.0)
        elif self.nStep == 1:
            # Same wire cube with hidden line removal simulated
            # Front Face (before rotation)
            self._draw_cube_colored()
        elif self.nStep == 2:
            # No lighting; Uniform colored surface looks 2D and goofey
            glutSolidCube(50.0)
        elif self.nStep == 3:
            # With lighting
            glutSolidCube(50.0)
        elif self.nStep == 4:
            # With shadow
            self._draw_cube_colored_with_shadow()
        elif self.nStep == 5:
            # With textures applied
            self._draw_cube_textured()
            
        glPopMatrix()

    def _enable_lighting(self):
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glEnable(GL_COLOR_MATERIAL)

        glLightfv(GL_LIGHT0, GL_AMBIENT, self.lightAmbient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.lightDiffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, self.lightSpecular)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.lightSpecular)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, self.materialColor)
        glMateriali(GL_FRONT, GL_SHININESS, 128)

    def _draw_tabletop_colored(self):
        glColor3f(0.0, 0.0, 0.90)    # Blue
        glBegin(GL_QUADS)
        glVertex3f(-100.0, -25.3, -100.0)
        glVertex3f(-100.0, -25.3, 100.0)		
        glVertex3f(100.0,  -25.3, 100.0)
        glVertex3f(100.0,  -25.3, -100.0)
        glEnd()

    def _draw_cube_colored(self):
        glBegin(GL_LINES)
        glVertex3f(25.0,25.0,25.0)
        glVertex3f(25.0,-25.0,25.0)
        
        glVertex3f(25.0,-25.0,25.0)
        glVertex3f(-25.0,-25.0,25.0)

        glVertex3f(-25.0,-25.0,25.0)
        glVertex3f(-25.0,25.0,25.0)

        glVertex3f(-25.0,25.0,25.0)
        glVertex3f(25.0,25.0,25.0)
        glEnd()

        # Top of cube
        glBegin(GL_LINES)
        # Front Face
        glVertex3f(25.0,25.0,25.0)
        glVertex3f(25.0,25.0,-25.0)
        
        glVertex3f(25.0,25.0,-25.0)
        glVertex3f(-25.0,25.0,-25.0)

        glVertex3f(-25.0,25.0,-25.0)
        glVertex3f(-25.0,25.0,25.0)

        glVertex3f(-25.0,25.0,25.0)
        glVertex3f(25.0,25.0,25.0)
        glEnd()

        # Last two segments for effect
        glBegin(GL_LINES)
        glVertex3f(25.0,25.0,-25.0)
        glVertex3f(25.0,-25.0,-25.0)

        glVertex3f(25.0,-25.0,-25.0)
        glVertex3f(25.0,-25.0,25.0)
        glEnd()

    def _draw_cube_colored_with_shadow(self):
        mCubeTransform = gl_vec(GLfloat, self.mCubeTransform)
        pPlane = self.pPlane
        
        # Draw a shadow with some lighting
        glGetFloatv(GL_MODELVIEW_MATRIX, mCubeTransform)
        glutSolidCube(50.0)
        glPopMatrix()

        # Disable lighting, we'll just draw the shadow as black
        glDisable(GL_LIGHTING)
        
        glPushMatrix()

        ground = self.ground
        m3dGetPlaneEquation(pPlane, ground[0], ground[1], ground[2])
        m3dMakePlanarShadowMatrix(mCubeTransform, pPlane, self.vLightPos)
        #MakeShadowMatrix(ground, lightpos, cubeXform);
        glMultMatrixf(mCubeTransform)
        
        glTranslatef(-10.0, 0.0, 10.0)
        
        # Set drawing color to Black
        glColor3f(0.0, 0.0, 0.0)

        glutSolidCube(50.0)
    
    def _draw_tabletop_textured(self):
        glColor3ub(255,255,255)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.textures[0])
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-100.0, -25.3, -100.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-100.0, -25.3, 100.0)		
        glTexCoord2f(1.0, 1.0)
        glVertex3f(100.0,  -25.3, 100.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(100.0,  -25.3, -100.0)
        glEnd()

    def _draw_cube_textured(self):
        mCubeTransform = gl_vec(GLfloat, self.mCubeTransform)
        pPlane = self.pPlane
        textures = self.textures
        ground = self.ground
        
        glColor3ub(255,255,255)
        glGetFloatv(GL_MODELVIEW_MATRIX, mCubeTransform)

        # Front Face (before rotation)
        glBindTexture(GL_TEXTURE_2D, textures[1])
        glBegin(GL_QUADS)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(25.0, 25.0, 25.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(25.0, -25.0, 25.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-25.0, -25.0, 25.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-25.0, 25.0, 25.0)
        glEnd()

        # Top of cube
        glBindTexture(GL_TEXTURE_2D, textures[2])
        glBegin(GL_QUADS)
        # Front Face
        glTexCoord2f(0.0, 0.0)
        glVertex3f(25.0, 25.0, 25.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(25.0, 25.0, -25.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-25.0, 25.0, -25.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-25.0, 25.0, 25.0)
        glEnd()

        # Last two segments for effect
        glBindTexture(GL_TEXTURE_2D, textures[3])
        glBegin(GL_QUADS)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(25.0, 25.0, -25.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(25.0, -25.0, -25.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(25.0, -25.0, 25.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(25.0, 25.0, 25.0)
        glEnd()

        glPopMatrix()

        # Disable lighting, we'll just draw the shadow as black
        glDisable(GL_LIGHTING)
        glDisable(GL_TEXTURE_2D)
        
        glPushMatrix()

        m3dGetPlaneEquation(pPlane, ground[0], ground[1], ground[2])
        m3dMakePlanarShadowMatrix(mCubeTransform, pPlane, self.vLightPos)
        glMultMatrixf(mCubeTransform)
        
        glTranslatef(-10.0, 0.0, 10.0)
        
        # Set drawing color to Black
        glColor3f(0.0, 0.0, 0.0)
        glutSolidCube(50.0)

    def on_resize(self, w, h):
        # Prevent a divide by zero, when window is too short
        # (you cant make a window of zero width).
        if h == 0:
            h = 1
        # Keep the square square
        if w <= h:
            windowHeight = 100.0*h/w
            windowWidth = 100.0
        else:
            windowWidth = 100.0*w/h
            windowHeight = 100.0
        # Set the viewport to be the entire window
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # Set the clipping volume
        glOrtho(-100.0, windowWidth, -100.0, windowHeight, -200.0, 200.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glLightfv(GL_LIGHT0, GL_POSITION, self.vLightPos)
        glRotatef(30.0, 1.0, 0.0, 0.0)
        glRotatef(330.0, 0.0, 1.0, 0.0)

if __name__ == '__main__':
    window = Window()
    pyglet.app.run()
