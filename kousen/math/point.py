# -*- coding: utf-8 -*-
import math
import PySide.QtCore

class Point3D(PySide.QtCore.QObject):
    """
    Point3D provides a simplified but self contained 3D Point class.
    """
    dataChanging = PySide.QtCore.Signal(object)
    dataChanged  = PySide.QtCore.Signal(object)

    def __init__(self,x=0,y=0,z=0):
        """
        Constructor.

        @param x The x component value.
        @param y The y component value.
        @param z The z component value.
        """
        super(Point3D, self).__init__()
        self._data = [x,y,z]

    def __len__(self):
        """
        The len operator.

        @returns The number of items in the internal data.
        """
        return len(self._data)

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

    def __repr__(self):
        """
        Generates the "official" string representation of the Point3D

        @returns A string representation of the Point3D
        """
        return "{0}({p.x}, {p.y}, {p.z})".format(self.__class__.__name__, p=self)

    def __str__(self):
        """
        Generates the "informal" string representation of the Point3D.

        @returns A string representation of the Point3D
        """
        return "P({p.x}, {p.y}, {p.z})".format(p=self)

    def __add__(self, other):
        """
        Calculates the sum of the addition operation.

        @param   other An object implementing x, y, z compoments
        @returns       The Point sum.
        """
        return self.__class__( self.x+other.x, self.y+other.y, self.z+other.z )

    def __sub__(self,other):
        """
        Calculates the difference of the substraction operation.

        @param   other An object implementing x, y, z compoments
        @returns       The Point difference if the other is a Vector3D; the Vector3D difference if the other is Point
        """
        from kousen.math.vector import Vector3D
        if isinstance(other, Vector3D):
            return self.__class__( self.x-other.x, self.y-other.y, self.z-other.z )
        return Vector3D( self.x-other.x, self.y-other.y, self.z-other.z )

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
        return not self == other

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

    @property
    def x(self):
        """
        Convenience property for the 'x' value

        @returns The value stored for the 'x' component
        """
        return self[0]

    @x.setter
    def x(self, value):
        """
        Convenience property for the 'x' value

        @param The value to store in the 'x' component
        """
        self[0] = value

    @property
    def y(self):
        """
        Convenience property for the 'y' value

        @returns The value stored for the 'y' component
        """
        return self[1]

    @y.setter
    def y(self, value):
        """
        Convenience property for the 'y' value

        @param The value to store in the 'y' component
        """
        self[1] = value

    @property
    def z(self):
        """
        Convenience property for the 'z' value

        @returns The value stored for the 'z' component
        """
        return self[2]

    @z.setter
    def z(self, value):
        """
        Convenience property for the 'z' value

        @param The value to store in the 'z' component
        """
        self[2] = value

    def data(self):
        """
        Accessor method to access the raw data

        @returns The list of values
        """
        return self._data

    def duplicate(self):
        """
        Copy Constructor.

        @returns Another Point with the same values as self
        """
        return self.__class__( self.x, self.y, self.z )

    def toVector3D(self):
        """
        Vector3D converter

        @returns A Vector3D with the same values as self
        """
        from kousen.math.vector import Vector3D
        return Vector3D( self.x, self.y, self.z )

    def distance(self, other):
        """
        Calculates the distance between self and another point

        @param   other An object implementing x, y, z compoments
        @returns The length of the vector calcaulted between self and another point
        """
        return (other-self).length()

    def midpoint(self, other):
        """
        Calculates the mid point between self and another point

        @returns A Point between self and aother point.
        """
        return self.__class__( (self.x+other.x)*0.5, (self.y+other.y)*0.5, (self.z+other.z)*0.5 )

