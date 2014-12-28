# -*- coding: utf-8 -*-
import math
from PySide import QtCore
from kousen.math import Vector3D, Point3D, Matrix4x4
from kousen.scenegraph import SceneGraphNode

class TransformationComponent(QtCore.QObject):
    """
    TransformationComponent provides a base interface of a Transformation component (Translation, Rotation, Scale, etc)
    """
    dataChanging = QtCore.Signal()
    dataChanged  = QtCore.Signal()

    def __init__(self, matrix=Matrix4x4.identity()):
        """
        Constructor.

        @param m The initial transformation matrix value.
        """
        super(TransformationComponent, self).__init__()
        self.__matrix = matrix

    def _dataChanging(self):
        """
        Internal method to emit the dataChanging signal.
        """
        if self.signalsBlocked():
            return

        self.dataChanging.emit()

    def _dataChanged(self):
        """
        Internal method to emit the dataChanged signal.
        """
        if self.signalsBlocked():
            return

        self._updateMatrix()
        self.dataChanged.emit()

    def _connect(self, dataObject):
        """
        Internal method to connect to dataObject.

        @param dataObject An instance of a DataObject.
        """
        dataObject.dataChanging.connect(self._dataChanging)
        dataObject.dataChanged.connect(self._dataChanged)

    def _disconnect(self, dataObject):
        """
        Internal method to disconnect from a dataObject.

        @param dataObject An instance of a DataObject.
        """
        dataObject.dataChanging.disconnect(self._dataChanging)
        dataObject.dataChanged.disconnect(self._dataChanged)

    def _updateMatrix(self):
        """
        Internal method to manually update the cached transformation matrix from internal data.
        """
        self.__matrix = self._generateMatrix()

    def _generateMatrix(self):
        """
        Generates a transformation matrix from internal data.

        @returns A Matrix4x4 representation of the transformation component.
        """
        return Matrix4x4.identity()

    def matrix(self):
        """
        Returns the component pre-calcaulted transformation matrix.
        
        @returns A Matrix4x4 representation of the transformation component.
        """
        return self.__matrix

class TranslationComponent(TransformationComponent):
    """
    TranslationComponent provides a Translation implementation of a TransformationComponent.
    """
    def __init__(self, direction=None):
        """
        Constructor.

        @param direction The Translation direction vector.
        """
        super(TranslationComponent, self).__init__()        
        self.__direction = None
        self.blockSignals(True)
        self.direction = direction or Vector3D(0,0,0)
        self.blockSignals(False)
        self._updateMatrix()

    def _generateMatrix(self):
        """
        Generates a transformation matrix from internal data.

        @returns A Matrix4x4 representation of the transformation component.
        """
        return Matrix4x4.translation(self.__direction)

    @property
    def direction(self):
        """
        Convenience property to access the Translation Component direction vector.

        @returns An instance of a Vector3D if valid; None otherwise.
        """
        return self.__direction

    @direction.setter
    def direction(self, value):
        """
        Convenience property to access the Translation Component direction vector.

        @param value An instance of a Vector3D.
        """
        if not isinstance(value, Vector3D):
            raise TypeError("direction must be a Vector3D")

        self._dataChanging()
        if self.__direction:
            self._disconnect(self.__direction)
        self.__direction = value
        self._connect(self.__direction)
        self._dataChanged()

