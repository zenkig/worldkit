This is a Python port of the very nice OpenGL Superbible, Revision 4.

Software requirements/tested for this port are:

* Pyglet/Version 1.1
* PyOpenGL/Version 3
* OpenGL/Version 2.1

The original C++ source code is available on the official site http://www.starstonesoftware.com/OpenGL/. The book is available for purchase from many popular book sellers. Please consider supporting the author of this book.

The Superbible libraries and examples are Pythonated by Gummbum as a learning experience towards a 3D world kit concept to be used in an upcoming, as yet unnamed game project. World kit source is available from the project site, http://code.google.com/p/worldkit/.

A fair amount of conversion was required for each example. But by far most of the work has gone into the math3d and glframe modules which do the heavy lifting for the Superbible examples.

This is a work in progress, nowhere near completion at the time of this writing. Chapters 1, 3, and 4 are complete and there are 19 chapters total. It is likely that not all examples will be translated to Python.

The glframe module is complete, but not yet thoroughly tested and proven by the examples. Some bugs were squahsed that were introduced by the translation to Python, and there may be more.

The math3d module is quite huge. The Vector classes are totally revamped in the spirit of the popular vec2d module and their usage is Pythonated wherever possible, mostly apparent in the math3d and glframe modules. Many math3d functions are not yet ported, but will be if/when the examples require them.

The gltools module is partially completed, and will be grown as required by the examples. Fortunately, Pyglet provides alternatives for handling media so, for example, the image file loading routines will not need porting.

The chapter examples and library APIs are purposely kept to resemble the original source. Some example code--vector get, set, and transform functions and the GLFrame methods to name a few--may resemble C++ too much for some Python enthusiasts, but this was a conscious choice to make it easier to follow them while studying the book and comparing with the original C++ source. Just keep in mind these are not necessarily best-practice (PEP8 and popular idioms) Python.

There are some gotchas to be aware of with Pyglet's exposure of OpenGL (pyglet.gl).

*   GL routines for setting light sources do not like math3d.M3DVector* types. They instead require ctypes arrays. Examples at present use the helper function vecf() at the top of most examples for this.
*   The GL routine glMultMatrix() does not like math3d.M3DVector* types. They instead requires list, numpy, or numeric arrays. Examples at present use list(some_m3dvector) for this.

Hope you enjoy this very slick programming environment: Pyglet, PyOpenGL, and OpenGL Superbible!

Gumm da Pythonator
