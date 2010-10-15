import math
from math import acos, cos, sin, sqrt


def vector_varargs(args, vector):
    if len(args) == len(vector):
        return args
    elif is_vector_compatible(args[0]) and len(args[0]) == len(vector):
        return args[0]
    else:
        raise VectorSizeError('%d values required' % (len(vector),))


def is_vector_compatible(obj):
    """Given content that can be converted to float, these are the types
    that are compatible with M3Vector*: list, tuple, str, and objects
    that define the __iter__ method.
    """
    return isinstance(obj, (list,tuple,str)) or hasattr(obj, '__iter__')


class VectorSizeError(Exception):
    def __init__(self, message):
        self.value = message
    def __str__(self):
        return str(self.value)



class _M3DVector(object):
    """Base class for M3DVector* classes."""
    __slots__ = ['__data','__iteri','__length']
    def __init__(self, length, *args):
        """Constructor requires the number of arguments specified by the
        subclass's __length attribute. The constructor will accept either an
        iterable container object or the required number of arguments, which
        values can be any that will convert to type float.
        
        If vector values are not specified in args, the values default to
        0.0.
        
        For typical OpenGL use the values should be between -1.0 and 1.0.
        Otherwise, some Trigonometric functions will raise a domain error.
        
        For example, the following constructions are equivalent:
            M3DVector3f(0.0, 0.0, 1.0)
            M3DVector3f(0, 0, 1)
            M3DVector3f((0, 0, 1))
            M3DVector3f([0, 0, 1])
            M3DVector3f('0.0', '0.0', '1.0')
            M3DVector3f('0', '0', '1')
            M3DVector3f('001')
            M3DVector3f(m3d_vector_3f_object)
        ]"""
        self.__length = length
        if len(args) == 0:
            args = [0]*length
        else:
            args = vector_varargs(args, self)
        self.__data = [float(n) for n in args]
    # Container methods.
    def __getitem__(self, i): return self.__data[i]
    def __setitem__(self, i, v): self.__data[i] = float(v)
    def __delitem__(self, i): raise VectorSizeError('operation would change size')
    def __getslice__(self, i, j): return self.__data[i:j]
    def __setslice__(self, i, j, sequence):
        if len(self.__data[i:j]) != len(sequence):
            raise VectorSizeError('operation would change size')
        self.__data[i:j] = [float(v) for v in sequence]
    def __delslice__(self, i, j): raise VectorSizeError('operation would change size')
    def __len__(self): return self.__length
    def __iter__(self):
        self.__iteri = 0
        return self
    def next(self):
        if self.__iteri >= len(self.__data):
            raise StopIteration
        v = self.__data[self.__iteri]
        self.__iteri += 1
        return v
    # Display methods.
    def __str__(self): return str(self.__data)
    # Logic methods.
    def __lt__(self, other): return self.__data < other[:]
    def __le__(self, other): return self.__data <= other[:]
    def __eq__(self, other): return self.__data == other[:]
    def __ne__(self, other): return self.__data != other[:]
    def __gt__(self, other): return self.__data > other[:]
    def __ge__(self, other): return self.__data >= other[:]
    def __cmp__(self, other): return cmp(self.__data, other[:])
    def __nonzero__(self): return all([n != None for n in self.__data])
    # Unary methods.
    def __neg__(self): return self.__class__([-v for v in self.__data])
    def __pos__(self): return self.__class__([+v for v in self.__data])
    def __abs__(self): return self.__class__([abs(v) for v in self.__data])
    def __invert__(self): ~self[0]  ## Not valid: raises TypeError
    # Math methods.
    def __add__(self, other): return self.__class__([v+other[i] for i,v in enumerate(self.__data)])
    def __sub__(self, other): return self.__class__([v-other[i] for i,v in enumerate(self.__data)])
    def __mul__(self, other): return self.__class__([v*other[i] for i,v in enumerate(self.__data)])
    def __div__(self, other): return self.__class__([v/other[i] for i,v in enumerate(self.__data)])
    def __radd__(self, other): return self + other
    def __rsub__(self, other): return self - other
    def __rmul__(self, other): return self * other
    def __rdiv__(self, other): return self / other
    def __iadd__(self, other): self[:] = [v+other[i] for i,v in enumerate(self.__data)]; return self
    def __isub__(self, other): self[:] = [v-other[i] for i,v in enumerate(self.__data)]; return self
    def __imul__(self, other): self[:] = [v*other[i] for i,v in enumerate(self.__data)]; return self
    def __idiv__(self, other): self[:] = [v/other[i] for i,v in enumerate(self.__data)]; return self
    # Conversion methods.
    def int(self): return [int(i) for i in self.__data]
    def long(self): return [long(i) for i in self.__data]


