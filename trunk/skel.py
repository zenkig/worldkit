#!/usr/bin/env python

__version__ = '0.0.1'

## Python imports
import imp
import os
import sys

def get_main_dir():
    """needed for py2exe compatibility"""
    def main_is_frozen():
        return (hasattr(sys, "frozen") or # new py2exe
                hasattr(sys, "importers") # old py2exe
                or imp.is_frozen("__main__")) # tools/freeze
    if main_is_frozen():
        # Program run from an executable, e.g. py2exe
        return os.path.dirname(sys.executable)
    elif os.path.dirname(sys.argv[0]) != '':
        # Program run as: python somepath/prog.py
        return os.path.dirname(sys.argv[0])
    else:
        # Program run as: python prog.py
        return sys.path[0]

PROGRAM_DIR = get_main_dir()
os.chdir(PROGRAM_DIR)
sys.path.insert(0, os.path.join(PROGRAM_DIR,'lib'))

try:
    ## Game library imports
    import main
except ImportError, e:
    print 'ImportError: %s' % e
    print '    in file "%s"' % os.path.abspath(sys.argv[0])

if __name__ == '__main__':
    main.run()
