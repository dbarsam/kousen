# -*- coding: utf-8 -*-
"""
This module provides primitive specializations of object nodes.

A Primitive is a simple geometric shape defined in constructive solid geometry.  See http://en.wikipedia.org/wiki/Geometric_primitive for more information.
"""
from kousen.scenegraph.object import ObjectNode
from kousen.math import Point3D, Vector3D

class PrimitiveNode(ObjectNode):
    """
    PrimitiveNode provides a base class for all geometric object implementation of an ObjectNode.
    """
    # Additional Meta Information
    __category__     = "Primitive Node"
    __icon__         = ":/icons/node.png"
    __description__  = "<Unknown Primitive>"

    def __init__(self, name, parent):
        """
        Constructor.

        @param name    The display name of the node.
        @param parent  The initial AbstractDataTreeItem-derived parent.
        """
        super(PrimitiveNode, self).__init__(name, parent)

    def _updateGeometry(self):
        """
        Internal method to manually update the cached geometry data from internal data.
        """
        pass

    def __generateGeometry(self):
        """
        Generates a gemetry data from internal data.

        @returns A specialized object representing geometry data.
        """
        pass

class SphereNode(PrimitiveNode):
    """
    SphereNonde implements a Sphere PrimitiveNode.
    """
    # Additional Meta Information
    __description__  = "Sphere Primitve"
    __instantiable__ = True

    def __init__(self, radius = 1.0, parent=None):
        """
        Constructor.

        @param radius   The radius of the sphere.
        @param parent   The parent SceneGraphNode instance.
        """
        super(SphereNode, self).__init__(self.__description__, parent)
        self.__radius = radius

    @property
    def radius(self):
        """
        Convenience property for the 'radius' value

        @returns The value stored for the 'radius' component
        """
        return self.__radius

    @radius.setter
    def radius(self, value):
        """
        Convenience property for the 'radius' value

        @param The value to store in the 'radius' component
        """
        self.__radius = value


class CubeNode(PrimitiveNode):
    """
    CubeNode implements a Cube PrimitiveNode.
    """
    # Additional Meta Information
    __description__  = "Cube Primitve"
    __instantiable__ = True

    def __init__(self, size = 0.5, parent=None):
        """
        Constructor.

        @param size     The length of one dimension of the sphere.
        @param parent   The parent SceneGraphNode instance.
        """
        super(CubeNode, self).__init__(self.__description__, parent)
        self.__size = size

    @property
    def size(self):
        """
        Convenience property for the 'size' value

        @returns The value stored for the 'size' component
        """
        return self.__size

    @size.setter
    def size(self, value):
        """
        Convenience property for the 'size' value

        @param The value to store in the 'size' component
        """
        self.__size = value

class CylinderNode(PrimitiveNode):
    """
    CylinderNode implements a Cylinder PrimitiveNode.
    """
    # Additional Meta Information
    __description__  = "Cylinder Primitive"
    __instantiable__ = True

    def __init__(self, radius = 1.0, length = 1, axis=Vector3D(0,1,0), parent=None):
        """
        Constructor.

        @param radius   The radius of the cylinder base.
        @param length   The length of the cylinder.
        @param axis     The axis of the cylinder.
        @param parent   The parent SceneGraphNode instance.
        """
        super(CylinderNode, self).__init__(self.__description__, parent)
        self.__radius = radius
        self.__length = length
        self.__axis = axis

    @property
    def radius(self):
        """
        Convenience property for the 'radius' value

        @returns The value stored for the 'radius' component
        """
        return self.__radius

    @radius.setter
    def radius(self, value):
        """
        Convenience property for the 'radius' value

        @param The value to store in the 'radius' component
        """
        self.__radius = value

    @property
    def length(self):
        """
        Convenience property for the 'length' value

        @returns The value stored for the 'length' component
        """
        return self.__length

    @length.setter
    def length(self, value):
        """
        Convenience property for the 'length' value

        @param The value to store in the 'length' component
        """
        self.__length = value

    @property
    def axis(self):
        """
        Convenience property for the 'axis' value

        @returns The value stored for the 'axis' component
        """
        return self.__axis

    @axis.setter
    def axis(self, value):
        """
        Convenience property for the 'axis' value

        @param The value to store in the 'axis' component
        """
        self.__axis = value

class ConeNode(CylinderNode):
    """
    ConeNode implements a specialized CylinderNode.
    """
    # Additional Meta Information
    __description__  = "Cone Primitve"
    __instantiable__ = True

