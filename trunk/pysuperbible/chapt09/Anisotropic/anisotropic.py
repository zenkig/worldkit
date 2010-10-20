"""
// Anisotropic.cpp
// Demonstrates anisotropic texture filtering
// OpenGL SuperBible
// Richard S. Wright Jr.
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
from simple_menu import SimpleMenu


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

    # Textures
    TEXTURE_BRICK   = 0
    TEXTURE_FLOOR   = 1
    TEXTURE_CEILING = 2
    szTextureFiles = ('brick.tga', 'floor.tga', 'ceiling.tga')
    images = []

    # Menu
    menu = None
    menu_option = None
    menu_items = (
        'GL_NEAREST',
        'GL_LINEAR',
        'GL_NEAREST_MIPMAP_NEAREST',
        'GL_NEAREST_MIPMAP_LINEAR',
        'GL_LINEAR_MIPMAP_NEAREST',
        'GL_LINEAR_MIPMAP_LINEAR',
        'Anisotropic Filter',
        'Anisotropic Off',
    )

    # Object distance from viewer
    zPos = -60.0
    zoom = 0.0
    menuRot = 0.0

    # GL display lists stored by name
    dlists = {}

    def __init__(self, w, h, title='Pyglet App'):
        super(Window, self).__init__(w, h, title)

        # Textures applied as decals, no lighting or coloring effects
        glEnable(GL_TEXTURE_2D)
        for name in self.szTextureFiles:
            self.images.append(pyglet.image.load(name))

        pyglet.clock.schedule_interval(self._update, 1.0/60.0)

    def get_texture(self, which):
        return self.images[which].get_mipmapped_texture().id

    def on_draw(self):
        self.clear()

        # Save the matrix state and do the rotations
        glPushMatrix()
        
        # Move object back and do in place rotation
        glTranslatef(0.0, 0.0, self.zPos)
    
        # Floor
        for i in range(60, 0, -10):
            z = float(i)
            glBindTexture(GL_TEXTURE_2D, self.get_texture(self.TEXTURE_FLOOR))
            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 0.0)
            glVertex3f(-10.0, -10.0, z)

            glTexCoord2f(1.0, 0.0)
            glVertex3f(10.0, -10.0, z)

            glTexCoord2f(1.0, 1.0)
            glVertex3f(10.0, -10.0, z - 10.0)

            glTexCoord2f(0.0, 1.0)
            glVertex3f(-10.0, -10.0, z - 10.0)
            glEnd()

            # Ceiling
            glBindTexture(GL_TEXTURE_2D, self.get_texture(self.TEXTURE_CEILING))
            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(-10.0, 10.0, z - 10.0)

            glTexCoord2f(1.0, 1.0)
            glVertex3f(10.0, 10.0, z - 10.0)

            glTexCoord2f(1.0, 0.0)
            glVertex3f(10.0, 10.0, z)

            glTexCoord2f(0.0, 0.0)
            glVertex3f(-10.0, 10.0, z)
            glEnd()

            
            # Left Wall
            glBindTexture(GL_TEXTURE_2D, self.get_texture(self.TEXTURE_BRICK))
            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 0.0)
            glVertex3f(-10.0, -10.0, z)

            glTexCoord2f(1.0, 0.0)
            glVertex3f(-10.0, -10.0, z - 10.0)

            glTexCoord2f(1.0, 1.0)
            glVertex3f(-10.0, 10.0, z - 10.0)

            glTexCoord2f(0.0, 1.0)
            glVertex3f(-10.0, 10.0, z)
            glEnd()


            # Right Wall
            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(10.0, 10.0, z)

            glTexCoord2f(1.0, 1.0)
            glVertex3f(10.0, 10.0, z - 10.0)

            glTexCoord2f(1.0, 0.0)
            glVertex3f(10.0, -10.0, z - 10.0)

            glTexCoord2f(0.0, 0.0)
            glVertex3f(10.0, -10.0, z)
            glEnd()

        # Restore the matrix state
        glPopMatrix()

        # Menu is drawn after all world rendering.
        if self.menu is not None:
            self._draw_menu()

    def _draw_menu(self):
        super(Window, self).on_resize(self.width, self.height)
        glPushMatrix()
        self.menu.draw()
        glPopMatrix()
        self.on_resize(self.width, self.height)

    def _update(self, dt):
        if self.zoom != 0.0:
            self.zPos += self.zoom

        if self.menu_option is not None:
            self._handle_menu()
    
    def _handle_menu(self):
        print 'menu option',self.menu_items[self.menu_option]
        for tex in [im.get_mipmapped_texture().id for im in self.images]:
            glBindTexture(GL_TEXTURE_2D, tex)
            if self.menu_option == 0:
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            elif self.menu_option == 1:
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            elif self.menu_option == 2:
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST)
            elif self.menu_option == 3:
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_LINEAR)
            elif self.menu_option == 4:
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
            elif self.menu_option == 5:
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            elif self.menu_option == 6:
                fLargest = glGetFloatv(GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT)
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, fLargest)
            elif self.menu_option == 7:
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, 1.0)
        self.menu_option = None

    def on_resize(self, w, h):
        # Prevent a divide by zero
        if h == 0:
            h = 1

        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)

        fAspect = w / h

        # Reset coordinate system
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Produce the perspective projection
        gluPerspective(90.0, fAspect, 1, 500)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    
    def on_key_press(self, sym, mods):
        if sym == key.UP:
            self.zoom = 1.0
        elif sym == key.DOWN:
            self.zoom = -1.0
        else:
            super(Window, self).on_key_press(sym, mods)

    def on_key_release(self, sym, mods):
        if sym in (key.UP,key.DOWN):
            self.zoom = 0.0

    def on_mouse_press(self, x, y, button, modifiers):
        self.menu_option = None
        self.menu = SimpleMenu(self, x, y, self.menu_items)
        @self.menu.event
        def on_close(selected_option):
            if selected_option is not None:
                self.menu_option = self.menu_items.index(selected_option)
            self.menu = None
        return pyglet.event.EVENT_HANDLED

    def on_close(self):
        pyglet.clock.unschedule(self._update)
        super(Window, self).on_close()


if __name__ == '__main__':
    window = Window(800, 600, 'Anisotropic Tunnel')
    pyglet.app.run()
