"""
// pointsprites.c
// OpenGL SuperBible
// Demonstrates point sprites
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

    time_step = 1.0/60.0

    # Arrays of stars
    SMALL_STARS = 100
    MEDIUM_STARS = 40
    LARGE_STARS = 15
    vSmallStars = []
    vMediumStars = []
    vLargeStars = []

    # Normal points
    drawMode = 2

    # Texture Objects
    image_files = ('star.tga','moon.tga')
    images = []
    textureObjects = []

    # Menu is posted when menu is not None
    menu = None
    # A menu selection is pending when menu_option is not None; the value will
    # be the index of the selected item text in Window.menu_item.
    menu_option = 2
    # Put strings in the menu_items list to enable a popup menu. Leave it empty
    # to disable menu. Put your menu code in _handle_menu().
    menu_items = [
        "Normal Points",
        "Antialiased Points",
        "Point Sprites",
    ]

    # GL display lists stored by name
    dlists = {}

    def __init__(self, w, h, title='Pyglet App'):
        super(Window, self).__init__(w, h, title)

        # Populate star list
        for i in range(self.SMALL_STARS):
            self.vSmallStars.append((rand()*w, rand()*(h-100)+100.0))
                
        # Populate star list
        for i in range(self.MEDIUM_STARS):
            self.vMediumStars.append((rand()*w*10/10.0, rand()*(h-100)+100.0))

        # Populate star list
        for i in range(self.LARGE_STARS):
            self.vLargeStars.append((rand()*w*10/10.0, rand()*(h-100)*10.0/10.0+100.0))
                
        # Set drawing color to white
        glColor3f(0.0, 0.0, 0.0)

        # Load texture objects and texture maps
        for name in self.image_files:
            image = pyglet.image.load(name)
            texid = image.get_mipmapped_texture().id
            glBindTexture(GL_TEXTURE_2D, texid)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            self.images.append(image)
            self.textureObjects.append(texid)
        
        glTexEnvi(GL_POINT_SPRITE, GL_COORD_REPLACE, GL_TRUE)
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

        pyglet.clock.schedule_interval(self._update, self.time_step)

    def on_draw(self):
        self.clear()

        x = 700.0     # Location and radius of moon
        y = 500.0
        r = 50.0
        angle = 0.0   # Another looping variable
                    
        # Everything is white
        glColor3f(1.0, 1.0, 1.0)

        if self.drawMode == 2:
            glEnable(GL_POINT_SPRITE)
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.textureObjects[0])
            glEnable(GL_BLEND)

        # Draw small stars
        glPointSize(7.0)          # 1.0
        glBegin(GL_POINTS)
        for i in range(self.SMALL_STARS):
            glVertex2fv(self.vSmallStars[i])
        glEnd()
            
        # Draw medium sized stars
        glPointSize(12.0)         # 3.0
        glBegin(GL_POINTS)
        for i in range(self.MEDIUM_STARS):
            glVertex2fv(self.vMediumStars[i])
        glEnd()
            
        # Draw largest stars
        glPointSize(20.0)      # 5.5
        glBegin(GL_POINTS)
        for i in range(self.LARGE_STARS):
            glVertex2fv(self.vLargeStars[i])
        glEnd()
            
        glPointSize(120.0)
        if self.drawMode == 2:
            glDisable(GL_BLEND)
            glBindTexture(GL_TEXTURE_2D, self.textureObjects[1])

        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()

        glDisable(GL_TEXTURE_2D)
        glDisable(GL_POINT_SPRITE)

        # Draw distant horizon
        glLineWidth(3.5)
        glBegin(GL_LINE_STRIP)
        glVertex2f(0.0, 25.0)
        glVertex2f(50.0, 100.0)
        glVertex2f(100.0, 25.0)
        glVertex2f(225.0, 115.0)
        glVertex2f(300.0, 50.0)
        glVertex2f(375.0, 100.0)
        glVertex2f(460.0, 25.0)
        glVertex2f(525.0, 100.0)
        glVertex2f(600.0, 20.0)
        glVertex2f(675.0, 70.0)
        glVertex2f(750.0, 25.0)
        glVertex2f(800.0, 90.0)    
        glEnd()

        # Menu is drawn after all world rendering.
        if self.menu is not None:
            self._draw_menu()
            ## menu.draw() changes the GL modes, and this affects the rendering
            ## in the next loop iteration. So we need to keep putting them back
            ## after drawing the menu. It is something mysterious in the call to
            ## Batch.draw(). There is probably a better way to do these draw
            ## modes with Pyglet, but I haven't found it yet.
            self._do_draw_mode()

    def _do_draw_mode(self):
        if self.drawMode == 0:
            # Turn off blending and all smoothing
            glDisable(GL_BLEND)
            glDisable(GL_LINE_SMOOTH)
            glDisable(GL_POINT_SMOOTH)
            glDisable(GL_TEXTURE_2D)
            glDisable(GL_POINT_SPRITE)
        elif self.drawMode == 1:
            # Turn on antialiasing, and give hint to do the best
            # job possible.
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glEnable(GL_BLEND)
            glEnable(GL_POINT_SMOOTH)
            glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
            glEnable(GL_LINE_SMOOTH)
            glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
            glDisable(GL_TEXTURE_2D)
            glDisable(GL_POINT_SPRITE)
        elif self.drawMode == 2:
            # Point Sprites
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_COLOR, GL_ONE_MINUS_SRC_COLOR)
            glDisable(GL_LINE_SMOOTH)
            glDisable(GL_POINT_SMOOTH)
            glDisable(GL_POLYGON_SMOOTH)

    def _draw_menu(self):
        """render the menu"""
        # Switch to orthographic view (Pyglet default), draw the menu, then
        # switch back back to game view.
        self._gui_view()
        glPushMatrix()
        self.menu.draw()
        glPopMatrix()
        self.on_resize(self.width, self.height)

    def _update(self, dt):
        if self.menu_option is not None:
            self._handle_menu()

    def _handle_menu(self):
        """process menu selections"""
        self.drawMode = self.menu_option
        self.menu_option = None
        self._do_draw_mode()

    def _gui_view(self):
        w,h = self.width,self.height
        # Prevent a divide by zero
        if h == 0:
            h = 1

        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)

        # Reset projection matrix stack
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Establish clipping volume (left, right, bottom, top, near, far)
        gluOrtho2D(0.0, w, 0.0, h)


        # Reset Model view matrix stack
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def on_mouse_press(self, x, y, button, modifiers):
        """event handler; """
        if len(self.menu_items):
            self.menu_option = None
            self.menu = SimpleMenu(self, x, y, self.menu_items)
            @self.menu.event
            def on_close(selected_option):
                if selected_option is not None:
                    self.menu_option = self.menu_items.index(selected_option)
                self.menu = None
        return pyglet.event.EVENT_HANDLED

    def on_resize(self, w, h):
        # Prevent a divide by zero
        if h == 0:
            h = 1

        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)

        # Reset projection matrix stack
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Establish clipping volume (left, right, bottom, top, near, far)
        gluOrtho2D(0.0, w, 0.0, h)


        # Reset Model view matrix stack
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    
    def on_key_press(self, sym, mods):
        super(Window, self).on_key_press(sym, mods)
    
    def on_close(self):
        pyglet.clock.unschedule(self._update)
        super(Window, self).on_close()


if __name__ == '__main__':
    window = Window(800, 600, 'Point Sprite Night Lights')
    pyglet.app.run()
