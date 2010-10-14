from math import cos, sin

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from math3d import *


# For best results, put this in a display list
# Draw a torus (doughnut)  at z = fZVal... torus is in xy plane
def gltDrawTorus(majorRadius, minorRadius, numMajor, numMinor):
    vNormal = M3DVector3f()
    majorStep = 2.0*M3D_PI / numMajor
    minorStep = 2.0*M3D_PI / numMinor
    
    for i in range(numMajor+1):
        a0 = i * majorStep
        a1 = a0 + majorStep
        x0 = cos(a0)
        y0 = sin(a0)
        x1 = cos(a1)
        y1 = sin(a1)
        
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(numMinor+1):
            b = j * minorStep
            c = cos(b)
            r = minorRadius * c + majorRadius
            z = minorRadius * sin(b)
            
            # First point
            glTexCoord2f(i/numMajor, j/numMinor)
            vNormal[0] = x0*c
            vNormal[1] = y0*c
            vNormal[2] = z/minorRadius
            m3dNormalizeVector(vNormal)
            glNormal3fv(list(vNormal))
            glVertex3f(x0*r, y0*r, z)
            
            glTexCoord2f((i+1)/numMajor, j/numMinor)
            vNormal[0] = x1*c
            vNormal[1] = y1*c
            vNormal[2] = z/minorRadius
            m3dNormalizeVector(vNormal)
            glNormal3fv(list(vNormal))
            glVertex3f(x1*r, y1*r, z)
        glEnd()
