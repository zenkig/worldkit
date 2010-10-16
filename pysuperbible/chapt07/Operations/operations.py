"""
// Operations.cpp
// OpenGL SuperBible
// Demonstrates Imaging Operations
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
from simple_menu import SimpleMenu


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

    # source image data
    pImage = None
    iWidth = 0
    iHeight = 0
    iComponents = 0
    eFormat = 0

    # desired drawing mode
    menu_option = None
    iRenderMode = 1

    def __init__(self, w, h, title='Pyglet App'):
        super(Window, self).__init__(w, h, title)
        self.pImage = pyglet.image.load('horse.tga')
        pyglet.clock.schedule_interval(self._update, 1.0/60.0)

    def on_draw(self):
        self.clear()

    def _update(self, dt):
        pass

    def on_resize(self, w, h):
        # Prevent a divide by zero, when window is too short
        # (you cant make a window of zero width).
        if h == 0:
            h = 1

        glViewport(0, 0, w, h)
            
        # Reset the coordinate system before modifying
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        # Set the clipping volume
        gluOrtho2D(0.0, w, 0.0, h)
            
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    
    def on_key_press(self, sym, mods):
        super(Window, self).on_key_press(sym, mods)
    
    def on_mouse_press(x, y, button, modifiers):
        self.menu_option = None
        menu_items = [
            'Save Image',
            'Draw Pixels',
            'Flip Pixels',
            'Zoom Pixels',
            'Just Red Channel',
            'Just Green Channel',
            'Just Blue Channel',
            'Black and White',
            'Invert Colors',
        ]
        m = SimpleMenu(self, x, y, menu_items)
        @m.event
        def on_close(selected_option):
            if selected_option is not None:
                self.menu_option = menu_items.index(selected_option)
        if self.menu_option == 0:
             # Save image
            pyglet.image.get_buffer_manager().get_color_buffer().save('Screenshot.png')
        else:
            # Change render mode index to match menu entry index
            self.iRenderMode = self.menu_option
        return pyglet.event.EVENT_HANDLED

    def on_close(self):
        pyglet.clock.unschedule(self._update)
        super(Window, self).on_close()


if __name__ == '__main__':
    window = Window(800, 600, 'OpenGL Image Operations')
    pyglet.app.run()
