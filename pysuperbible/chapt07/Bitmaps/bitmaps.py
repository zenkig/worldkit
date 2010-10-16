"""
// Bitmaps.cpp
// OpenGL SuperBible
// Demonstrates loading and displaying bitmaps
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


# Bitmap of camp fire
fire = [
    0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0xc0,
    0x00, 0x00, 0x01, 0xf0,
    0x00, 0x00, 0x07, 0xf0,
    0x0f, 0x00, 0x1f, 0xe0,
    0x1f, 0x80, 0x1f, 0xc0,
    0x0f, 0xc0, 0x3f, 0x80,	
    0x07, 0xe0, 0x7e, 0x00,
    0x03, 0xf0, 0xff, 0x80,
    0x03, 0xf5, 0xff, 0xe0,
    0x07, 0xfd, 0xff, 0xf8,
    0x1f, 0xfc, 0xff, 0xe8,
    0xff, 0xe3, 0xbf, 0x70, 
    0xde, 0x80, 0xb7, 0x00,
    0x71, 0x10, 0x4a, 0x80,
    0x03, 0x10, 0x4e, 0x40,
    0x02, 0x88, 0x8c, 0x20,
    0x05, 0x05, 0x04, 0x40,
    0x02, 0x82, 0x14, 0x40,
    0x02, 0x40, 0x10, 0x80, 
    0x02, 0x64, 0x1a, 0x80,
    0x00, 0x92, 0x29, 0x00,
    0x00, 0xb0, 0x48, 0x00,
    0x00, 0xc8, 0x90, 0x00,
    0x00, 0x85, 0x10, 0x00,
    0x00, 0x03, 0x00, 0x00,
    0x00, 0x00, 0x10, 0x00,
]


class Window(pyglet.window.Window):

    def __init__(self, w, h, title='Pyglet App'):
        super(Window, self).__init__(w, h, title)

        pyglet.clock.schedule_interval(self._update, 1.0/60.0)

    def on_draw(self):
        self.clear()

        # Set color to white
        glColor3f(1.0, 1.0, 1.0)
        
        # Loop through 16 rows and columns
        for y in range(16):
            # Set raster position for this "square"
            glRasterPos2i(0, y*32)
            for x in range(16):
                # Draw the "fire" bitmap, advance raster position
                glBitmap(32, 32, 0.0, 0.0, 32.0, 0.0, fire)

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

        # Psuedo window coordinates
        gluOrtho2D(0.0, w, 0.0, h)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    
    def on_key_press(self, sym, mods):
        super(Window, self).on_key_press(sym, mods)
    
    def on_close(self):
        pyglet.clock.unschedule(self._update)
        super(Window, self).on_close()


if __name__ == '__main__':
    window = Window(512, 512, 'OpenGL Bitmaps')
    pyglet.app.run()
