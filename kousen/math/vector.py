# -*- coding: utf-8 -*-
import math

class Vector3D(object):
    """
    Vector3D provides a simplified but self contained 3D Vector class.
    """
    def __init__(self, x=0, y=0, z=0):
        """
        Constructor.

        @param x The x component value.
        @param y The y component value.
        @param z The z component value.
        """
        self._data = [x,y,z]

    @property
    def x(self):
        """
        Convenience property for the 'x' value

        @returns The value stored for the 'x' component
        """
        return self._data[0]

    @property
    def y(self):
        """
        Convenience property for the 'y' value

        @returns The value stored for the 'y' component
        """
        return self._data[1]

    @property
    def z(self):
        """
        Convenience property for the 'z' value

        @returns The value stored for the 'z' component
        """
        return self._data[2]

    @property
    def data(self):
        """
        Convenience property to access the raw data

        @returns The list of values
        """
        return self._data

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        """
        The [] operator getter.

        @param index The lookup index to the internal data.
        @returns      The data if the lookup operation was succesful; None otherwise.
        """
        return self._data[index] if index < len(self._data) else None

    def __repr__(self):
        """
        Generates the "official" string representation of the Vector3D

        @returns A string representation of the Vector3D
        """
        return "{0}({v.x}, {v.y}, {v.z})".format(self.__class__.__name__, v=self)

    def __str__(self):
        """
        Generates the "informal" string representation of the Vector3D.

        @returns A string representation of the Vector3D
        """
        return "V({v.x}, {v.y}, {v.z})".format(v=self)

    def __neg__(self):
        """
        Calculates the negated vector.

        @returns The duplicate vector with negated values.
        """
        return self.__class__( -self.x, -self.y, -self.z )

    def __add__(self,other):
        """
        Calculates the sum of the addition operation.

        @param   other An object implementing x, y, z compoments
        @returns       The Point sum if the other is a Point3D; the Vector3D sum if the other is a Vector3D
        """
        from kousen.math.point import Point3D
        if isinstance(other,Point3D):
            return other.__class__( self.x+other.x, self.y+other.y, self.z+other.z )
        return self.__class__( self.x+other.x, self.y+other.y, self.z+other.z )

    def __sub__(self,other):
        """
        Calculates the difference of the substraction operation.

        @param   other An object implementing x, y, z compoments
        @returns       The Vector3D difference
        """
        return self.__class__( self.x-other.x, self.y-other.y, self.z-other.z )

    def __mul__(self, other):
        """
        Calculates the product of the scalar multiplication operation or (out of coveneince) the dot product of the Vector3D dot product operations.

        @param   other An object implementing x, y, z compoments or a single scalar value
        @returns       The Vector3D product or Vector3D dot product
        """
        # dot product
        if isinstance(other, Vector3D):
           return self.dotproduct(other)

        # scalar product
        return self.__class__( self.x*other, self.y*other, self.z*other )

    def __rmul__(self,other):
        """
        Calculates the product of the 'reflected' scalar multiplication operation or the dot product of the Vector3D multiplication operations.

        @param   other An object implementing x, y, z compoments or a single scalar value
        @returns       The Vector3D product
        """
        return self*other

    def __div__(self,other):
        """
        Calculates the product of the scalar division operation.

        @param   other A single scalar value
        @returns       The Vector3D product
        """
        return self.__class__( self.x/other, self.y/other, self.z/other )

    def __xor__(self, other):
        """
        Calculates the cross product of the Vector3D cross product operation.

        @param   other An object implementing x, y, z compoments.
        @returns       The Vector3D cross product.
        @warning       This overrides the '^' notation.
        """
        return self.crossproduct(other)

    def __eq__(self,other):
        """
        Calculates the result of the rich comparison equality operation.

        @param   other An object implementing x, y, z compoments
        @returns       True if the components are equal; false otherwise
        """
        return self.x==other.x and self.y==other.y and self.z==other.z

    def __ne__(self,other):
        """
        Calculates the result of the rich comparison not equality opeeration.

        @param   other An object implementing x, y, z compoments
        @returns       True if the components not are equal; false otherwise
        """
        return not (self==other)

    def dotproduct(self, other):
        """
        Calculates the dot product of the Vector3D dot product operation.

        @param   other An object implementing x, y, z compoments
        @returns       The dot product product
        """
        return self.x*other.x + self.y*other.y + self.z*other.z

    def angle(self, other):
        """
        Calculates the angle between two vectors using the Vector3D dot product operation.

        @param   other An object implementing x, y, z compoments
        @returns       The angle in radians
        """
        return math.acos( (self * other) / (self.length() * other.length()) )

    def crossproduct(self, other, normalized=False):
        """
        Calculates the cross product of the Vector3D cross product operation.

        @param   other      An object implementing x, y, z compoments
        @param   normalized Flag to normalize the resulting cross product
        @returns            The cross product Vector3D
        """
        product = self.__class__(
            self.y*other.z - self.z*other.y,
            self.z*other.x - self.x*other.z,
            self.x*other.y - self.y*other.x )

        if normalized:
            product.normalize()

        return product

    def duplicate(self):
        """
        Copy Constructor.

        @returns A duplicate Vector3D with the same values.
        """
        return self.__class__( self.x, self.y, self.z )

    def toPoint3D(self):
        """
        Point3D Converter.

        @returns A duplicate Point3D with the same values.
        """
        from kousen.math.point import Point3D
        return Point3D( self.x, self.y, self.z )

    def lengthSquared(self):
        """
        Calculates the squared length.

        @returns The Vector3D length, squared.
        """
        return self.x*self.x+self.y*self.y+self.z*self.z

    def length(self):
        """
        Calculates the length.

        @returns The Vector3D length.
        """
        return math.sqrt( self.lengthSquared() )

    def lengthInversed(self):
        """
        Calculates the inverse length.

        @returns The Vector3D 1 / length if valid; 0 otherwise.
        """
        l = self.length()
        return 1/l if l > 0 else 0

    def normalize(self):
        """
        Performs an in-place normalization.
        """
        l = self.lengthInversed()

        if ( l > 0 ):
            self._data[:] = [i*l for i in self._data]

    def normalized(self):
        """
        Calculates the vector of the normalization process.

        @returns A duplicate Vector3D with a normalized length.
        """
        l = self.length()
        if ( l > 0 ):
            return self.__class__( self.x/l, self.y/l, self.z/l )
        return self.duplicate()

XAxis = Vector3D(1,0,0)
YAxis = Vector3D(0,1,0)
ZAxis = Vector3D(0,0,1)
