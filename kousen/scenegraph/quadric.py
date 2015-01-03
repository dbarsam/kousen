# -*- coding: utf-8 -*-
"""
This module provides quadric specializations of primitive nodes.

A Quadric surface is a tessellated polygon defined by a quadratic polynomial.  See http://en.wikipedia.org/wiki/Quadric for more information.
"""
from PySide import QtCore, QtGui
from kousen.scenegraph.primitive import (
    SphereNode,
    CylinderNode,
    ConeNode,
    ArrowNode,
    GnomonNode
)
from kousen.math import (
    Point3D, 
    Vector3D
)

class QuadricSphereNode(SphereNode):
    """
    QuadricSphereNode extends the SphereNode as a Quadric Surface specialization.
    """
    # Additional Meta Information
    __description__  = "Quadric Sphere Primitve"
    __instantiable__ = True

    def __init__(self, radius = 1.0, slices = 32, stacks = 32, parent=None):
        """
        Constructor.

        @param radius   The radius of the sphere.
        @param slices   The number of subdivisions around the z-axis (similar to lines of longitude).
        @param stacks   The number of subdivisions along the z-axis (similar to lines of latitude).
        @param parent   The parent SceneGraphNode instance.
        """
        super(QuadricSphereNode, self).__init__(radius, parent)
        self.__stacks = stacks
        self.__slices = slices

    @property
    def slices(self):
        """
        Convenience property for the 'slices' value

        @returns The value stored for the 'slices' component
        """
        return self.__slices

    @slices.setter
    def slices(self, value):
        """
        Convenience property for the 'slices' value

        @param The value to store in the 'slices' component
        """
        self.__slices = value

    @property
    def stacks(self):
        """
        Convenience property for the 'stacks' value

        @returns The value stored for the 'stacks' component
        """
        return self.__stacks

    @stacks.setter
    def stacks(self, value):
        """
        Convenience property for the 'stacks' value

        @param The value to store in the 'stacks' component
        """
        self.__stacks = value


class QuadricCylinderNode(CylinderNode):
    """
    QuadricCylinderNode extends the CylinderNode as a Quadric Surface specialization.
    """
    # Additional Meta Information
    __description__  = "Quadric Cylinder Primitve"
    __instantiable__ = True

    def __init__(self, radius = 1.0, length = 1, axis=Vector3D(0,1,0), slices = 32, stacks = 1, loops = 1, parent=None):
        """
        Constructor.

        @param radius   The radius of the cylinder base.
        @param length   The length of the cylinder.
        @param axis     The axis of the cylinder.
        @param slices   The number of subdivisions around the z-axis (similar to lines of longitude).
        @param stacks   The number of subdivisions along the z-axis (similar to lines of latitude).
        @param loops    The number of concentric rings about the origin into which the cylinder's base is subdivided.
        @param parent   The parent SceneGraphNode instance.
        """
        super(QuadricCylinderNode, self).__init__(radius, length, axis, parent)
        self.__stacks = stacks
        self.__slices = slices
        self.__loops = loops

    @property
    def slices(self):
        """
        Convenience property for the 'slices' value

        @returns The value stored for the 'slices' component
        """
        return self.__slices

    @slices.setter
    def slices(self, value):
        """
        Convenience property for the 'slices' value

        @param The value to store in the 'slices' component
        """
        self.__slices = value

    @property
    def stacks(self):
        """
        Convenience property for the 'stacks' value

        @returns The value stored for the 'stacks' component
        """
        return self.__stacks

    @stacks.setter
    def stacks(self, value):
        """
        Convenience property for the 'stacks' value

        @param The value to store in the 'stacks' component
        """
        self.__stacks = value

    @property
    def loops(self):
        """
        Convenience property for the 'loops' value

        @returns The value stored for the 'loops' component
        """
        return self.__loops

    @loops.setter
    def loops(self, value):
        """
        Convenience property for the 'loops' value

        @param The value to store in the 'loops' component
        """
        self.__loops = value