class RotationComponent(TransformationComponent):
    """
    RotationComponent provides a Rotation implementation of a TransformationComponent.
    """
    def __init__(self, angle=0, axis=None, point=None):
        """
        Constructor.

        @param angle   The initial rotation angle (degrees).
        @param axis    The initial rotation axis.
        @param point   The initial rotation origin point.
        """
        super(RotationComponent, self).__init__()        
        self.__angle = None        
        self.__axis = None        
        self.__point = None
        self.blockSignals(True)
        self.angle = angle
        self.axis = axis or Vector3D(0,0,0)
        self.point = point or Point3D(0,0,0)
        self.blockSignals(False)
        self._updateMatrix()

    def _generateMatrix(self):
        """
        Generates a transformation matrix from internal data.

        @returns A Matrix4x4 representation of the transformation component.
        """
        radians = math.radians(self.angle)
        return Matrix4x4.rotation(radians, self.__axis, self.__point)

    @property
    def axis(self):
        """
        Convenience property to access the Rotation Component axis vector.

        @returns An instance of a Vector3D if valid; None otherwise.
        """
        return self.__axis

    @axis.setter
    def axis(self, value):
        """
        Convenience property to access the Rotation Component axis vector.

        @param value An instance of a Vector3D.
        """
        if not isinstance(value, Vector3D):
            raise TypeError("point must be a Vector3D")

        self._dataChanging()
        if self.__axis:
            self._diconnect(self.__axis)
        self.__axis = value
        self._connect(self.__axis)
        self._dataChanged()

    @property
    def angle(self):
        """
        Convenience property to access the Rotation Component rotation angle (radians).

        @returns An rotation angle in degrees.
        """
        return self.__angle

    @angle.setter
    def angle(self, value):
        """
        Convenience property to access the Rotation Component rotation angle (radians).

        @param value An rotation angle in radians.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("angle must be a number")

        self._dataChanging()
        self.__angle = value
        self._dataChanged()

    @property
    def point(self):
        """
        Convenience property to access the Rotation Component rotation point.

        @returns An instance of a Point3D if valid; None otherwise.
        """
        return self.__point

    @point.setter
    def point(self, value):
        """
        Convenience property to access the Rotation Component rotation point.

        @param value An instance of a Point3D.
        """
        if not isinstance(value, Point3D):
            raise TypeError("point must be a Point3D")

        self._dataChanging()
        if self.__point:
            self._disconnect(self.__point)
        self.__point = value
        self._connect(self.__point)
        self._dataChanged()


class ScaleComponent(TransformationComponent):
    """
    ScaleComponent provides a Scale implementation of a TransformationComponent.
    """

    def __init__(self, factor=1, point=None):
        """
        Constructor.

        @param factor  The initial scale factor.
        @param point   The initial scale origin point.
        """
        super(ScaleComponent, self).__init__()        
        self.__factor = None
        self.__point = None
        self.blockSignals(True)
        self.factor = factor
        self.point  = point or Point3D(0,0,0)
        self.blockSignals(False)
        self._updateMatrix()

    def _generateMatrix(self):
        """
        Generates a transformation matrix from internal data.

        @returns A Matrix4x4 representation of the transformation component.
        """
        return Matrix4x4.scale(self.__factor, self.__point)

    @property
    def factor(self):
        """
        Convenience property to access the Scale Component scale factor.

        @returns The scale factor.
        """
        return self.__factor

    @factor.setter
    def factor(self, value):
        """
        Convenience property to access the Scale Component scale factor.

        @param value The scale factor.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("angle must be a number")

        self._dataChanging()
        self.__factor = value
        self._dataChanged()

    @property
    def point(self):
        """
        Convenience property to access the Scale Component scale point.

        @returns An instance of a Point3D if valid; None otherwise.
        """
        return self.__point

    @point.setter
    def point(self, value):
        """
        Convenience property to access the Scale Component scale point.

        @param value An instance of a Point3D.
        """
        if not isinstance(value, Point3D):
            raise TypeError("point must be a Point3D")

        self._dataChanging()
        if self.__point:
            self._disconnect(self.__point)
        self.__point = value
        self._connect(self.__point)
        self._dataChanged()