class ArrowNode(PrimitiveNode):
    """
    ArrowNode implements a primitive composite node.
    """
    # Additional Meta Information
    __description__  = "Arrow Primitve"
    __instantiable__ = True

    def __init__(self, head = Point3D(0,1,0), tail = Point3D(0,0,0), cyradius = 0.005, coradius = 0.075, mid=0.80, parent=None):
        """
        Constructor.

        @param head     The point representing the tip of the arrow
        @param tail     The point representing the base of the arrow
        @param cyradius The radius of the cylinder used in the arrow shaft
        @param coradius The radius of the cone used in the arrow tip
        @param mid      The "mid point" or the percentage [0,1] along the length where the cylinder and cone join
        @param parent   The parent SceneGraphNode instance.
        """
        super(ArrowNode, self).__init__(self.__description__, parent)

        self.__head = head
        self.__tail = tail
        self.__mid = mid
        self.__cyradius = cyradius
        self.__coradius = coradius
        
        self._updateGeometry()

    def _updateGeometry(self):
        """
        Internal method to manually update the cached geometry data from internal data.
        """
        for node in self._generateGeometry():
            self.appendChild( node )

    def _generateGeometry(self):
        """
        Generates a geometry data from internal data.

        @returns A specialized object representing geometry data.
        """
        direction = head - tail
        length = direction.length()
        cylinder_length = length * mid
        cone_length = length * (1-mid)
        normalized_direction = direction.normalized()
        
        cy = CylinderNode(self.cylinder_radius, cylinder_length, normalized_direction, self)
        co = ConeNode(self.cone_radius, cone_length, normalized_direction, self)
        co.translation.direction = direction * self.mid
        return (cy, co)

    @property
    def head(self):
        """
        Convenience property for the 'head' value

        @returns The value stored for the 'head' component
        """
        return self.__head

    @head.setter
    def head(self, value):
        """
        Convenience property for the 'head' value

        @param The value to store in the 'head' component
        """
        self.__head = value

    @property
    def tail(self):
        """
        Convenience property for the 'tail' value

        @returns The value stored for the 'tail' component
        """
        return self.__tail

    @tail.setter
    def tail(self, value):
        """
        Convenience property for the 'tail' value

        @param The value to store in the 'tail' component
        """
        self.__tail = value

    @property
    def mid(self):
        """
        Convenience property for the 'mid' value

        @returns The value stored for the 'mid' component
        """
        return self.__mid

    @mid.setter
    def mid(self, value):
        """
        Convenience property for the 'mid' value

        @param The value to store in the 'mid' component
        """
        self.__mid = value

    @property
    def cylinder_radius(self):
        """
        Convenience property for the 'cylinder radius' value

        @returns The value stored for the 'cylinder radius' component
        """
        return self.__cyradius

    @cylinder_radius.setter
    def cylinder_radius(self, value):
        """
        Convenience property for the 'cylinder radius' value

        @param The value to store in the 'cylinder radius' component
        """
        self.__cyradius = value

    @property
    def cone_radius(self):
        """
        Convenience property for the 'cone radius' value

        @returns The value stored for the 'cone radius' component
        """
        return self.__coradius

    @cone_radius.setter
    def cone_radius(self, value):
        """
        Convenience property for the 'cone radius' value

        @param The value to store in the 'cone radius' component
        """
        self.__coradius = value

class GnomonNode(PrimitiveNode):
    """
    GnomonNode implements a primitive composite node.
    """
    # Additional Meta Information
    __description__  = "Gnomon Primitve"
    __instantiable__ = True

    def __init__(self, length = 0.4, cyradius = 0.005, coradius = 0.075, mid=0.80, parent=None):
        """
        Constructor.

        @param cyradius The radius of the cylinder used in the arrow shaft
        @param coradius The radius of the cone used in the arrow tip
        @param mid      The "mid point" or the percentage [0,1] along the length where the cylinder and cone join
        @param parent   The parent SceneGraphNode instance.
        """
        super(GnomonNode, self).__init__(self.__description__, parent)

        self.__length = length
        self.__o = Vector3D();
        self.__x = Vector3D(length, 0, 0)
        self.__y = Vector3D(0, length, 0)
        self.__z = Vector3D(0, 0, length)
        self.__mid = mid
        self.__cyradius = cyradius
        self.__coradius = coradius
        self._updateGeometry()

    def _updateGeometry(self):
        """
        Internal method to manually update the cached geometry data from internal data.
        """
        for node in self._generateGeometry():
            self.appendChild( node )

    def _generateGeometry(self):
        """
        Generates a geometry data from internal data.

        @returns A specialized object representing geometry data.
        """
        return (
            ArrowNode(self.xaxis, self.origin, self.cylinder_radius, self.cone_radius, self.mid, self),
            ArrowNode(self.yaxis, self.origin, self.cylinder_radius, self.cone_radius, self.mid, self),
            ArrowNode(self.zaxis, self.origin, self.cylinder_radius, self.cone_radius, self.mid, self)
        )

    @property
    def length(self):
        """
        Convenience property for the 'length' value

        @returns The value stored for the 'length' component
        """
        return self.__length

    @length.setter
    def length(self, value):
        """
        Convenience property for the 'length' value

        @param The value to store in the 'length' component
        """
        self.__length = value

    @property
    def xaxis(self):
        """
        Convenience property for the 'xaxis' value

        @returns The value stored for the 'xaxis' component
        """
        return self.__x

    @xaxis.setter
    def xaxis(self, value):
        """
        Convenience property for the 'xaxis' value

        @param The value to store in the 'xaxis' component
        """
        self.__x = value

    @property
    def yaxis(self):
        """
        Convenience property for the 'yaxis' value

        @returns The value stored for the 'yaxis' component
        """
        return self.__y

    @yaxis.setter
    def yaxis(self, value):
        """
        Convenience property for the 'yaxis' value

        @param The value to store in the 'yaxis' component
        """
        self.__y = value

    @property
    def zaxis(self):
        """
        Convenience property for the 'zaxis' value

        @returns The value stored for the 'zaxis' component
        """
        return self.__z

    @zaxis.setter
    def zaxis(self, value):
        """
        Convenience property for the 'zaxis' value

        @param The value to store in the 'zaxis' component
        """
        self.__z = value

    @property
    def origin(self):
        """
        Convenience property for the 'origin' value

        @returns The value stored for the 'origin' component
        """
        return self.__o

    @origin.setter
    def origin(self, value):
        """
        Convenience property for the 'origin' value

        @param The value to store in the 'origin' component
        """
        self.__o = value

    @property
    def mid(self):
        """
        Convenience property for the 'mid' value

        @returns The value stored for the 'mid' component
        """
        return self.__mid

    @mid.setter
    def mid(self, value):
        """
        Convenience property for the 'mid' value

        @param The value to store in the 'mid' component
        """
        self.__mid = value

    @property
    def cylinder_radius(self):
        """
        Convenience property for the 'cylinder radius' value

        @returns The value stored for the 'cylinder radius' component
        """
        return self.__cyradius

    @cylinder_radius.setter
    def cylinder_radius(self, value):
        """
        Convenience property for the 'cylinder radius' value

        @param The value to store in the 'cylinder radius' component
        """
        self.__cyradius = value

    @property
    def cone_radius(self):
        """
        Convenience property for the 'cone radius' value

        @returns The value stored for the 'cone radius' component
        """
        return self.__coradius

    @cone_radius.setter
    def cone_radius(self, value):
        """
        Convenience property for the 'cone radius' value

        @param The value to store in the 'cone radius' component
        """
        self.__coradius = value