class QuadricConeNode(ConeNode):
    """
    QuadricConeNode extends the ConeNode as a Quadric Surface specialization.
    """
    # Additional Meta Information
    __description__  = "Quadric Cone Primitve"
    __instantiable__ = True

    def __init__(self, radius = 1.0, length = 1, axis=Vector3D(0,1,0), slices = 32, stacks = 32, loops = 1, parent=None):
        """
        Constructor.

        @param radius   The radius of the cylinder base.
        @param length   The length of the cylinder.
        @param axis     The axis of the cylinder.
        @param slices   The number of subdivisions around the z-axis (similar to lines of longitude).
        @param stacks   The number of subdivisions along the z-axis (similar to lines of latitude).
        @param loops    The number of concentric rings about the origin into which the cylinder's base is subdivided.
        @param parent   The parent SceneGraphNode instance.
        """
        super(QuadricConeNode, self).__init__(radius, length, axis, parent)
        self.__stacks = stacks
        self.__slices = slices
        self.__loops = loops

    @property
    def slices(self):
        """
        Convenience property for the 'slices' value

        @returns The value stored for the 'slices' component
        """
        return self.__slices

    @slices.setter
    def slices(self, value):
        """
        Convenience property for the 'slices' value

        @param The value to store in the 'slices' component
        """
        self.__slices = value

    @property
    def stacks(self):
        """
        Convenience property for the 'stacks' value

        @returns The value stored for the 'stacks' component
        """
        return self.__stacks

    @stacks.setter
    def stacks(self, value):
        """
        Convenience property for the 'stacks' value

        @param The value to store in the 'stacks' component
        """
        self.__stacks = value

    @property
    def loops(self):
        """
        Convenience property for the 'loops' value

        @returns The value stored for the 'loops' component
        """
        return self.__loops

    @loops.setter
    def loops(self, value):
        """
        Convenience property for the 'loops' value

        @param The value to store in the 'loops' component
        """
        self.__loops = value

class QuadricArrowNode(ArrowNode):
    """
    ArrowNode implements a primitive composite node.
    """
    # Additional Meta Information
    __description__  = "Quadric Arrow Primitve"
    __instantiable__ = True

    def __init__(self, head = Point3D(0,1,0), tail = Point3D(0,0,0), cyradius = 0.005, coradius = 0.075, mid=0.80, slices = 32, stacks = 32, loops = 1, parent=None):
        """
        Constructor.

        @param head     The point representing the tip of the arrow
        @param tail     The point representing the base of the arrow
        @param cyradius The radius of the cylinder used in the arrow shaft
        @param coradius The radius of the cone used in the arrow tip
        @param mid      The "mid point" or the percentage [0,1] along the length where the cylinder and cone join
        @param slices   The number of subdivisions around the z-axis (similar to lines of longitude).
        @param stacks   The number of subdivisions along the z-axis (similar to lines of latitude).
        @param loops    The number of concentric rings about the origin into which the cylinder's base is subdivided.
        @param parent   The parent SceneGraphNode instance.
        """
        self.__stacks = stacks
        self.__slices = slices
        self.__loops = loops
        super(QuadricArrowNode, self).__init__(head, tail, cyradius, coradius, mid, parent)

    def _generateGeometry(self):
        """
        Generates a geometry data from internal data.

        @returns A specialized object representing geometry data.
        """
        direction = self.head - self.tail
        length = direction.length()
        cylinder_length  = length * self.mid
        cone_length =  length * (1-self.mid)
        normalized_direction = direction.normalized()

        cy = QuadricCylinderNode(self.cylinder_radius, cylinder_length, normalized_direction, self.slices, self.stacks, self.loops, self)
        co = QuadricConeNode(self.cone_radius, cone_length, normalized_direction, self.slices, self.stacks, self.loops, self)
        co.translation.direction = direction * self.mid
        return (cy, co)

    @property
    def slices(self):
        """
        Convenience property for the 'slices' value

        @returns The value stored for the 'slices' component
        """
        return self.__slices

    @slices.setter
    def slices(self, value):
        """
        Convenience property for the 'slices' value

        @param The value to store in the 'slices' component
        """
        self.__slices = value

    @property
    def stacks(self):
        """
        Convenience property for the 'stacks' value

        @returns The value stored for the 'stacks' component
        """
        return self.__stacks

    @stacks.setter
    def stacks(self, value):
        """
        Convenience property for the 'stacks' value

        @param The value to store in the 'stacks' component
        """
        self.__stacks = value

    @property
    def loops(self):
        """
        Convenience property for the 'loops' value

        @returns The value stored for the 'loops' component
        """
        return self.__loops

    @loops.setter
    def loops(self, value):
        """
        Convenience property for the 'loops' value

        @param The value to store in the 'loops' component
        """
        self.__loops = value

