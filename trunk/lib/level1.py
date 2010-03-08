#!/usr/bin/env python

__version__ = '0.0.1'

try:
    ## Pygame imports
    import pygame
    ## World kit imports
    import world_kit
    from world_kit import Globals
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
        print self._enter_msg % self.name()
        print 'Exits:', ', '.join(self.exit_names())
        print 'Contents:', ', '.join([str(o) for o in self.contents()])

class Chair(world_kit.Object):
    def __str__(self):
        return 'chair'

class Sack(world_kit.Container):
    def __str__(self):
        return 'empty sack'

entrance = Room(contents=[Chair()])
room1 = Room(contents=[Sack()])
#world_kit.Exit().link(entrance, 'n', room1, 's')
world_kit.Exit(rooms=(entrance,'n',room1,'s'))

entrance.enter()