# Data structures and containers
# Much thought went into how these are declared. Many libraries declare these
# as structures with x, y, z data members. However structure alignment issues
# could limit the portability of code based on such structures, or the binary
# compatibility of data files (more likely) that contain such structures across
# compilers/platforms. Arrays are always tightly packed, and are more efficient 
# for moving blocks of data around (usually).
#typedef float	M3DVector3f[3];		// Vector of three floats (x, y, z)
#typedef double	M3DVector3d[3];		// Vector of three doubles (x, y, z)
class M3DVector3f(_M3DVector):
    __slots__ = 'xyz'
    def __init__(self, *args):
        _M3DVector.__init__(self, 3, *args)
    @property
    def x(self):
        return self[0]
    @x.setter
    def x(self, v):
     self[0] = v
    @property
    def y(self):
        return self[1]
    @y.setter
    def y(self, v):
        self[1] = v
    @property
    def z(self):
        return self[2]
    @z.setter
    def z(self, v):
        self[2] = v

class M3DVector3d(_M3DVector):
    __slots__ = 'xyz'
    def __init__(self, *args):
        _M3DVector.__init__(self, 3, *args)
    @property
    def x(self):
        return self[0]
    @x.setter
    def x(self, v):
     self[0] = v
    @property
    def y(self):
        return self[1]
    @y.setter
    def y(self, v):
        self[1] = v
    @property
    def z(self):
        return self[2]
    @z.setter
    def z(self, v):
        self[2] = v

#typedef float M3DVector4f[4];		// Lesser used... Do we really need these?
#typedef double M3DVector4d[4];		// Yes, occasionaly
class M3DVector4f(_M3DVector):
    __slots__ = 'xyzw'
    def __init__(self, *args):
        _M3DVector.__init__(self, 4, *args)
    @property
    def x(self):
        return self[0]
    @x.setter
    def x(self, v):
     self[0] = v
    @property
    def y(self):
        return self[1]
    @y.setter
    def y(self, v):
        self[1] = v
    @property
    def z(self):
        return self[2]
    @z.setter
    def z(self, v):
        self[2] = v
    @property
    def w(self):
        return self[3]
    @w.setter
    def w(self, v):
        self[3] = v

class M3DVector4d(_M3DVector):
    __slots__ = 'xyzw'
    def __init__(self, *args):
        _M3DVector.__init__(self, 4, *args)
    @property
    def x(self):
        return self[0]
    @x.setter
    def x(self, v):
     self[0] = v
    @property
    def y(self):
        return self[1]
    @y.setter
    def y(self, v):
        self[1] = v
    @property
    def z(self):
        return self[2]
    @z.setter
    def z(self, v):
        self[2] = v
    @property
    def w(self):
        return self[3]
    @w.setter
    def w(self, v):
        self[3] = v

#typedef float M3DVector2f[2];		// 3D points = 3D Vectors, but we need a
#typedef double M3DVector2d[2];		// 2D representations sometimes... (x,y) order
class M3DVector2f(_M3DVector):
    __slots__ = 'xy'
    def __init__(self, *args):
        _M3DVector.__init__(self, 2, *args)
    @property
    def x(self):
        return self[0]
    @x.setter
    def x(self, v):
     self[0] = v
    @property
    def y(self):
        return self[1]
    @y.setter
    def y(self, v):
        self[1] = v

class M3DVector2d(_M3DVector):
    __slots__ = 'xy'
    def __init__(self, *args):
        _M3DVector.__init__(self, 2, *args)
    @property
    def x(self):
        return self[0]
    @x.setter
    def x(self, v):
     self[0] = v
    @property
    def y(self):
        return self[1]
    @y.setter
    def y(self, v):
        self[1] = v