class QuadricGnomonNode(GnomonNode):
    """
    QuadricGnomon implements a primitive composite node.
    """
    # Additional Meta Information
    __description__  = "Quadric Gnomon Primitve"
    __instantiable__ = True

    def __init__(self, length = 0.4, cyradius = 0.005, coradius = 0.05, mid=0.80, slices = 32, stacks = 32, loops = 1, parent=None):
        """
        Constructor.

        @param head     The point representing the tip of the arrow
        @param tail     The point representing the base of the arrow
        @param cyradius The radius of the cylinder used in the arrow shaft
        @param coradius The radius of the cone used in the arrow tip
        @param mid      The "mid point" or the percentage [0,1] along the length where the cylinder and cone join
        @param slices   The number of subdivisions around the z-axis (similar to lines of longitude).
        @param stacks   The number of subdivisions along the z-axis (similar to lines of latitude).
        @param loops    The number of concentric rings about the origin into which the cylinder's base is subdivided.
        @param parent   The parent SceneGraphNode instance.
        """
        self.__stacks = stacks
        self.__slices = slices
        self.__loops = loops
        super(QuadricGnomonNode, self).__init__(length, cyradius, coradius, mid, parent)

    def _generateGeometry(self):
        """
        Generates a geometry data from internal data.

        @returns A specialized object representing geometry data.
        """
        xaxis = QuadricArrowNode(self.xaxis, self.origin, self.cylinder_radius, self.cone_radius, self.mid, self.slices, self.stacks, self.loops, self)
        yaxis = QuadricArrowNode(self.yaxis, self.origin, self.cylinder_radius, self.cone_radius, self.mid, self.slices, self.stacks, self.loops, self)
        zaxis = QuadricArrowNode(self.zaxis, self.origin, self.cylinder_radius, self.cone_radius, self.mid, self.slices, self.stacks, self.loops, self)
        xaxis.setColor( QtGui.QColor(QtCore.Qt.GlobalColor.red) )
        yaxis.setColor( QtGui.QColor(QtCore.Qt.GlobalColor.green) )
        zaxis.setColor( QtGui.QColor(QtCore.Qt.GlobalColor.blue) )
        return ( xaxis, yaxis, zaxis )

    @property
    def slices(self):
        """
        Convenience property for the 'slices' value

        @returns The value stored for the 'slices' component
        """
        return self.__slices

    @slices.setter
    def slices(self, value):
        """
        Convenience property for the 'slices' value

        @param The value to store in the 'slices' component
        """
        self.__slices = value

    @property
    def stacks(self):
        """
        Convenience property for the 'stacks' value

        @returns The value stored for the 'stacks' component
        """
        return self.__stacks

    @stacks.setter
    def stacks(self, value):
        """
        Convenience property for the 'stacks' value

        @param The value to store in the 'stacks' component
        """
        self.__stacks = value

    @property
    def loops(self):
        """
        Convenience property for the 'loops' value

        @returns The value stored for the 'loops' component
        """
        return self.__loops

    @loops.setter
    def loops(self, value):
        """
        Convenience property for the 'loops' value

        @param The value to store in the 'loops' component
        """
        self.__loops = value