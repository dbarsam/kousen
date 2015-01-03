# -*- coding: utf-8 -*-
"""
This module provides all utility functions and class defintions for matrix operations.
"""

import math
import PySide.QtCore
from kousen.math.point import Point3D
from kousen.math.vector import Vector3D

class Matrix4x4(PySide.QtCore.QObject):
    """
    Matrix4x4 provides a simplified but self contained 4x4 Matrix class.

    @warning The Matrix4x4 is Column Major.
    """
    dataChanging = PySide.QtCore.Signal(object)
    dataChanged  = PySide.QtCore.Signal(object)

    def __init__(self):
        """
        Constructor.
        """
        super(Matrix4x4, self).__init__()
        self.init()

    def __repr__(self):
        """
        Generates the "official" string representation of the Matrix4x4

        @returns A string representation of the Matrix4x4
        """
        return "{0}{1}".format(self.__class__.__name__, self._data)

    def __str__(self):
        """
        Generates the "informal" string representation of the Matrix4x4.

        @returns A string representation of the Matrix4x4
        """
        return "{0[0]:5}, {0[4]:5}, {0[8]:5}, {0[12]:5}\n{0[1]:5}, {0[5]:5}, {0[9]:5}, {0[13]:5}\n{0[2]:5}, {0[6]:5}, {0[10]:5}, {0[14]:5}\n{0[3]:5}, {0[7]:5}, {0[11]:5}, {0[15]:5}".format(self._data)

    def __getitem__(self, key):
        """
        The [] operator getter.

        @param key The lookup index to the internal data.
        @returns      The data if the lookup operation was succesful; None otherwise.
        """
        if key >= len(self._data):
            raise IndexError()
        return self._data[key]

    def __setitem__(self, key, value):
        """
        The [] operator setter.

        @param key The lookup index to the internal data.
        @param value The lookup index to the internal data.
        """
        if key >= len(self._data):
            raise IndexError()
        self._dataChanging(key)
        self._data[key] = value
        self._dataChanged(key)

    def __iter__(self):
        """
        Return an iterator object.
        """
        return iter(self._data)

    def __hash__(self):
        """
        Calculates the hash value of the instance.

        @returns A hash value calcaulted from internal data.
        """
        return hash(tuple(self._data))

    def __setitem__(self, index, value):
        """
        The [] operator setter.

        @param index The lookup index to the internal data.
        @param value The value to apply.
        """
        if index < len(self._data):
            self._data[index] = value

    def __mul__(self, other):
        """
        Calculates the product of the
            1) Matrix Multiplication:         Product = Self * Matrix
            2) Matric Vector Multiplication:  Product = Self * Vector
            3) Matrix Point Multiplication:   Product = Self * Point

        @param   other An instance of a 1) Matrix4x4, 2) Vector3D, or 3) Point3D.
        @returns       The Matrix Product if Matrix multiplication; The Vector3D product if Matrix Vector multiplication; the Point3D product if Matrix Point multiplication; None otherwise.
        """
        if isinstance(other,Matrix4x4):
            return self.multMatrix(other)

        if isinstance(other,Vector3D):
            return self.multVector3D(other)

        if isinstance(other,Point3D):
            return self.multPoint3D(other)

        return None

    @classmethod
    def identity(cls):
        """
        Creates an Identity Matrix.
        """
        M = cls()
        M[ 0] = 1.0;   M[ 4] = 0.0;   M[ 8] = 0.0;   M[12] = 0.0;
        M[ 1] = 0.0;   M[ 5] = 1.0;   M[ 9] = 0.0;   M[13] = 0.0;
        M[ 2] = 0.0;   M[ 6] = 0.0;   M[10] = 1.0;   M[14] = 0.0;
        M[ 3] = 0.0;   M[ 7] = 0.0;   M[11] = 0.0;   M[15] = 1.0;
        return M

    @classmethod
    def translation( cls, vector3D ):
        """
        Creates a Translation Matrix from a Translation Vector3D.

        @param vector3D The translation Vector3D.
        @returns A Matrix4x4 Translation Matrix
        """
        M = cls()
        M[ 0] = 1.0;   M[ 4] = 0.0;   M[ 8] = 0.0;   M[12] = vector3D.x;
        M[ 1] = 0.0;   M[ 5] = 1.0;   M[ 9] = 0.0;   M[13] = vector3D.y;
        M[ 2] = 0.0;   M[ 6] = 0.0;   M[10] = 1.0;   M[14] = vector3D.z;
        M[ 3] = 0.0;   M[ 7] = 0.0;   M[11] = 0.0;   M[15] = 1.0;
        return M

    @classmethod
    def rotation( cls, angleInRadians, axisVector, originPoint = None ):
        """
        Creates a Axis-Angle Rotation Matrix from an Angle and Axis Vector.

        @param angleInRadians The angle (radians) of the Axis-Angle rotation.
        @param axisVector     The axis (normalized) of the Axis-Angle rotation.
        @param originPoint    The origin point of the Axis-Angle rotation; if None assume the origin (0,0,0).
        @returns A Matrix4x4 Rotation Matrix
        """
        # Note: assumes axisVector is normalized
        c = math.cos( angleInRadians )
        s = math.sin( angleInRadians )
        one_minus_c = 1-c
        xs = axisVector.x * s
        ys = axisVector.y * s
        zs = axisVector.z * s

        M = cls()
        M[ 0] = c + one_minus_c * axisVector.x*axisVector.x
        M[ 5] = c + one_minus_c * axisVector.y*axisVector.y
        M[10] = c + one_minus_c * axisVector.z*axisVector.z
        M[ 1] = M[ 4] = one_minus_c * axisVector.x*axisVector.y;
        M[ 2] = M[ 8] = one_minus_c * axisVector.x*axisVector.z;
        M[ 6] = M[ 9] = one_minus_c * axisVector.y*axisVector.z;

        M[ 1] += zs;  M[ 4] -= zs;
        M[ 2] -= ys;  M[ 8] += ys;
        M[ 6] += xs;  M[ 9] -= xs;

        M[12] = 0.0;
        M[13] = 0.0;
        M[14] = 0.0;
        M[ 3] = 0.0;   M[ 7] = 0.0;   M[11] = 0.0;   M[15] = 1.0;

        if originPoint:
            v = originPoint.toVector3D()
            return cls.translation(v) * M * cls.translation(-v)
        return M

    @classmethod
    def scale(cls, scaleFactor, originPoint = None):
        """
        Creates a Uniform Scale Matrix from an scalar factor.

        @param scaleFactor    The scalar factor of the scale.
        @param originPoint    The origin point of the scale; if None assume the origin (0,0,0).
        @returns A Matrix4x4 Rotation Matrix
        """
        M = cls()
        M[ 0] = scaleFactor; M[ 4] = 0.0;         M[ 8] = 0.0;         M[12] = 0.0;
        M[ 1] = 0.0;         M[ 5] = scaleFactor; M[ 9] = 0.0;         M[13] = 0.0;
        M[ 2] = 0.0;         M[ 6] = 0.0;         M[10] = scaleFactor; M[14] = 0.0;
        M[ 3] = 0.0;         M[ 7] = 0.0;         M[11] = 0.0;         M[15] = 1.0;

        if originPoint:
            v = originPoint.toVector3D()
            return cls.translation(v) * M * cls.translation(-v)
        return M

    @classmethod
    def lookAt( cls, eyePoint, targetPoint, upVector, isInverted ):
        """
        Creates a 'LookAt' Matrix.

        @param eyePoint     The origin of the camera.
        @param targetPoint  The 'look at' point
        @param upVector     The up vector of the camera.
        @param isInverted   The inverted flag.
        @returns            A Matrix4x4 LookAt Matrix
        @see http://www.opengl.org/archives/resources/faq/technical/lookat.cpp
        @see http://stackoverflow.com/questions/349050/calculating-a-lookat-matrix
        @see http://processing.org/reference/camera_.html
        @see http://www.cs.rutgers.edu/~decarlo/428/glu_man/lookat.html
        """
        # step one: generate a rotation matrix

        # Compute our new look at vector, which will be the new Z axis of our transformed object.
        z = (eyePoint-targetPoint).normalized()
        y = upVector
        x = y ^ z   # cross product
        y = z ^ x   # cross product

        # Cross product gives area of parallelogram, which is < 1 for
        # non-perpendicular unit-length vectors; so normalize x and y.
        x = x.normalized()
        y = y.normalized()

        M = cls()

        if isInverted :
            # the rotation matrix
            M[ 0] = x.x;   M[ 4] = y.x;   M[ 8] = z.x;   M[12] = 0.0;
            M[ 1] = x.y;   M[ 5] = y.y;   M[ 9] = z.y;   M[13] = 0.0;
            M[ 2] = x.z;   M[ 6] = y.z;   M[10] = z.z;   M[14] = 0.0;
            M[ 3] = 0.0;   M[ 7] = 0.0;   M[11] = 0.0;   M[15] = 1.0;

            # step two: premultiply by a translation matrix
            return cls.translation( eyePoint.toVector3D() ) * M

        # the rotation matrix
        M[ 0] = x.x;   M[ 4] = x.y;   M[ 8] = x.z;   M[12] = 0.0;
        M[ 1] = y.x;   M[ 5] = y.y;   M[ 9] = y.z;   M[13] = 0.0;
        M[ 2] = z.x;   M[ 6] = z.y;   M[10] = z.z;   M[14] = 0.0;
        M[ 3] = 0.0;   M[ 7] = 0.0;   M[11] = 0.0;   M[15] = 1.0;

        # step two: postmultiply by a translation matrix
        return M * cls.translation( - eyePoint.toVector3D() )

    def _dataChanging(self, index):
        """
        Internal method to emit the DataChanging signal.
        """
        self.dataChanging.emit(index)

    def _dataChanged(self, index):
        """
        Internal method to emit the DataChanged signal.
        """
        self.dataChanged.emit(index)

    def data(self):
        """
        Accessor method to access the raw data

        @returns The list of values
        """
        return self._data

    def duplicate(self):
        """
        Copy Constructor.

        @returns Another Matrix4x4 with the same values as self
        """
        M = self.__class__()
        M._data = list(self._data)
        return M

    def init(self):
        """
        Initializes the internal data to the Identity Matrix.
        """
        self._data = [ 1.0, 0.0, 0.0, 0.0,
                   0.0, 1.0, 0.0, 0.0,
                   0.0, 0.0, 1.0, 0.0,
                   0.0, 0.0, 0.0, 1.0 ]

    def multMatrix(self, other):
        """
        Calculates the product of the Matrix Multiplication Product = Self * Matrix

        @param   other An instance of a Matrix4x4.
        @returns       The Matrix Product of the Matrix multiplication.
        """
        # Convenience Variables:
        a = self
        b = other

        M = self.__class__()
        M[ 0] = a[ 0] * b[ 0]  +  a[ 4] * b[ 1]  +  a[ 8] * b[ 2]  +  a[12] * b[ 3]
        M[ 1] = a[ 1] * b[ 0]  +  a[ 5] * b[ 1]  +  a[ 9] * b[ 2]  +  a[13] * b[ 3]
        M[ 2] = a[ 2] * b[ 0]  +  a[ 6] * b[ 1]  +  a[10] * b[ 2]  +  a[14] * b[ 3]
        M[ 3] = a[ 3] * b[ 0]  +  a[ 7] * b[ 1]  +  a[11] * b[ 2]  +  a[15] * b[ 3]

        M[ 4] = a[ 0] * b[ 4]  +  a[ 4] * b[ 5]  +  a[ 8] * b[ 6]  +  a[12] * b[ 7]
        M[ 5] = a[ 1] * b[ 4]  +  a[ 5] * b[ 5]  +  a[ 9] * b[ 6]  +  a[13] * b[ 7]
        M[ 6] = a[ 2] * b[ 4]  +  a[ 6] * b[ 5]  +  a[10] * b[ 6]  +  a[14] * b[ 7]
        M[ 7] = a[ 3] * b[ 4]  +  a[ 7] * b[ 5]  +  a[11] * b[ 6]  +  a[15] * b[ 7]

        M[ 8] = a[ 0] * b[ 8]  +  a[ 4] * b[ 9]  +  a[ 8] * b[10]  +  a[12] * b[11]
        M[ 9] = a[ 1] * b[ 8]  +  a[ 5] * b[ 9]  +  a[ 9] * b[10]  +  a[13] * b[11]
        M[10] = a[ 2] * b[ 8]  +  a[ 6] * b[ 9]  +  a[10] * b[10]  +  a[14] * b[11]
        M[11] = a[ 3] * b[ 8]  +  a[ 7] * b[ 9]  +  a[11] * b[10]  +  a[15] * b[11]

        M[12] = a[ 0] * b[12]  +  a[ 4] * b[13]  +  a[ 8] * b[14]  +  a[12] * b[15]
        M[13] = a[ 1] * b[12]  +  a[ 5] * b[13]  +  a[ 9] * b[14]  +  a[13] * b[15]
        M[14] = a[ 2] * b[12]  +  a[ 6] * b[13]  +  a[10] * b[14]  +  a[14] * b[15]
        M[15] = a[ 3] * b[12]  +  a[ 7] * b[13]  +  a[11] * b[14]  +  a[15] * b[15]
        return M

    def multVector3D(self, other):
        """
        Calculates the product of the Matrix Vector Multiplication:  Product = Self * Vector

        @param   other An instance of Vector3D
        @returns       The Vector3D product of the Matrix Vector multiplication.
        """
        # Convenience Variables:
        m = self
        v = other
        # Vectors (i.e direction & length) are Homogeneous Coordinate of the form (x,y,z,0) so we can simplify the mutiplication
        return Vector3D(
            m[ 0]*v.x + m[ 4]*v.y + m[ 8]*v.z,
            m[ 1]*v.x + m[ 5]*v.y + m[ 9]*v.z,
            m[ 2]*v.x + m[ 6]*v.y + m[10]*v.z
            )

    def multPoint3D(self, other):
        """
        Calculates the product of the Matrix Point Multiplication:  Product = Self * Point

        @param   other An instance of Point3D
        @returns       The Point3D product of the Matrix Point multiplication.
        """
        # Convenience Variables:
        m = self
        p = other
        # Points are Homogeneous Coordinates of the form (x,y,z,1) so we can simplify the mutiplication
        return Point3D(
            m[ 0]*p.x + m[ 4]*p.y + m[ 8]*p.z + m[12],
            m[ 1]*p.x + m[ 5]*p.y + m[ 9]*p.z + m[13],
            m[ 2]*p.x + m[ 6]*p.y + m[10]*p.z + m[14]
            )