# 3x3 matrix - column major. X vector is 0, 1, 2, etc.
#		0	3	6	
#		1	4	7
#		2	5	8
class M3DMatrix33f(_M3DVector):
    __slots__ = 'abcdefghi'
    def __init__(self, *args):
        _M3DVector.__init__(self, 9, *args)
class M3DMatrix33d(_M3DVector):
    __slots__ = 'abcdefghi'
    def __init__(self, *args):
        _M3DVector.__init__(self, 9, *args)

# 4x4 matrix - column major. X vector is 0, 1, 2, etc.
#	0	4	8	12
#	1	5	9	13
#	2	6	10	14
#	3	7	11	15
class M3DMatrix44f(_M3DVector):
    __slots__ = 'abcdefghijklmnop'
    def __init__(self, *args):
        _M3DVector.__init__(self, 16, *args)
class M3DMatrix44d(_M3DVector):
    __slots__ = 'abcdefghijklmnop'
    def __init__(self, *args):
        _M3DVector.__init__(self, 16, *args)

# Useful constants
M3D_PI = math.pi
M3D_2PI = 2.0 * math.pi
M3D_PI_DIV_180 = math.pi / 180.0
M3D_INV_PI_DIV_180 = 180.0 / math.pi

# Useful shortcuts and macros
# Radians are king... but we need a way to swap back and forth
m3dDegToRad = lambda x: x * M3D_PI_DIV_180
m3dRadToDeg = lambda x: x * M3D_INV_PI_DIV_180

# Hour angles
m3dHrToDeg = lambda x: x * 15.0
m3dHrToRad = lambda x: m3dDegToRad(m3dHrToDeg(x))

m3dDegToHr = lambda x: x / 15.0
m3dRadToHr = lambda x: m3dDegToHr(m3dRadToDeg(x))

# Returns the same number if it is a power of
# two. Returns a larger integer if it is not a 
# power of two. The larger integer is the next
# highest power of two.
def m3dIsPOW2(iValue):
    nPow2 = 1
    while iValue > nPow2:
        nPow2 = nPow2 << 1
    return nPow2

# Inline accessor functions for people who just can't count to 3 - Vectors
m3dGetVectorX = lambda v: v[0]
m3dGetVectorY = lambda v: v[1]
m3dGetVectorZ = lambda v: v[2]
m3dGetVectorW = lambda v: v[3]

def m3dSetVectorX(v, x): v[0] = x
def m3dSetVectorY(v, y): v[1] = y
def m3dSetVectorZ(v, z): v[2] = z
def m3dSetVectorW(v, w): v[3] = w

# Inline vector functions
# Load Vector with (x, y, z, w).
def m3dLoadVector2(v, x, y): v[:] = x,y
def m3dLoadVector3(v, x, y, z): v[:] = x,y,z
def m3dLoadVector4(v, x, y, z, w): v[:] = x,y,z,w

# Copy vector src into vector dst
def m3dCopyVector2(dst, src): dst[:] = src[:]
def m3dCopyVector3(dst, src): dst[:] = src[:]
def m3dCopyVector4(dst, src): dst[:] = src[:]

# Add Vectors (r, a, b) r = a + b
def m3dAddVectors2(r, a, b):
    r[:] = [a[i]+b[i] for i in range(len(a))]
def m3dAddVectors3(r, a, b):
    r[:] = [a[i]+b[i] for i in range(len(a))]
def m3dAddVectors4(r, a, b):
    r[:] = [a[i]+b[i] for i in range(len(a))]

# Subtract Vectors (r, a, b) r = a - b
def m3dSubtractVectors2(r, a, b):
    r[:] = [a[i]-b[i] for i in range(len(a))]
def m3dSubtractVectors3(r, a, b):
    r[:] = [a[i]-b[i] for i in range(len(a))]
def m3dSubtractVectors4(r, a, b):
    r[:] = [a[i]-b[i] for i in range(len(a))]

# Scale Vectors (in place)
def m3dScaleVectors2(v, scale):
    v[:] = [n*scale for n in v]