class AffineTransformation(TransformationComponent):
    """
    AffineTransformation provides an Affine Transforamtion (composite of Translation, Roation, Scale) implementation of a TransformationComponent.
    """

    def __init__(self, translation=None, rotation=None, scale=None):
        """
        Constructor.

        @param translation  The initial translation transformation component.
        @param rotation  The initial rotation transformation component.
        @param scale  The initial scale transformation component.
        """
        super(AffineTransformation, self).__init__()        
        self.__translation = None
        self.__rotation = None
        self.__scale = None
        self.blockSignals(True)
        self.translation = translation or TranslationComponent()
        self.rotation = rotation or RotationComponent()        
        self.scale = scale or ScaleComponent()
        self.blockSignals(False)
        self._updateMatrix()

    def _generateMatrix(self):
        """
        Generates a transformation matrix from internal data.

        @returns A Matrix4x4 representation of the transformation component.
        """
        t = self.__translation.matrix() if self.__translation else Matrix4x4.identity()
        r = self.__rotation.matrix() if self.__rotation else Matrix4x4.identity()
        s = self.__scale.matrix() if self.__scale else Matrix4x4.identity()
        return t * r * s

    @property
    def translation(self):
        """
        Convenience property to access the Translation Component of the Transformation Node.

        @returns An instance of a Vector3D if valid; None otherwise.
        """
        return self.__translation

    @translation.setter
    def translation(self, value):
        """
        Convenience property to access the Translation Component of the Transformation Node.

        @param value An instance of a Translation Component.
        """
        if not isinstance(value, TranslationComponent):
            raise TypeError("point must be a TranslationComponent")

        self._dataChanging()
        if self.__translation:
            self._disconnect(self.__translation)
        self.__translation = value
        self._connect(self.__translation)
        self._dataChanged()

    @property
    def rotation(self):
        """
        Convenience property to access the Rotation Component of the Transformation Node.

        @returns An instance of a Rotation Component if valid; None otherwise.
        """
        return self.__rotation

    @rotation.setter
    def rotation(self, value):
        """
        Convenience property to access the Rotation Component of the Transformation Node.

        @param value An instance of a Rotation Component.
        """
        if not isinstance(value, RotationComponent):
            raise TypeError("point must be a RotationComponent")

        self._dataChanging()
        if self.__rotation:
            self._disconnect(self.__rotation)
        self.__rotation = value
        self._connect(self.__rotation)
        self._dataChanged()

    @property
    def scale(self):
        """
        Convenience property to access the Scale Cmponent of the Transformation Node.

        @returns An instance of a ScaleComponent if valid; None otherwise.
        """
        return self.__scale

    @scale.setter
    def scale(self, value):
        """
        Convenience property to access the Scale Component of the Transformation Node.

        @param value An instance of a Scale Component.
        """
        if not isinstance(value, ScaleComponent):
            raise TypeError("point must be a ScaleComponent")

        self._dataChanging()
        if self.__scale:
            self._disconnect(self.__scale)
        self.__scale = value
        self._connect(self.__scale)
        self._dataChanged()

class TransformationNode(SceneGraphNode):
    """
    TransformationNode provides a Transformation implementation of a SceneGraphNode.
    """
    # Additional Meta Information
    __category__ = "Transformation Node"
    __icon__     = ":/icons/transform-translation.png"

    def __init__(self, name, parent=None):
        """
        Constructor.

        @param name    The display name of the node.
        @param parent  The initial AbstractDataTreeItem-derived parent.
        """
        super(TransformationNode, self).__init__(name, parent)
        self.__transformation = AffineTransformation()
        self.__transformation.dataChanging.connect(lambda: self._dataChanging(self.Fields.NAME, QtCore.Qt.DisplayRole))
        self.__transformation.dataChanged.connect(lambda: self._dataChanged(self.Fields.NAME, QtCore.Qt.DisplayRole))

    @property
    def translation(self):
        """
        Convenience property to access the Translation Component of the Transformation Node.

        @returns An instance of a Vector3D if valid; None otherwise.
        """
        return self.__transformation.translation

    @property
    def rotation(self):
        """
        Convenience property to access the Rotation Component of the Transformation Node.

        @returns An instance of a Rotation Component if valid; None otherwise.
        """
        return self.__transformation.rotation

    @property
    def scale(self):
        """
        Convenience property to access the Scale Cmponent of the Transformation Node.

        @returns An instance of a ScaleComponent if valid; None otherwise.
        """
        return self.__transformation.scale

    def matrix(self):
        """
        Returns the component pre-calcaulted transformation matrix.
        
        @returns A Matrix4x4 representation of the transformation component.
        """
        return self.__transformation.matrix()