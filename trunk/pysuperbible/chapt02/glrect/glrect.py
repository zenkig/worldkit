"""
// GLRect.cpp
// Just draw a single rectangle in the middle of the screen
// OpenGL SuperBible, 3rd Edition
// Richard S. Wright Jr.
// rwright@starstonesoftware.com
## Pythonated for Pyglet by Gummbum
"""


import pyglet
from pyglet.gl import *


class Window(pyglet.window.Window):

    def __init__(self):
        super(Window, self).__init__(width=800, height=600, caption='GLRect')
        # Set clear color to blue
        glClearColor(0.0, 0.0, 1.0, 1.0)

    def on_draw(self):
        """Called when window needs to be rendered"""
        self.clear()

        # Set current drawing color to red
        #		   R	 G	   B
        glColor3f(1.0, 0.0, 0.0)

        # Draw a filled rectangle with current color
        glRectf(-25.0, 25.0, 25.0, -25.0)

    def on_resize(self, w, h):
        """Called when window is created or resized"""
        # Prevent a divide by zero
        if h == 0:
            h = 1
            
        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)

        # Reset coordinate system
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Establish clipping volume (left, right, bottom, top, near, far)
        aspectRatio = w / h
        if w <= h:
            glOrtho(
                -100.0, 100.0,
                -100/aspectRatio, 100.0/aspectRatio,
                1.0, -1.0)
        else:
            glOrtho(
                -100.0*aspectRatio, 100.0*aspectRatio,
                -100.0, 100.0,
                1.0, -1.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()


if __name__ == '__main__':
    window = Window()
    pyglet.app.run()