def m3dScaleVectors3(v, scale):
    v[:] = [n*scale for n in v]
def m3dScaleVectors4(v, scale):
    v[:] = [n*scale for n in v]

# Cross Product - computes the vector perpendicular to the plane defined by two
# vectors.
# u x v = result
# We only need one version for floats, and one version for doubles. A 3 component
# vector fits in a 4 component vector. If  M3DVector4d or M3DVector4f are passed
# we will be OK because 4th component is not used.
def m3dCrossProduct(result, u, v):
    result[0] = u[1]*v[2] - v[1]*u[2]
    result[1] = -u[0]*v[2] + v[0]*u[2]
    result[2] = u[0]*v[1] - v[0]*u[1]

# Dot Product, only for three component vectors - returns the cosine between two
# vectors.
# return u dot v
def m3dDotProduct(u, v):
    return u[0]*v[0] + u[1]*v[1] + u[2]*v[2]

# Scale Vectors (in place)
def m3dScaleVector2(v, scale):
    v[:] = [n * scale for n in v]
def m3dScaleVector3(v, scale):
    v[:] = [n * scale for n in v]
def m3dScaleVector4(v, scale):
    v[:] = [n * scale for n in v]

# Angle between vectors, only for three component vectors. Angle is in radians...
def m3dGetAngleBetweenVectors(u, v):
    d = m3dDotProduct(u, v)
    return acos(d)

# Get Square of a vectors length
# Only for three component vectors
def m3dGetVectorLengthSquared(u):
    return (u[0] * u[0]) + (u[1] * u[1]) + (u[2] * u[2])

# Get length of vector
# Only for three component vectors.
def m3dGetVectorLength(u):
    return sqrt(m3dGetVectorLengthSquared(u))

# Normalize a vector
# Scale a vector to unit length. Easy, just scale the vector by it's length
def m3dNormalizeVector(u):
    m3dScaleVector3(u, 1.0 / m3dGetVectorLength(u))

# Get/Set Column.
def m3dGetMatrixColumn33(dst, src, column):
    off = 3 * column
    dst[0:3] = src[off:off+3]

def m3dSetMatrixColumn33(dst, src, column):
    off = 3 * column
    dst[off:off+3] = src[0:3]

def m3dGetMatrixColumn44(dst, src, column):
    off = 4 * column
    dst[0:3] = src[off:off+3]

def m3dSetMatrixColumn44(dst, src, column):
    off = 4 * column
    dst[off:off+3] = src[0:3]

def m3dGetPlaneEquation(planeEq, p1, p2, p3):
    """Get plane equation from three points and a normal,
    Calculate the plane equation of the plane that the three specified
    points lay in. The points are given in clockwise winding order, with
    normal pointing out of clockwise face planeEq contains the A,B,C, and D
    of the plane equation coefficients.
    """
    # Get two vectors... do the cross product
    v1 = M3DVector3f()
    v2 = M3DVector3f()

    # V1 = p3 - p1
    v1[0] = p3[0] - p1[0]
    v1[1] = p3[1] - p1[1]
    v1[2] = p3[2] - p1[2]

    # V2 = P2 - p1
    v2[0] = p2[0] - p1[0]
    v2[1] = p2[1] - p1[1]
    v2[2] = p2[2] - p1[2]

    # Unit normal to plane - Not sure which is the best way here
    m3dCrossProduct(planeEq, v1, v2)
    m3dNormalizeVector(planeEq)
    # Back substitute to get D
    planeEq[3] = -(planeEq[0] * p3[0] + planeEq[1] * p3[1] + planeEq[2] * p3[2])

def m3dMakePlanarShadowMatrix(proj, planeEq, vLightPos):
    """Create a projection to "squish" an object into the plane.
    Use m3dGetPlaneEquationf(planeEq, point1, point2, point3) to get a
    plane equation.
    """
    # These just make the code below easier to read. They will be 
    # removed by the optimizer.	
    a = planeEq[0]
    b = planeEq[1]
    c = planeEq[2]
    d = planeEq[3]

    dx = -vLightPos[0]
    dy = -vLightPos[1]
    dz = -vLightPos[2]

    # Now build the projection matrix
    proj[0] = b * dy + c * dz
    proj[1] = -a * dy
    proj[2] = -a * dz
    proj[3] = 0.0

    proj[4] = -b * dx
    proj[5] = a * dx + c * dz
    proj[6] = -b * dz
    proj[7] = 0.0

    proj[8] = -c * dx
    proj[9] = -c * dy
    proj[10] = a * dx + b * dy
    proj[11] = 0.0

    proj[12] = -d * dx
    proj[13] = -d * dy
    proj[14] = -d * dz
    proj[15] = a * dx + b * dy + c * dz
    # Shadow matrix ready

