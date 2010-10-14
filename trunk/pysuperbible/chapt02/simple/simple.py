"""
// Simple.cpp
// The Simplest OpenGL program with GLUT
// OpenGL SuperBible, 3rd Edition
// Richard S. Wright Jr.
// rwright@starstonesoftware.com
## Pythonated for Pyglet by Gummbum
"""

import pyglet
from pyglet.gl import *

class Window(pyglet.window.Window):
    
    def __init__(self):
        # Open a window "Simple" in the title bar
        super(Window, self).__init__(caption="Simple")
        # Set the color with which to clear the window
        glClearColor(0.0, 0.0, 1.0, 1.0)
    
    def on_draw(self):
        """Called to draw scene"""
        # Clear the window's color and depth buffers
        self.clear()

if __name__ == '__main__':
    # Make our Pyglet window object
    window = Window()
    # Start the Pyglet application loop
    pyglet.app.run()
