#!/usr/bin/env python

## Python imports
from string import Template

__version__ = '0.0.1'

class Globals(object):
    # world_kit package version
    vernum = (0,0,1)
    version = '%d.%d.%d' % vernum
    
    # These are intended to accept return values from optparse.ParseOptions.
    # parse_args() like so:
    # (Globals.program_options,Globals.program_args) = parser.parse_args()
    program_options = None
    program_args = None

    # Current room object dictates the context of the runtime at any given
    # moment; it is the room that the player is currently interacting with
    current_room = None
    
    player = None
    
    # Debug verbosity level; 0=silent
    debug = 0

    def __init__(self):
        raise Exception, 'do not instantiate world_kit.Globals'
