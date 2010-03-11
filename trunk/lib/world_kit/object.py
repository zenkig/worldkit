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
        self.parent = kwargs.get('parent', None)
        self.id = kwargs.get('id', _next_id())
        self.name = kwargs.get('name', '')

    ############################################################################
    # Properties

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def parent(self):
        return self._parent
    @parent.setter
    def parent(self, value):
        self._parent = value

    ############################################################################

class Container(Object):
    """Container holds objects."""
    def __init__(self, **kwargs):
        super(Container, Container).__init__(self, **kwargs)        self._contents = []
        self.add(*kwargs.get('contents', []))

    ############################################################################
    # Properties

    @property
    def contents(self):
        return list(self._contents)

    @property
    def count(self):
        return len(self._contents)

    ############################################################################
    # Methods

    def add(self, *obj):
        for o in obj:
            self._contents.append(o)
            o.parent = self

    def empty(self):
        del self._contents[:]

    def remove(self, obj):
        obj.parent = None
        self._contents.remove(obj)
