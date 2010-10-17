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
    
    for i in range(numMajor):
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
            glTexCoord2f(float(i)/float(numMajor), float(j)/float(numMinor))
            vNormal.x = x0*c
            vNormal.y = y0*c
            vNormal.z = z/minorRadius
            m3dNormalizeVector(vNormal)
            glNormal3fv(list(vNormal))
            glVertex3f(x0*r, y0*r, z)
            
            glTexCoord2f(float(i+1)/float(numMajor), float(j)/float(numMinor))
            vNormal.x = x1*c
            vNormal.y = y1*c
            vNormal.z = z/minorRadius
            m3dNormalizeVector(vNormal)
            glNormal3fv(list(vNormal))
            glVertex3f(x1*r, y1*r, z)
        glEnd()

# For best results, put this in a display list
# Draw a sphere at the origin
def gltDrawSphere(fRadius, iSlices, iStacks):
    drho = 3.141592653589 / iStacks
    dtheta = 2.0 * 3.141592653589 / iSlices
    ds = 1.0 / iSlices
    dt = 1.0 / iStacks
    t = 1.0
    s = 0.0
    
    for i in range(iStacks):
        rho = i * drho;
        srho = sin(rho)
        crho = cos(rho)
        srhodrho = sin(rho + drho)
        crhodrho = cos(rho + drho)
        
        # Many sources of OpenGL sphere drawing code uses a triangle fan
        # for the caps of the sphere. This however introduces texturing 
        # artifacts at the poles on some OpenGL implementations
        glBegin(GL_TRIANGLE_STRIP)
        s = 0.0
        for j in range(iSlices+1):
            if j == iSlices:
                theta = 0.0
            else:
                theta = j * dtheta
            stheta = -sin(theta)
            ctheta = cos(theta)
            
            x = stheta * srho
            y = ctheta * srho
            z = crho
            
            glTexCoord2f(s, t)
            glNormal3f(x, y, z)
            glVertex3f(x * fRadius, y * fRadius, z * fRadius)
            
            x = stheta * srhodrho
            y = ctheta * srhodrho
            z = crhodrho
            glTexCoord2f(s, t - dt)
            s += ds
            glNormal3f(x, y, z)
            glVertex3f(x * fRadius, y * fRadius, z * fRadius)
        glEnd()

        t -= dt
