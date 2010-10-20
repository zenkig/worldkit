"""
## Pythonated for Pyglet by Gummbum
"""


import sys

import pyglet
pyglet.options['debug_gl'] = False
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

    # The game runtime updates at this interval. For example, 1.0/30.0 is 30
    # times per second.
    time_step = 1.0/60.0

    # Menu is posted when menu is not None
    menu = None
    # A menu selection is pending when menu_option is not None; the value will
    # be the index of the selected item text in Window.menu_item.
    menu_option = None
    # Put strings in the menu_items list to enable a popup menu. Leave it empty
    # to disable menu. Put your menu code in _handle_menu().
    menu_items = []

    # GL display lists stored by name
    dlists = {}

    def __init__(self, w, h, title='Pyglet App'):
        super(Window, self).__init__(w, h, title)

        ## Init code here.

        pyglet.clock.schedule_interval(self._update, self.time_step)

    def _make_display_list(self, name, func):
        """make a GL display list that can be called by name
        
        name -> immutable object to use as dictionary key
        func -> calback function or method that executes GL rendering code; should require no args
        """
        dlists = self.dlists
        dlists[name] = glGenLists(1)
        glNewList(dlists[name], GL_COMPILE)
        func()
        glEndList()
    
    def _call_display_list(self, name):
        """call a GL display list by name"""
        glCallList(self.dlists[name])

    def on_draw(self):
        """event handler; Pyglet handler that's called when the display needs
        updating."""
        self.clear()

        glPushMatrix()
        
        ## Game rendering code here.
        
        glPopMatrix()

        # Menu is drawn after all world rendering.
        if self.menu is not None:
            self._draw_menu()

    def _draw_menu(self):
        """render the menu"""
        # Switch to orthographic view (Pyglet default), draw the menu, then
        # switch back back to game view.
#        super(Window, self).on_resize(self.width, self.height)
        self._gui_view()
        glPushMatrix()
        self.menu.draw()
        glPopMatrix()
        self.on_resize(self.width, self.height)

    def _update(self, dt):
        """event handler; update game state on timer
        
        Pyglet passes the number of milliseconds in dt that elapsed since the
        previous call."""
        if self.menu_option is not None:
            self._handle_menu()
        
        ## Game state updates here.

    def _handle_menu(self):
        """process menu selections"""
        option = self.menu_option
        text = self.menu_items[option]
        if option is 0:
            print 'Menu selected: %d -> %s' % (option,text)
        self.menu_option = None

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
        """event handler; initialize or resize window"""
        ## Replace this super call to customize your view.
        super(Window, self).on_resize(w, h)
    
    def on_key_press(self, sym, mods):
        """event handler; process key presses
        
        sym -> pyglet.window.key.* symbol
        mods -> pyglet.window.key.* modifiers, bitwise OR-ed"""
        ## Insert your if..elif.. and finish with else: super...
        ## This will allow pyglet to handle quit key press events.
        super(Window, self).on_key_press(sym, mods)
    
    def on_close(self):
        """event handler; on-exit code"""
        # Clean up our stuff then call Pyglet's handler.
        pyglet.clock.unschedule(self._update)
        super(Window, self).on_close()


if __name__ == '__main__':
    window = Window(800, 600, 'Pyglet Skeleton')
    pyglet.app.run()