# LoadIdentity
# For 3x3 and 4x4 float and double matricies.
# 3x3 float
def m3dLoadIdentity33(m):
    # Don't be fooled, this is still column major
    identity = M3DMatrix33f(
        1.0, 0.0, 0.0,
        0.0, 1.0, 0.0,
        0.0, 0.0, 1.0)
    m[:]  = identity

# 4x4 float
def m3dLoadIdentity44(m):
    # Don't be fooled, this is still column major
    identity = M3DMatrix44f(
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0)
    m[:] = identity

# Transform - Does rotation and translation via a 4x4 matrix. Transforms
# a point or vector.
def m3dTransformVector3(vOut3f, v3f, m33f):
    vOut3f[0] = m33f[0] * v3f[0] + m33f[4] * v3f[1] + m33f[8] *  v3f[2] + m33f[12]
    vOut3f[1] = m33f[1] * v3f[0] + m33f[5] * v3f[1] + m33f[9] *  v3f[2] + m33f[13]
    vOut3f[2] = m33f[2] * v3f[0] + m33f[6] * v3f[1] + m33f[10] * v3f[2] + m33f[14]

def m3dTransformVector4(vOut4f, v4f, m44f):
    vOut4f[0] = m44f[0] * v4f[0] + m44f[4] * v4f[1] + m44f[8] *  v4f[2] + m44f[12] * v4f[3]
    vOut4f[1] = m44f[1] * v4f[0] + m44f[5] * v4f[1] + m44f[9] *  v4f[2] + m44f[13] * v4f[3]
    vOut4f[2] = m44f[2] * v4f[0] + m44f[6] * v4f[1] + m44f[10] * v4f[2] + m44f[14] * v4f[3]
    vOut4f[3] = m44f[3] * v4f[0] + m44f[7] * v4f[1] + m44f[11] * v4f[2] + m44f[15] * v4f[3]

# Creates a 3x3 rotation matrix, takes radians NOT degrees
def m3dRotationMatrix33(m, angle, x, z):

    s = float(sin(angle))
    c = float(cos(angle))

    mag = float(sqrt( x*x + y*y + z*z ))

    # Identity matrix
    if mag == 0.0:
        m3dLoadIdentity33(m)

    # Rotation matrix is normalized
    x /= mag
    y /= mag
    z /= mag

    xx = x * x
    yy = y * y
    zz = z * z
    xy = x * y
    yz = y * z
    zx = z * x
    xs = x * s
    ys = y * s
    zs = z * s
    one_c = 1.0 - c

    def M33(row,col,val): m[col*4+row] = val

    M33(0,0, (one_c * xx) + c)
    M33(0,1, (one_c * xy) - zs)
    M33(0,2, (one_c * zx) + ys)

    M33(1,0, (one_c * xy) + zs)
    M33(1,1, (one_c * yy) + c)
    M33(1,2, (one_c * yz) - xs)

    M33(2,0, (one_c * zx) - ys)
    M33(2,1, (one_c * yz) + xs)
    M33(2,2, (one_c * zz) + c)

