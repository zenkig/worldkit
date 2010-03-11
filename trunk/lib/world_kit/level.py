#!/usr/bin/env python
import sys
import os

__version__ = '0.0.1'

try:
    ## World kit imports
    import world_kit
    from world_kit import Globals
except ImportError, e:
    print 'ImportError: %s' % e
    print '    in file "%s"' % os.path.abspath(sys.argv[0])
    quit()

class Level(world_kit.Container):
    """Level contains rooms linked by exits, has a start point and a finish
    condition."""
    def __init__(self, **kwargs):
        super(Level, Level).__init__(self, **kwargs)
        self._goal = kwargs.get('goal', lambda _: False)
        self._rooms = {}
        self._exits = []
        self._start_room = None

    ############################################################################
    # Properties

    @property
    def rooms(self):
        return dict(self._rooms)

    @property
    def complete(self):
        return self._goal(self)

    @property
    def start_room(self):
        return self._start_room
    @start_room.setter
    def start_room(self, value):
        self._start_room = value

    ############################################################################
    # Methods

    def start(self):
        Globals.current_room = self.start_room
        self._on_start()

    def finish(self):
        self._on_finish()

    def link(self, room1, name1, room2, name2):
        self._add_room(room1, name1)
        self._add_room(room2, name2)
        self._add_exit(world_kit.Exit(rooms=(room1, name1, room2, name2)))

    def _add_room(self, room, name):
        self._room[name] = room

    def _add_exit(self, exit):
        self._exits.append(exit)

    def _on_start(self):
        """override in subclass to perform actions upon level start"""
        pass

    def _on_finish(self):
        """override in subclass to perform actions upon level completion"""
        pass

    ############################################################################

