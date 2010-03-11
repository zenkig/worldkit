#!/usr/bin/env python

__version__ = '0.0.1'

__doc__ = """Game initialization. Parse command line args, create a single
game level, and cycle the main event loop.
"""

## Python imports
from optparse import OptionParser
import os
import sys

try:
    ## Pygame imports
    import pygame
    ## World kit imports
    import world_kit
    from world_kit import Globals, debug1
    ## Game imports
    import level1
except ImportError, e:
    print 'ImportError: %s' % e
    print '    in file "%s"' % os.path.abspath(sys.argv[0])
    quit()

def init():
    # Parse command line args
    globals = world_kit.Globals
    def show_version(*args):
        print 'Version', globals.version
        quit()
    def inc_debug(*args):
        if globals.debug < 3:
            globals.debug += 1
    parser = OptionParser()
    parser.add_option('-V', '--version',
        action='callback', callback=show_version,
        help='show version')
    parser.add_option('-v', '--verbose',
        action='callback', callback=inc_debug,
        help='increase verbosity')
    (globals.program_options, globals.program_args) = parser.parse_args()
    
    # Init Pygame in console-only mode
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.display.init()

def run():
    debug1('game.run start')
    init()
    running = True
    level = level1.Level()
    level.start()
    
    while running:
        command = raw_input('> ')
        if len(command) == 0:
            pass
        elif command in Globals.current_room.exits:
            Globals.current_room.exit(command).use()
        elif command.startswith('q'):
            running = False
        
        if level.complete:
            level.finish()
            running = False
    
    print 'Goodbye.'
    debug1('game.run exit')
