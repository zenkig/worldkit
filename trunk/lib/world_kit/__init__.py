#!/usr/bin/env python

__version__ = '0.0.1'

from world_kit.globals import Globals
from world_kit.object import Object
from world_kit.object import Container
from world_kit.room import Room
from world_kit.room import Exit
from world_kit.level import Level

def debug1(s):
    if Globals.debug > 0:
        print 'debug1:',s
def debug2(s):
    if Globals.debug > 1:
        print 'debug2:',s
def debug3(s):
    if Globals.debug > 2:
        print 'debug3:',s
