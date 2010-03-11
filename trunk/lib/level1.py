#!/usr/bin/env python

__version__ = '0.0.1'

import os
import sys

try:
    ## Pygame imports
    import pygame
    ## World kit imports
    import world_kit
    from world_kit import Globals, debug1
except ImportError, e:
    print 'ImportError: %s' % e
    print '    in file "%s"' % os.path.abspath(sys.argv[0])
    quit()

class Room(world_kit.Room):
    def __init__(self, **kwargs):
        kwargs.setdefault('name', 'an unremarkable room')
        super(Room,Room).__init__(self, **kwargs)
        self._enter_msg = kwargs.get(
            'enter_msg', 'You enter %s.')
    def _on_enter(self):
        print self._enter_msg % self.name
        print 'Exits:', ', '.join(self.exit_names)
        print 'Contents:', ', '.join([str(o) for o in self.contents])

class Chair(world_kit.Object):
    def __str__(self):
        return 'chair'

class Sack(world_kit.Container):
    def __str__(self):
        return 'empty sack'

def goal_condition(level):
    """Dummy goal condition that succeeds after 5 actions"""
    i = getattr(level, 'i', 1)
    debug1('actions performed: %d' % i)
    if i < 5:
        level.i = i + 1
        return False
    else:        
        return True

class Level(world_kit.Level):
    def __init__(self, **kwargs):
        kwargs.setdefault('name', 'Level 1')
        kwargs.setdefault('goal', goal_condition)
        super(Level, Level).__init__(self, **kwargs)
        entrance = Room(contents=[Chair()])
        room1 = Room(contents=[Sack()])
        self.link(entrance, 'n', room1, 's')
        self.start_room = entrance

    def _on_start(self):
        debug1('level started')
        Globals.current_room.enter()

    def _on_finish(self):
        debug1('level finished')