# Creates a 4x4 rotation matrix, takes radians NOT degrees
def m3dRotationMatrix44(m, angle, x, y, z):
    s = float(sin(angle))
    c = float(cos(angle))

    mag = float(sqrt( x*x + y*y + z*z ))

    # Identity matrix
    if mag == 0.0:
        m3dLoadIdentity44(m)

    # Rotation matrix is normalized
    x /= mag
    y /= mag
    z /= mag

    xx = x * x
    yy = y * y
    zz = z * z
    xy = x * y
    yz = y * z
    zx = z * x
    xs = x * s
    ys = y * s
    zs = z * s
    one_c = 1.0 - c

    def M(row,col,val): m[col*4+row] = val

    M(0,0, (one_c * xx) + c)
    M(0,1, (one_c * xy) - zs)
    M(0,2, (one_c * zx) + ys)
    M(0,3, 0.0)

    M(1,0, (one_c * xy) + zs)
    M(1,1, (one_c * yy) + c)
    M(1,2, (one_c * yz) - xs)
    M(1,3, 0.0)

    M(2,0, (one_c * zx) - ys)
    M(2,1, (one_c * yz) + xs)
    M(2,2, (one_c * zz) + c)
    M(2,3, 0.0)

    M(3,0, 0.0)
    M(3,1, 0.0)
    M(3,2, 0.0)
    M(3,3, 1.0)

# Calculates the normal of a triangle specified by the three points
# p1, p2, and p3. Each pointer points to an array of three floats. The
# triangle is assumed to be wound counter clockwise. 
def m3dFindNormal(result, point1, point2, point3):
    # Temporary vectors
    v1 = M3DVector3f()
    v2 = M3DVector3f()

    # Calculate two vectors from the three points. Assumes counter clockwise
    # winding!
    v1[0] = point1[0] - point2[0]
    v1[1] = point1[1] - point2[1]
    v1[2] = point1[2] - point2[2]

    v2[0] = point2[0] - point3[0]
    v2[1] = point2[1] - point3[1]
    v2[2] = point2[2] - point3[2]

    # Take the cross product of the two vectors to get
    # the normal vector.
    m3dCrossProduct(result, v1, v2)


