# -*- coding: utf-8 -*-
from kousen.math import Vector3D, Point3D, Matrix4x4
from kousen.scenegraph import SceneGraphItem

class TranslationNode(SceneGraphItem):
    """
    TranslationNode provides a Translation implementation of a SceneGraphItem.
    """
    # Additional Meta Information
    __category__ = "Transformation Node"
    __icon__     = ":/icons/transform-translation.png"

    def __init__(self, translation=Vector3D(0,0,0), sdata={}, parent=None):
        """
        Constructor.

        @param translation The initial translation vector.
        @param sdata       The initial instance of AbstractData or iterable object containing static data to be converted to an instance of AbstractData.
        @param parent      The initial parent SceneGraphItem of this SceneGraphItem
        """
        super(SceneGraphItem, self).__init__(sdata, parent)
        self._translation = translation
        self._matrix = Matrix4x4.translation(self._translation)

    @property
    def translation(self):
        """
        Convenience property to access the Translation Node translation vector.

        @returns An instance of a Vector3D if valid; None otherwise.
        """ 
        return self._translation

    @translation.setter
    def translation(self, value):
        """
        Convenience property to access the Translation Node translation vector.

        @param value An instance of a Vector3D.
        """ 
        self._translation = value
        self._matrix = Matrix4x4.translation(self._translation)

class RotationNode(SceneGraphItem):
    """
    RotationNode provides a Rotation implementation of a SceneGraphItem.
    """
    # Additional Meta Information
    __category__ = "Transformation Node"
    __icon__     = ":/icons/transform-rotation.png"

    def __init__(self, angle=0, axis=Vector3D(0,0,0), point=Point3D(0,0,0), sdata={}, parent=None):
        """
        Constructor.

        @param angle   The initial rotation angle (radians).
        @param axis    The initial rotation axis.
        @param point   The initial rotation origin point.
        @param sdata   The initial instance of AbstractData or iterable object containing static data to be converted to an instance of AbstractData.
        @param parent  The initial parent SceneGraphItem of this SceneGraphItem
        """
        super(SceneGraphItem, self).__init__(sdata, parent)
        self._angle = angle
        self._axis  = axis
        self._point = point
        self._matrix = Matrix4x4.rotation(self._angle, self._axis, self._point)

    @property
    def axis(self):
        """
        Convenience property to access the Rotation Node axis vector.

        @returns An instance of a Vector3D if valid; None otherwise.
        """ 
        return self._axis

    @axis.setter
    def axis(self, value):
        """
        Convenience property to access the Rotation Node axis vector.

        @param value An instance of a Vector3D.
        """ 
        self._axis = value
        self._matrix = Matrix4x4.rotation(self._angle, self._axis, self._point)

    @property
    def angle(self):
        """
        Convenience property to access the Rotation Node rotation angle (radians).

        @returns An rotation angle in radians.
        """ 
        return self._angle

    @angle.setter
    def angle(self, value):
        """
        Convenience property to access the Rotation Node rotation angle (radians).

        @param value An rotation angle in radians.
        """ 
        self._angle = value
        self._matrix = Matrix4x4.rotation(self._angle, self._axis, self._point)

    @property
    def point(self):
        """
        Convenience property to access the Rotation Node rotation point.

        @returns An instance of a Point3D if valid; None otherwise.
        """ 
        return self._point

    @point.setter
    def point(self, value):
        """
        Convenience property to access the Rotation Node rotation point.

        @param value An instance of a Point3D.
        """ 
        self._point = value
        self._matrix = Matrix4x4.rotation(self._angle, self._axis, self._point)

class ScaleNode(SceneGraphItem):
    """
    ScaleNode provides a Scale implementation of a SceneGraphItem.
    """
    # Additional Meta Information
    __category__ = "Transformation Node"
    __icon__     = ":/icons/transform-scale.png"

    def __init__(self, factor=1, point=Point3D(0,0,0), sdata={}, parent=None):
        """
        Constructor.

        @param factor  The initial scale factor.
        @param point   The initial scale origin point.
        @param sdata   The initial instance of AbstractData or iterable object containing static data to be converted to an instance of AbstractData.
        @param parent  The initial parent SceneGraphItem of this SceneGraphItem
        """
        super(SceneGraphItem, self).__init__(sdata, parent)
        self._factor = factor
        self._point  = point
        self._matrix = Matrix4x4.scale(self._factor, self._point)

    @property
    def factor(self):
        """
        Convenience property to access the Scale Node scale factor.

        @returns The scale factor.
        """ 
        return self._factor

    @factor.setter
    def factor(self, value):
        """
        Convenience property to access the Scale Node scale factor.

        @param value The scale factor.
        """ 
        self._factor = value
        self._matrix = Matrix4x4.scale(self._factor, self._point)

    @property
    def point(self):
        """
        Convenience property to access the Scale Node scale point.

        @returns An instance of a Point3D if valid; None otherwise.
        """ 
        return self._point

    @point.setter
    def point(self, value):
        """
        Convenience property to access the Scale Node scale point.

        @param value An instance of a Point3D.
        """ 
        self._point = value
        self._matrix = Matrix4x4.scale(self._angle, self._axis, self._point)
