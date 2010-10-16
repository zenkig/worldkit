"""
// Operations.cpp
// OpenGL SuperBible
// Demonstrates Imaging Operations
// Program by Richard S. Wright Jr.
## Pythonated for Pyglet by Gummbum
## Added display lists for glDrawPixels(), as it is a very expensive operation
## Gumm note: Yeah, there's a lotta freaky voodoo in here.
## The inverted image doesn't save any pixels for some mysterious reason.
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

    # source image data
    image = None
    pImage = None
    pModifiedBytes = None
    iWidth = 0
    iHeight = 0
    iComponents = 0
    eFormat = 0
    data = None

    # desired drawing mode
    menu = None
    menu_option = None
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
    iRenderMode = 1

    # GL display lists
    dlists = {}

    def __init__(self, w, h, title='Pyglet App'):
        super(Window, self).__init__(w, h, title)

        self.image = pyglet.image.load('horse.tga')

        pyglet.clock.schedule_interval(self._update, 1.0/60.0)

    def _make_display_list(self, name, func):
        dlists = self.dlists
        dlists[name] = glGenLists(1)
        glNewList(dlists[name], GL_COMPILE)
        func()
        glEndList()
    
    def _call_display_list(self, name):
        glCallList(self.dlists[name])

    def on_draw(self):
        self.clear()

#        iViewport = [0] * 4
        pModifiedBytes = None
        invertMap = [0] * 256
        
        iRenderMode = self.iRenderMode
        iWidth,iHeight,eFormat,pImage = self.iWidth, self.iHeight, self.eFormat, self.pImage
        
        # Current Raster Position always at bottom left hand corner of window
        glRasterPos2i(0, 0);
            
        # Do image operation, depending on rendermode index
        if iRenderMode == 2:     # Flip the pixels
            glPixelZoom(-1.0, -1.0)
            glRasterPos2i(iWidth, iHeight)
        elif iRenderMode == 3:     # Zoom pixels to fill window
            iViewport = glGetIntegerv(GL_VIEWPORT)
            glPixelZoom(float(iViewport[2])/iWidth, float(iViewport[3])/iHeight)
        elif iRenderMode == 4:     # Just Red
            glPixelTransferf(GL_RED_SCALE, 1.0)         
            glPixelTransferf(GL_GREEN_SCALE, 0.0)
            glPixelTransferf(GL_BLUE_SCALE, 0.0) 
        elif iRenderMode == 5:     # Just Green
            glPixelTransferf(GL_RED_SCALE, 0.0)         
            glPixelTransferf(GL_GREEN_SCALE, 1.0)
            glPixelTransferf(GL_BLUE_SCALE, 0.0) 
        elif iRenderMode == 6:     # Just Blue
            glPixelTransferf(GL_RED_SCALE, 0.0)         
            glPixelTransferf(GL_GREEN_SCALE, 0.0)
            glPixelTransferf(GL_BLUE_SCALE, 1.0)
        elif iRenderMode == 7:     # Black & White, more tricky
            if pModifiedBytes is None:
                # First draw image into color buffer
                self._call_display_list('color image')

                # Allocate space for the luminance map
                nBytes = iWidth * iHeight
                pModifiedBytes = gl_vec(GLubyte, ([0]*nBytes))
                
                # Scale colors according to NSTC standard
                glPixelTransferf(GL_RED_SCALE, 0.3)
                glPixelTransferf(GL_GREEN_SCALE, 0.59)
                glPixelTransferf(GL_BLUE_SCALE, 0.11)
                
                # Read pixles into buffer (scale above will be applied)
                glReadPixels(0,0, iWidth, iHeight, GL_LUMINANCE, GL_UNSIGNED_BYTE, pModifiedBytes)
                
                # Return color scaling to normal
                glPixelTransferf(GL_RED_SCALE, 1.0)
                glPixelTransferf(GL_GREEN_SCALE, 1.0)
                glPixelTransferf(GL_BLUE_SCALE, 1.0)
                
                self.pModifiedBytes = pModifiedBytes
                self._make_display_list('bw image', self._make_bw_image)
        elif iRenderMode ==  8:     # Invert colors
            invertMap[0] = 1.0
            for i in range(256):
                invertMap[i] = 1.0 - (1.0 / 255.0 * i)
                
            glPixelMapfv(GL_PIXEL_MAP_R_TO_R, 255, invertMap)
            glPixelMapfv(GL_PIXEL_MAP_G_TO_G, 255, invertMap)
            glPixelMapfv(GL_PIXEL_MAP_B_TO_B, 255, invertMap)
            glPixelTransferi(GL_MAP_COLOR, GL_TRUE)

        if False:
            # Let pyglet render (a manual hack for debugging)
            self.image.blit(0, 0)
        else:
            # Do the pixel draw
            if pModifiedBytes is None:
                if self.pImage is None:
                    self._make_display_list('color image', self._make_color_image)
                else:
                    self._call_display_list('color image')
            else:
                self._call_display_list('bw image')

        # Reset everyting to default
        glPixelTransferi(GL_MAP_COLOR, GL_FALSE)
        glPixelTransferf(GL_RED_SCALE, 1.0)
        glPixelTransferf(GL_GREEN_SCALE, 1.0)
        glPixelTransferf(GL_BLUE_SCALE, 1.0)
        glPixelZoom(1.0, 1.0)   # No Pixel Zooming

        # If the menu exists, draw it.
        if self.menu is not None:
            self.menu.draw()

    def _make_color_image(self):
        # Details needed by GL
        self.iWidth = self.image.width
        self.iHeight = self.image.height
        self.eFormat = self.image._get_gl_format_and_type(self.image.format)[0]
        # And the data needed by GL
        raw_image = self.image.get_image_data()
        pixels = raw_image.get_data(raw_image.format, raw_image.pitch)
        self.pImage = gl_vec(GLubyte, pixels)
        # Render the image
        iWidth,iHeight,eFormat,pImage = self.iWidth, self.iHeight, self.eFormat, self.pImage
        glDrawPixels(iWidth, iHeight, eFormat, GL_UNSIGNED_BYTE, pImage)
    
    def _make_bw_image(self):
        iWidth,iHeight,pModifiedBytes = self.iWidth, self.iHeight, self.pModifiedBytes
        glDrawPixels(iWidth, iHeight, GL_LUMINANCE, GL_UNSIGNED_BYTE, pModifiedBytes)

    
    def _update(self, dt):
        if self.menu_option is None:
            return
        
        if self.menu_option == 0 and self.menu is None:
             # Save image, but wait until menu is destroyed
            self.on_draw()
            pyglet.image.get_buffer_manager().get_color_buffer().save('Screenshot.png')
            self.menu_option = None
        else:
            # Change render mode index to match menu entry index
            self.iRenderMode = self.menu_option
            self.menu_option = None

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
    
    def on_mouse_press(self, x, y, button, modifiers):
        self.menu_option = None
        self.menu = SimpleMenu(self, x, y, self.menu_items)
        @self.menu.event
        def on_close(selected_option):
            del (self.menu)
            if selected_option is not None:
                self.menu_option = self.menu_items.index(selected_option)
        return pyglet.event.EVENT_HANDLED

    def on_close(self):
        pyglet.clock.unschedule(self._update)
        super(Window, self).on_close()


if __name__ == '__main__':
    window = Window(800, 600, 'OpenGL Image Operations (click for menu)')
    pyglet.app.run()
