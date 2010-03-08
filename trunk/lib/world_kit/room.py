#!/usr/bin/env python

__version__ = '0.0.1'

try:
    ## World kit imports
    import world_kit
    from world_kit import Globals
except ImportError, e:
    print 'ImportError: %s' % e
    print '    in file "%s"' % os.path.abspath(sys.argv[0])
    quit()

class Room(world_kit.Container):
    """Room contains objects, and has exits that link it to other rooms."""
    def __init__(self, **kwargs):
        super(Room, Room).__init__(self, **kwargs)
        self._exits = {}
    def enter(self):
        Globals.current_room = self
        self._on_enter()
    def exit(self, exit_name):
        return self._exits[exit_name]
    def exits(self):
        return dict(self._exits)
    def exit_names(self):
        return self._exits.keys()
    def use_exit(self, exit_name):
        self._exits[exit_name].use()
    def _add_exit(self, exit_name, exit):
        self._exits[exit_name] = exit
        return exit
    def _on_enter(self):
        """override in subclass to perform actions upon entering"""
        pass
    def _remove_exit(self, exit_name):
        del self._exits[exit_name]

class Exit(world_kit.Object):
    """Exit links two room objects together. When you "use" an exit, it
    moves the game's focus from the current room to the room on the other
    side of the exit."""
    def __init__(self, **kwargs):
        super(Exit, Exit).__init__(self, **kwargs)
        self._rooms = {}
        if kwargs.has_key('rooms'):
            self.link(*kwargs.get('rooms'))
    def link(self, room1, exit_name1, room2, exit_name2):
        self._rooms.clear()
        self._rooms[room1] = exit_name1
        self._rooms[room2] = exit_name2
        room1._add_exit(exit_name1, self)
        room2._add_exit(exit_name2, self)
    def unlink(self):
        for (room,exit_name) in self._rooms:
            room._remove_exit(exit_name)
        self._rooms.clear()
    def use(self):
        (this,that) = self._rooms.keys()
        if Globals.current_room is this:
            that.enter()
        elif Globals.current_room is that:
            this.enter()
    def _on_use(self):
        """override in subclass to perform actions upon using the exit"""
        pass