if __name__ == '__main__':
    def _assert_float(v):
        assert all(isinstance(n, float) for n in v)
    
    print '_M3DVector constructor args default to zero'
    v = M3DVector3f(); assert v == [0,0,0]; _assert_float(v)
    
    print '_M3DVector constructor accepts various forms'
    v = M3DVector3f(0.0, 0.0, 1.0); assert v == [0,0,1]; _assert_float(v)
    v = M3DVector3f(0, 0, 1); assert v == [0,0,1]; _assert_float(v)
    v = M3DVector3f((0, 0, 1)); assert v == [0,0,1]; _assert_float(v)
    v = M3DVector3f([0, 0, 1]); assert v == [0,0,1]; _assert_float(v)
    v = M3DVector3f('0.0', '0.0', '1.0'); assert v == [0,0,1]; _assert_float(v)
    v = M3DVector3f('0', '0', '1'); assert v == [0,0,1]; _assert_float(v)
    v = M3DVector3f('001'); assert v == [0,0,1]; _assert_float(v)
    v = M3DVector3f(v); assert v == [0,0,1]; _assert_float(v)
    v = M3DVector3f(range(3)); assert v == [0,1,2]; _assert_float(v)
    v = M3DVector3f(*range(3)); assert v == [0,1,2]; _assert_float(v)
    
    print '_M3DVector does conversion from int, long, str'
    assert M3DVector3f(int(0),int(1),int(2)) == [0,1,2]; _assert_float(v)
    assert M3DVector3f(long(0),long(1),long(2)) == [0,1,2]; _assert_float(v)
    assert M3DVector3f(str(0),str(1),str(2)) == [0,1,2]; _assert_float(v)
    v[0] = int(0); _assert_float(v)
    v[0] = long(0); _assert_float(v)
    v[0] = str(0); _assert_float(v)
    
    print '_M3DVector does conversion to list of int, long'
    assert all(isinstance(n, int) for n in v.int()); _assert_float(v)
    assert all(isinstance(n, long) for n in v.long()); _assert_float(v)
    
    print '_M3DVector does comparisons'
    assert v == [0.0,1.0,2.0]; _assert_float(v)
    assert v == [0,1,2]; _assert_float(v)
    assert v != [1.0,1.0,1.0]; _assert_float(v)
    assert v != [1,1,1]; _assert_float(v)
    assert v >= [0,1,2]; _assert_float(v)
    assert v > [0,0,0]; _assert_float(v)
    assert v <= [0,1,2]; _assert_float(v)
    assert v < [2,2,2]; _assert_float(v)

    print '_M3DVector does unary operators'
    v = -v; assert v == [-0,-1,-2]; _assert_float(v)
    v = +v; assert v == [-0,-1,-2]; _assert_float(v)
    v = abs(v); assert v == [0,1,2]; _assert_float(v)
    try: v = ~v; print '~v (__invert__) is not working!!'
    except TypeError: assert v == [0,1,2]; _assert_float(v); print '  except for ~v'

    print '_M3DVector does math'
    assert v + [1,1,1] == [1,2,3]; _assert_float(v)
    assert v - [1,1,1] == [-1,0,1]; _assert_float(v)
    assert v * [2,2,2] == [0,2,4]; _assert_float(v)
    assert v / [2,2,2] == [0,.5,1]; _assert_float(v)
    
    print '_M3DVector does in-place math'
    v[:] = [0,1,2]; _assert_float(v)
    v += [1,1,1]; assert v == [1,2,3]; _assert_float(v)
    v -= [1,1,1]; assert v == [0,1,2]; _assert_float(v)
    v *= [2,2,2]; assert v == [0,2,4]; _assert_float(v)
    v /= [2,2,2]; assert v == [0,1,2]; _assert_float(v)
    
    print '_M3DVector does indices and slices'
    assert v[0] == 0; _assert_float(v)
    assert v[0:2] == [0,1]; _assert_float(v)
    v[0] = 1; assert v == [1,1,2]; _assert_float(v)
    v[0:2] = [0,2]; assert v == [0,2,2]; _assert_float(v)
    v[:] = [0,1,2]; assert v == [0,1,2]; _assert_float(v)
    
    print '_M3DVector enforces size in constructor, slices, and array operations'
    try: v = M3DVector3f(1,2); print 'constructor size enforcement not working!!'
    except VectorSizeError, e: assert v == [0,1,2]; _assert_float(v); print '  constructor:',e
    try: v = M3DVector3f([1,2,3,4]); print 'constructor size enforcement not working!!'
    except VectorSizeError, e: assert v == [0,1,2]; _assert_float(v); print '  constructor:',e
    try: v[0:2] = [1]; print '__setslice__ not working!!'
    except VectorSizeError, e: assert v == [0,1,2]; _assert_float(v); print '  slice mismatch:',e
    try: del v[0]; print '__delitem__ not working!!'
    except VectorSizeError, e: assert v == [0,1,2]; _assert_float(v); print '  delete array item:',e
    try: del v[0:2]; print '__delslice__ not working!!'
    except VectorSizeError, e: assert v == [0,1,2]; _assert_float(v); print '  delete slice:',e
    
    print 'M3DVector2f supports x,y attributes'
    v = M3DVector2f(range(2)); assert v == [0,1]; _assert_float(v)
    v.x,v.y = range(2); assert v == [0,1]; _assert_float(v)
    assert [v.x,v.y] == [0,1];  _assert_float(v)
    
    print 'M3DVector3f supports x,y,z attributes'
    v = M3DVector3f(range(3)); assert v == [0,1,2]; _assert_float(v)
    v.x,v.y,v.z = range(3); assert v == [0,1,2]; _assert_float(v)
    assert [v.x,v.y,v.z] == [0,1,2];  _assert_float(v)

    print 'M3DVector4f supports x,y,z,w attributes'
    v = M3DVector4f(range(4)); assert v == [0,1,2,3]; _assert_float(v)
    v.x,v.y,v.z,v.w = range(4); assert v == [0,1,2,3]; _assert_float(v)
    assert [v.x,v.y,v.z,v.w] == [0,1,2,3];  _assert_float(v)

    print 'M3DMatrix33f for 3x3 matrix'
    M3DMatrix33f(*range(9))
    M3DMatrix33d(range(9))
    
    print 'M3DMatrix44f for 4x4 matrix'
    M3DMatrix44f(*range(16))
    M3DMatrix44f(range(16))

    print """
That's it for the vector class tests. There is a hodge-podge of other
functions for operating on vectors. A lot of it is carried over from
the C++ module, and can be accomplished much more elegantly with the
augmented Python classes M3DVector*. But, many demos use the C++-
style functions.
"""
