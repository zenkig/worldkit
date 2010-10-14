"""
The GLFrame (OrthonormalFrame) class. Possibly the most useful little
piece of 3D graphics code for OpenGL immersive environments.
// Richard S. Wright Jr.
"""


from OpenGL.GL import *

from math3d import *


class GLFrame(object):

    origin = None	# Where am I?
    forward = None	# Where am I going?
    up = None		# Which way is up?

    # Default position and orientation. At the origin, looking
    # down the positive Z axis (right handed coordinate system).
    def __init__(self):
        # At origin
        self.origin = M3DVector3f(0.0, 0.0, 0.0)

        # Up is up (+Y)
        self.up = M3DVector3f(0.0, 1.0, 0.0)

        # Forward is -Z (default OpenGL)
        self.forward = M3DVector3f(0.0, 0.0, -1.0)


    # Set Location
    def SetOrigin(self, *args):
        """Set origin from args. args[0] is either a M3DVector3f object, or
        a sequence of length 3, or args[0:3] is x, y, and z points."""
        self.origin[:] = vector_varargs(args, self.origin)
        
    def GetOrigin(self, vector_point):
        """Copy origin into vector_point. vector_point is either a
        M3DVector* object or a mutable sequence."""
        vector_point[:] = self.origin

    def GetOriginX(self):
        return self.origin.x
    
    def GetOriginY(self):
        return self.origin.y
    
    def GetOriginZ(self):
        return self.origin.z

    # Set Forward Direction
    def SetForwardVector(self, *xyz):
        """Set direction from xyz. xyz[0] is either a M3DVector3f object, or
        a sequence of length 3, or xyz[0:3] is x, y, and z points."""
        self.forward[:] = vector_varargs(xyz, self.forward)

    def GetForwardVector(self, vector):
        vector[:] = self.forward

    # Set Up Direction
    def SetUpVector(self, *xyz):
        """Set up from xyz. xyz[0] is either a M3DVector3f object, or
        a sequence of length 3, or xyz[0:3] is x, y, and z points."""
        self.up[:] = vector_varargs(xyz, self.up)

    def GetUpVector(self, vector):
        vector[:] = self.up

    # Get Axes
    def GetZAxis(self, vector): self.GetForwardVector(vector)
    def GetYAxis(self, vector): self.GetUpVector(vector)
    def GetXAxis(self, vector): m3dCrossProduct(vector, self.up, self.forward)

    # Translate along orthonormal axis... world or local
    def TranslateWorld(self, *xyz):
        """Set up from xyz. xyz[0] is either a M3DVector3f object, or
        a sequence of length 3, or xyz[0:3] is x, y, and z points."""
        x,y,z = vector_varargs(xyz, self.origin)
        self.origin += (x,y,z)
    
    def TranslateLocal(self, *xyz):
        """Set up from xyz. xyz[0] is either a M3DVector3f object, or
        a sequence of length 3, or xyz[0:3] is x, y, and z points."""
        x,y,z = vector_varargs(xyz, self.origin)
        self.MoveForward(z); self.Up(y); self.MoveRight(x)

    # Move Forward (along Z axis)
    def MoveForward(self, delta):
        # Move along direction of front direction
        self.origin[:] += self.forward * ((delta,)*3)

    def MoveUp(self, delta):
        # Move along direction of up direction
        self.origin[:] += self.up * ((delta,)*3)
    
    def MoveRight(self, delta):
        cross = M3DVector3f()
        m3dCrossProduct(cross, self.up, self.forward)
        self.origin += cross * ((delta,)*3)

    # Just assemble the matrix
    def GetMatrix(self, matrix, rotation_only=False):
        """matrix is a M3DMatrix44f object."""
        # Calculate the right side (x) vector, drop it right into the matrix
        xaxis = M3DVector3f()
        m3dCrossProduct(xaxis, self.up, self.forward)
        # Set matrix column does not fill in the fourth value...
        m3dSetMatrixColumn44(matrix, xaxis, 0)
        matrix[3] = 0.0
        # Y Column
        m3dSetMatrixColumn44(matrix, self.up, 1)
        matrix[7] = 0.0
        # Z Column
        m3dSetMatrixColumn44(matrix, self.forward, 2)
        matrix[11] = 0.0
        # Translation (already done)
        if rotation_only == True:
            matrix[12] = 0.0
            matrix[13] = 0.0
            matrix[14] = 0.0
        else:
            m3dSetMatrixColumn44(matrix, self.origin, 3)
        matrix[15] = 1.0

    def GetCameraOrientation(self, m):
        """Copy camera location to m.
        m is a M3DMatrix44f object. Get a 4x4 transformation matrix that
        describes the camera orientation.
        """
        x = M3DVector3f()
        z = M3DVector3f()

        # Make rotation matrix
        # Z vector is reversed
        forward = self.forward
        z.x = -forward.x
        z.y = -forward.y
        z.z = -forward.z

        # X vector = Y cross Z 
        up = self.up
        m3dCrossProduct(x, up, z)

        # Matrix has no translation information and is
        # transposed.... (rows instead of columns)
        def M(row,col,val): m[col*4+row] = val
        M(0,0, x[0])
        M(0,1, x[1])
        M(0,2, x[2])
        M(0,3, 0.0)
        M(1,0, up[0])
        M(1,1, up[1])
        M(1,2, up[2])
        M(1,3, 0.0)
        M(2,0, z[0])
        M(2,1, z[1])
        M(2,2, z[2])
        M(2,3, 0.0)
        M(3,0, 0.0)
        M(3,1, 0.0)
        M(3,2, 0.0)
        M(3,3, 1.0)

    def ApplyCameraTransform(self, rot_only=False):
        """Perform viewing or modeling transformations.
        Position as the camera (for viewing). Apply this transformation
        first as your viewing transformation. The default implementation of
        gluLookAt can be considerably sped up since it uses doubles for
        everything... Then again profile before you tune... ;-) You might
        get a boost form page fault reduction too... If no other glu
        routines are used... This will get called once per frame.... Go
        ahead and inline.
        """
        m = M3DMatrix44f()

        self.GetCameraOrientation(m)
        
        # Camera Transform   
        glMultMatrixf(list(m))
    
        # If Rotation only, then do not do the translation
        if not rot_only:
            glTranslatef(*-self.origin);

        """
        /*gluLookAt(vOrigin[0], vOrigin[1], vOrigin[2],
                    vOrigin[0] + vForward[0], 
                    vOrigin[1] + vForward[1], 
                    vOrigin[2] + vForward[2], 
                    vUp[0], vUp[1], vUp[2]);
        */
        """

    def ApplyActorTransform(self, rotation_only=False):
        """Position as an object in the scene.
        This places and orients a coordinate frame for other objects
        (besides the camera). There is ample room for optimization
        here... This is going to be called alot... don't inline. Add flag
        to perform actor rotation only and not the translation.
        """
        rot_mat = M3DMatrix44f()
        self.GetMatrix(rot_mat, rotation_only);

        # Apply rotation to the current matrix
        glMultMatrixf(list(rot_mat))
        return rot_mat

    def RotateLocalX(self, angle):
        """Rotate around local X Axes - Note all rotations are in radians"""
        rot_mat = M3DMatrix44f()
        cross = M3DVector3f()
        m3dCrossProduct(cross, self.up, self.forward)
        m3dRotationMatrix44(rot_mat, angle, cross.x, cross.y, cross.z)

        new_vect = M3DVector3f('000')
        # Inline 3x3 matrix multiply for rotation only
        forward = self.forward
        new_vect[0] = rot_mat[0] * forward[0] + rot_mat[4] * forward[1] + rot_mat[8] *  forward[2]
        new_vect[1] = rot_mat[1] * forward[0] + rot_mat[5] * forward[1] + rot_mat[9] *  forward[2]
        new_vect[2] = rot_mat[2] * forward[0] + rot_mat[6] * forward[1] + rot_mat[10] * forward[2]
        forward[:] = new_vect

        # Update pointing up vector
        up = self.up
        new_vect[0] = rot_mat[0] * up[0] + rot_mat[4] * up[1] + rot_mat[8] *  up[2]
        new_vect[1] = rot_mat[1] * up[0] + rot_mat[5] * up[1] + rot_mat[9] *  up[2]
        new_vect[2] = rot_mat[2] * up[0] + rot_mat[6] * up[1] + rot_mat[10] * up[2]
        up[:] = new_vect

    def RotateLocalY(self, angle):
        """Rotate around local Y"""
        rot_mat = M3DMatrix44f()

        # Just Rotate around the up vector
        # Create a rotation matrix around my Up (Y) vector
        up = self.up
        m3dRotationMatrix44(rot_mat, angle, up[0], up[1], up[2])

        new_vect = M3DVector3f()

        # Rotate forward pointing vector (inlined 3x3 transform)
        forward = self.forward
        new_vect[0] = rot_mat[0] * forward[0] + rot_mat[4] * forward[1] + rot_mat[8] *  forward[2]
        new_vect[1] = rot_mat[1] * forward[0] + rot_mat[5] * forward[1] + rot_mat[9] *  forward[2]
        new_vect[2] = rot_mat[2] * forward[0] + rot_mat[6] * forward[1] + rot_mat[10] * forward[2]
        forward[:] = new_vect

    def RotateLocalZ(self, fAngle):
        """Rotate around local Z"""
        rot_mat = M3DMatrix44f()

        # Only the up vector needs to be rotated
        forward = self.forward
        m3dRotationMatrix44(rot_mat, fAngle, forward.x, forward.y, forward.z)

        new_vect = M3DVector3f()
        up = self.up
        new_vect[0] = rot_mat[0] * up[0] + rot_mat[4] * up[1] + rot_mat[8] *  up[2]
        new_vect[1] = rot_mat[1] * up[0] + rot_mat[5] * up[1] + rot_mat[9] *  up[2]
        new_vect[2] = rot_mat[2] * up[0] + rot_mat[6] * up[1] + rot_mat[10] * up[2]
        up[:] = new_vect

    def Normalize(self):
        """Reset axes to make sure they are orthonormal. This should be
        called on occasion if the matrix is long-lived and frequently
        transformed.
        """
        vCross = M3DVector3f()

        # Calculate cross product of up and forward vectors
        up = self.up
        forward = self.forward
        m3dCrossProduct(vCross, up, forward)

        # Use result to recalculate forward vector
        m3dCrossProduct(forward, vCross, up)

        # Also check for unit length...
        m3dNormalizeVector(up)
        m3dNormalizeVector(uorward)

    def RotateWorld(self, fAngle, x, y, z):
        """Rotate in world coordinates..."""
        rotMat = M3DMatrix44f()

        # Create the Rotation matrix
        m3dRotationMatrix44(rotMat, fAngle, x, y, z)

        newVect = M3DVector3f()
        
        # Transform the up axis (inlined 3x3 rotation)
        up = self.up
        newVect[0] = rotMat[0] * up.x + rotMat[4] * up.y + rotMat[8] *  up.z
        newVect[1] = rotMat[1] * up.x + rotMat[5] * up.y + rotMat[9] *  up.z
        newVect[2] = rotMat[2] * up.x + rotMat[6] * up.y + rotMat[10] * up.z
        m3dCopyVector3(up, newVect)

        # Transform the forward axis
        newVect[0] = rotMat[0] * vForward[0] + rotMat[4] * vForward[1] + rotMat[8] *  vForward[2];	
        newVect[1] = rotMat[1] * vForward[0] + rotMat[5] * vForward[1] + rotMat[9] *  vForward[2];	
        newVect[2] = rotMat[2] * vForward[0] + rotMat[6] * vForward[1] + rotMat[10] * vForward[2];	
        m3dCopyVector3(vForward, newVect);

    def RotateLocal(self, fAngle, x, y, z):
        """Rotate around a local axis"""
        vWorldVect = M3DVector3f()
        vLocalVect = M3DVector3f()
        m3dLoadVector3(vLocalVect, x, y, z)

        self.LocalToWorld(vLocalVect, vWorldVect)
        self.RotateWorld(fAngle, vWorldVect.x, vWorldVect.y, vWorldVect.z)

    def LocalToWorld(self, vLocal, vWorld):
        """Convert Coordinate Systems
        This is pretty much, do the transformation represented by the
        rotation and position on the point. Is it better to stick to the
        convention that the destination always comes first, or use the
        convention that "sounds" like the function...
        """
        # Create the rotation matrix based on the vectors
        rotMat = M3DMatrix44f()

        self.GetMatrix(rotMat, True)

        # Do the rotation (inline it, and remove 4th column...)
        vWorld[0] = rotMat[0] * vLocal[0] + rotMat[4] * vLocal[1] + rotMat[8] *  vLocal[2]
        vWorld[1] = rotMat[1] * vLocal[0] + rotMat[5] * vLocal[1] + rotMat[9] *  vLocal[2]
        vWorld[2] = rotMat[2] * vLocal[0] + rotMat[6] * vLocal[1] + rotMat[10] * vLocal[2]

        # Translate the point
        origin = self.origin
        vWorld[0] += origin.x
        vWorld[1] += origin.y
        vWorld[2] += origin.z

    def WorldToLocal(self, vWorld, vLocal):
        """Change world coordinates into "local" coordinates"""
        # Translate the origin
        vNewWorld = M3DVector3f()
        origin = self.origin
        vNewWorld[0] = vWorld[0] - origin.x
        vNewWorld[1] = vWorld[1] - origin.y
        vNewWorld[2] = vWorld[2] - origin.z

        # Create the rotation matrix based on the vectors
        rotMat = M3DMatrix44f()
        invMat = M3DMatrix44f()
        self.GetMatrix(rotMat, True)

        # Do the rotation based on inverted matrix
        m3dInvertMatrix44(invMat, rotMat)

        vLocal[0] = invMat[0] * vNewWorld[0] + invMat[4] * vNewWorld[1] + invMat[8] *  vNewWorld[2]
        vLocal[1] = invMat[1] * vNewWorld[0] + invMat[5] * vNewWorld[1] + invMat[9] *  vNewWorld[2]
        vLocal[2] = invMat[2] * vNewWorld[0] + invMat[6] * vNewWorld[1] + invMat[10] * vNewWorld[2]
    
    def TransformPoint(vPointSrc, vPointDst):
        """Transform a point by frame matrix"""
        m = M3DMatrix44f()
        self.GetMatrix(m, False)     # Rotate and translate
        vPointDst[0] = m[0] * vPointSrc[0] + m[4] * vPointSrc[1] + m[8] *  vPointSrc[2] + m[12] # * v[3]
        vPointDst[1] = m[1] * vPointSrc[0] + m[5] * vPointSrc[1] + m[9] *  vPointSrc[2] + m[13] # * v[3]
        vPointDst[2] = m[2] * vPointSrc[0] + m[6] * vPointSrc[1] + m[10] * vPointSrc[2] + m[14] # * v[3]
    
    def RotateVector(self, vVectorSrc, vVectorDst):
        """Rotate a vector by frame matrix"""
        m = M3DMatrix44f()
        self.GetMatrix(m, True)      # Rotate only
        vVectorDst[0] = m[0] * vVectorSrc[0] + m[4] * vVectorSrc[1] + m[8] *  vVectorSrc[2]
        vVectorDst[1] = m[1] * vVectorSrc[0] + m[5] * vVectorSrc[1] + m[9] *  vVectorSrc[2]
        vVectorDst[2] = m[2] * vVectorSrc[0] + m[6] * vVectorSrc[1] + m[10] * vVectorSrc[2]


if __name__ == '__main__':
    v = M3DVector3f(1,1,1)
    f = GLFrame()
    assert f.origin == [0.0, 0.0, 0.0]
    assert f.up == [0.0, 1.0, 0.0]
    assert f.forward == [0.0, 0.0, -1.0]
    
    print 'GLFrame set/get location'
    f.GetOrigin(v)
    assert v == [0.0, 0.0, 0.0]
    f.SetOrigin(1,1,1)
    assert f.origin == [1.0,1.0,1.0]
    f.SetOrigin([0,0,0])
    assert f.GetOriginX() == 0
    assert f.GetOriginY() == 0
    assert f.GetOriginZ() == 0
    
    print 'GLFrame set/get forward direction'
    f.GetForwardVector(v)
    assert v == [0.0, 0.0, -1.0]
    f.SetForwardVector(0,0,0)
    assert f.forward == [0,0,0]
    f.SetForwardVector((0,0,-1))
    assert f.forward == [0,0,-1]
    
    print 'GLFrame set/get up vector'
    f.GetUpVector(v)
    assert v == [0,1,0]
    f.SetUpVector(1,0,0)
    assert f.up == [1,0,0]
    f.SetUpVector((0,1,0))
    assert f.up == [0,1,0]
