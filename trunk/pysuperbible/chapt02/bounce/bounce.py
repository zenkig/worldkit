"""
// Bounce.cpp
// Demonstrates a simple animated rectangle program with GLUT
// OpenGL SuperBible, 3rd Edition
// Richard S. Wright Jr.
// rwright@starstonesoftware.com
## Pythonated for Pyglet by Gummbum
"""


import pyglet
from pyglet.gl import *


class Window(pyglet.window.Window):

    # Initial square position and size
    x = 0.0
    y = 0.0
    rsize = 25

    # Step size in x and y directions
    # (number of pixels to move each second)
    xstep = 60.0
    ystep = 60.0

    # Keep track of windows changing width and height
    windowWidth = 800
    windowHeight = 600

    def __init__(self):
        super(Window, self).__init__(
            width=self.windowWidth,
            height=self.windowHeight,
            caption='Bounce')
        pyglet.clock.schedule_interval(self._update, 1.0/60.0)

    def on_draw(self):
        self.clear()
        
        # Set current drawing color to red
        #		   R	 G	   B
        glColor3f(1.0, 0.0, 0.0)

        # Draw a filled rectangle with current color
        x,y,rsize = self.x, self.y, self.rsize
        glRectf(x, y, x+rsize, y-rsize)

    def _update(self, dt):
        x,y = self.x, self.y
        xstep,ystep = self.xstep*dt, self.ystep*dt
        windowWidth,windowHeight = self.windowWidth, self.windowHeight
        rsize = self.rsize
        
        # Reverse direction when you reach left or right edge
        if x > windowWidth-rsize or x < -windowWidth:
            self.xstep = -self.xstep
            xstep = -xstep

        # Reverse direction when you reach top or bottom edge
        if y > windowHeight or y < -windowHeight+rsize:
            self.ystep = -self.ystep
            ystep = -ystep

        # Actually move the square
        x += xstep
        y += ystep

        # Check bounds. This is in case the window is made
        # smaller while the rectangle is bouncing and the 
        # rectangle suddenly finds itself outside the new
        # clipping volume
        if x > (windowWidth-rsize + xstep):
            self.x = windowWidth - rsize - 1
        elif x < -(windowWidth + xstep):
            self.x = -windowWidth - 1
        else:
            self.x = x

        if y > (windowHeight + ystep):
            self.y = windowHeight-1
        elif y < -(windowHeight - rsize + ystep):
            self.y = -windowHeight + rsize - 1
        else:
            self.y = y

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
        
        # Reset coordinate system
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Establish clipping volume (left, right, bottom, top, near, far)
        aspectRatio = w / h
        if w <= h:
            windowWidth = 100
            windowHeight = 100 / aspectRatio
            glOrtho(-100.0, 100.0, -windowHeight, windowHeight, 1.0, -1.0)
        else:
            windowWidth = 100 * aspectRatio
            windowHeight = 100
            glOrtho(-windowWidth, windowWidth, -100.0, 100.0, 1.0, -1.0)

        self.windowWidth = windowWidth
        self.windowHeight = windowHeight

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def on_close(self):
        pyglet.clock.unschedule(self._update)
        pyglet.app.exit()


if __name__ == '__main__':
    window = Window()
    pyglet.app.run()
