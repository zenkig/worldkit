"""
// SphereWorld.cpp
// OpenGL SuperBible
// Demonstrates an immersive 3D environment using actors
// and a camera. This version adds lights and material properties
// and shadows.
// Program by Richard S. Wright Jr.
## Pythonated for Pyglet by Gummbum
## Added display lists for speed.
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

    NUM_SPHERES = 30
    spheres = [None] * NUM_SPHERES
    frameCamera = GLFrame()

    # Light and material Data
    fLightPos = gl_vec(GLfloat, -100.0, 100.0, 50.0, 1.0)  # Point source
    fNoLight = gl_vec(GLfloat, 0.0, 0.0, 0.0, 0.0)
    fLowLight = gl_vec(GLfloat, 0.25, 0.25, 0.25, 1.0)
    fBrightLight = gl_vec(GLfloat, 1.0, 1.0, 1.0, 1.0)

    mShadowMatrix = [0.0] * 16

    # Textures
    szTextureFiles = ('grass.tga', 'wood.tga', 'orb.tga')
    GROUND_TEXTURE = 0
    TORUS_TEXTURE  = 1
    SPHERE_TEXTURE = 2
    NUM_TEXTURES   = 3
    images = []
    textureObjects = []

    # Movement
    forward = 0.0
    turn = 0.0
    right = 0.0

    # GL display lists stored by name
    dlists = {}
    
    yRot = 0.0

    def __init__(self, w, h, title='Pyglet App'):
        super(Window, self).__init__(w, h, title)

        vPoints = [
            [0.0, -0.4, 0.0],
            [10.0, -0.4, 0.0],
            [5.0, -0.4, -5.0],
        ]
    
        # Grayish background
        glClearColor(*self.fLowLight)
   
        # Clear stencil buffer with zero, increment by one whenever anybody
        # draws into it. When stencil function is enabled, only write where
        # stencil value is zero. This prevents the transparent shadow from drawing
        # over itself
        glStencilOp(GL_INCR, GL_INCR, GL_INCR)
        glClearStencil(0)
        glStencilFunc(GL_EQUAL, 0x0, 0x01)
    
        # Cull backs of polygons
        glCullFace(GL_BACK)
        glFrontFace(GL_CCW)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE_ARB)
    
        # Setup light parameters
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, self.fNoLight)
        glLightfv(GL_LIGHT0, GL_AMBIENT, self.fLowLight)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.fBrightLight)
        glLightfv(GL_LIGHT0, GL_SPECULAR, self.fBrightLight)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        
        # Calculate shadow matrix
        pPlane = M3DVector4f()
        m3dGetPlaneEquation(pPlane, vPoints[0], vPoints[1], vPoints[2])
        m3dMakePlanarShadowMatrix(self.mShadowMatrix, pPlane, self.fLightPos)
    
        # Mostly use material tracking
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.fBrightLight)
        glMateriali(GL_FRONT, GL_SHININESS, 128)
    
        # Randomly place the sphere inhabitants
        for iSphere in range(self.NUM_SPHERES):
            # Pick a random location between -20 and 20 at .1 increments
            s = GLFrame()
            x = rand() * 40 - 20
            z = rand() * 40 - 20
            s.SetOrigin(x, 0.0, z)
            self.spheres[iSphere] = s
      
        # Set up texture maps
        glEnable(GL_TEXTURE_2D)
        for name in self.szTextureFiles:
            image = pyglet.image.load(name)
            texid = image.get_mipmapped_texture().id
            self.images.append(image)
            self.textureObjects.append(texid)

        # Set up display lists for faster rendering
        self._make_display_list('ground', self._draw_ground)
        self._make_display_list('torus', self._draw_torus)
        self._make_display_list('big sphere', self._draw_big_sphere)
        self._make_display_list('small sphere', self._draw_small_sphere)

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

    def clear(self):
        # Pyglet's Window.clear() does not clear stencil buffer.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)

    def on_draw(self):
        self.clear()

        glPushMatrix()
        self.frameCamera.ApplyCameraTransform()
        
        # Position light before any other transformations
        glLightfv(GL_LIGHT0, GL_POSITION, self.fLightPos)
        
        # Draw the ground
        glColor3f(1.0, 1.0, 1.0)
        #self._draw_ground()
        self._call_display_list('ground')
        
        # Draw shadows first
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_STENCIL_TEST)
        glPushMatrix()
        glMultMatrixf(self.mShadowMatrix)
        self._draw_inhabitants(1)
        glPopMatrix()
        glDisable(GL_STENCIL_TEST)
        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)
        
        # Draw inhabitants normally
        self._draw_inhabitants(0)

        glPopMatrix()

    def _draw_inhabitants(self, nShadow):
        if nShadow == 0:
            glColor4f(1.0, 1.0, 1.0, 1.0)
        else:
            glColor4f(0.0, 0.0, 0.0, 0.6);  # Shadow color
      
        # Draw the randomly located spheres
        for i in range(self.NUM_SPHERES):
            glPushMatrix()
            self.spheres[i].ApplyActorTransform()
            #self._draw_big_sphere()
            self._call_display_list('big sphere')
            glPopMatrix()

        # Draw mobile sphere and torus
        glPushMatrix()
        glTranslatef(0.0, 0.1, -2.5)
    
        glPushMatrix()
        glRotatef(-self.yRot * 2.0, 0.0, 1.0, 0.0)
        glTranslatef(1.0, 0.0, 0.0)
        #self._draw_small_sphere()
        self._call_display_list('small sphere')
        glPopMatrix()
    
        if nShadow == 0:
            # Torus alone will be specular
            glMaterialfv(GL_FRONT, GL_SPECULAR, self.fBrightLight)
        
        glRotatef(self.yRot, 0.0, 1.0, 0.0)
        #self._draw_torus()
        self._call_display_list('torus')
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.fNoLight)
        glPopMatrix()

    def _draw_ground(self):
        """draw texture-mapped ground; this should go in a display list"""
        fExtent = 20
        fStep = 1
        y = -0.4
        s = 0.0
        t = 0.0
        texStep = 1.0 / (fExtent * .075)
        
        glBindTexture(GL_TEXTURE_2D, self.textureObjects[self.GROUND_TEXTURE])
        
        for iStrip in range(-fExtent, fExtent+1, fStep):
            t = 0.0
            glBegin(GL_TRIANGLE_STRIP)
            for iRun in range(fExtent, -fExtent, -fStep):
                glTexCoord2f(s, t)
                glNormal3f(0.0, 1.0, 0.0)   # All Point up
                glVertex3f(iStrip, y, iRun)
                glTexCoord2f(s + texStep, t)
                glNormal3f(0.0, 1.0, 0.0)   # All Point up
                glVertex3f(iStrip + fStep, y, iRun)
                t += texStep
            glEnd()
            s += texStep

    def _draw_torus(self):
        """draw torus; this should go in a display list"""
        glBindTexture(GL_TEXTURE_2D, self.textureObjects[self.TORUS_TEXTURE])
        gltDrawTorus(0.35, 0.15, 61, 37)
    
    def _draw_small_sphere(self):
        """draw small sphere; this should go in a display list"""
        glBindTexture(GL_TEXTURE_2D, self.textureObjects[self.SPHERE_TEXTURE])
        gltDrawSphere(0.1, 21, 11)

    def _draw_big_sphere(self):
        """draw big sphere; this should go in a display list"""
        glBindTexture(GL_TEXTURE_2D, self.textureObjects[self.SPHERE_TEXTURE])
        gltDrawSphere(0.3, 21, 11)

    def _update(self, dt):
        self.yRot = (self.yRot + 1.0) % 360.0
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
        ## Delete the textures ??
#        glDeleteTextures(self.NUM_TEXTURES, self.textureObjects)

        pyglet.clock.unschedule(self._update)
        pyglet.clock.unschedule(self.fps)
        super(Window, self).on_close()


if __name__ == '__main__':
    window = Window(800, 600, 'OpenGL SphereWorld Demo + Texture Maps')
    pyglet.app.run()
