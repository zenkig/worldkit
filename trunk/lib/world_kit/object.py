#!/usr/bin/env python

__version__ = '0.0.1'

def _next_id():
    global _id
    _id += 1
    return _id
_id = 1

class Object(object):
    """Object is the top-level world_kit ancestor."""
    def __init__(self, **kwargs):
        self._parent = kwargs.get('parent', None)
        self._id = kwargs.get('id', _next_id())
        self._name = kwargs.get('name', '')
    def id(self):
        return self._id
    def name(self):
        return self._name
    def parent(self):
        return self._parent
    def set_id(self, val):
        self._id = val
    def set_name(self, name):
        self._name = name
    def set_parent(self, parent):
        self._parent = parent

class Container(Object):
    """Container holds objects."""
    def __init__(self, **kwargs):
        super(Container, Container).__init__(self, **kwargs)        self._contents = []
        self.add(*kwargs.get('contents', []))
    def add(self, *obj):
        for o in obj:
            self._contents.append(o)
            o.set_parent(self)
    def contents(self):
        return list(self._contents)
    def count(self):
        return len(self._contents)
    def empty(self):
        del self._contents[:]
    def remove(self, obj):
        obj.set_parent(None)
        self._contents.remove(obj)