class PlaneNode(PrimitiveNode):
    """
    PlaneNode implements a Plane PrimitiveNode.
    """
    # Additional Meta Information
    __description__  = "Plane Primitve"
    __instantiable__ = True

    def __init__(self, length = 0.5, width = 0.5, normal = Vector3D(0,1,0), parent=None):
        """
        Constructor.

        @param length   The length of one dimension of the plane.
        @param width    The length of one dimension of the plane.
        @param normal   The surface normal of the plane.
        @param parent   The parent SceneGraphNode instance.
        """
        super(PlaneNode, self).__init__(self.__description__, parent)
        self.__length = length
        self.__width = width
        self.__normal = normal

    @property
    def length(self):
        """
        Convenience property for the 'length' value

        @returns The value stored for the 'length' component
        """
        return self.__length

    @length.setter
    def length(self, value):
        """
        Convenience property for the 'length' value

        @param The value to store in the 'length' component
        """
        self.__length = value

    @property
    def width(self):
        """
        Convenience property for the 'width' value

        @returns The value stored for the 'width' component
        """
        return self.__width

    @width.setter
    def width(self, value):
        """
        Convenience property for the 'width' value

        @param The value to store in the 'width' component
        """
        self.__width = value

    @property
    def normal(self):
        """
        Convenience property for the 'normal' value

        @returns The value stored for the 'normal' component
        """
        return self.__normal

    @normal.setter
    def normal(self, value):
        """
        Convenience property for the 'normal' value

        @param The value to store in the 'normal' component
        """
        self.__normal = value

class GridNode(PlaneNode):
    """
    GridNode implements a specialized PlaneNode.
    """
    # Additional Meta Information
    __description__  = "Grid Primitve"
    __instantiable__ = True

    def __init__(self, spacing=0.5, count = 14, normal=Vector3D(0,1,0), parent=None):
        """
        Constructor.

        @param count    The number of lines in the grid.
        @param space    The spaceing between lines.
        @param length   The length of one dimension of the plane.
        @param width    The length of one dimension of the plane.
        @param normal   The surface normal of the plane.
        @param parent   The parent SceneGraphNode instance.
        """
        super(GridNode, self).__init__(spacing * count, spacing * count, normal, parent)
        self.__spacing = spacing
        self.__count = count

    @property
    def spacing(self):
        """
        Convenience property for the 'spacing' value

        @returns The value stored for the 'spacing' component
        """
        return self.__spacing

    @spacing.setter
    def spacing(self, value):
        """
        Convenience property for the 'spacing' value

        @param The value to store in the 'spacing' component
        """
        self.__spacing = value

    @property
    def count(self):
        """
        Convenience property for the 'count' value

        @returns The value stored for the 'count' component
        """
        return self.__count

    @count.setter
    def count(self, value):
        """
        Convenience property for the 'count' value

        @param The value to store in the 'count' component
        """
        self.__count = value
