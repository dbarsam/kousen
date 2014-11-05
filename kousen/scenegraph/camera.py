# -*- coding: utf-8 -*-
import math
from PySide import QtGui, QtCore
from OpenGL import GL
from kousen.scenegraph import SceneGraphItem
from kousen.gl.glscene import GLNode
from kousen.math import Point3D, Vector3D, Matrix4x4
from kousen.math.conic import coniclength, conicwidth

class CameraNode(SceneGraphItem):
    """
    The Camera Node provides Camera implementation of a SceneGraphItem.
    """
    # Additional Meta Information
    __category__     = "Camera Node"
    __icon__         = ":/icons/camera.png"

    # Camera default values 
    __camera_target__   = Point3D(0, 0, 0)
    __camera_position__ = Point3D(21, 28, 21)
    __camera_upvector__ = Vector3D(0, 1, 0)
    __camera_fov__      = 30.0    # (degrees)
    __camera_znear__    = 1.0
    __camera_zfar__     = 1000
    __camera_swidth__   = 1.0
    __camera_sheight__  = 1.0

    # The rotation speed; The amount of rotation (in degrees) that will occur
    # from dragging the mouse across the entire width of the screen.
    __camera_max_screen_rotation__ = 180.0

    def __init__(self, position=None, target=None, up=None, fov=None, znear=None, zfar=None, swidth=None, sheight=None, parent=None):
        super(CameraNode, self).__init__({}, parent) 
        """
        Constructor.

        @param position The position of the camera (in world space). If None, it will default to CameraNode.__camera_target__.
        @param target   The camera target point (in world space).  If None, it will default to CameraNode.__camera_position__.
        @param up       The camera up point (in world space). If None, it will default to CameraNode.__camera_upvector__.
        @param fov      The field of view (in degrees). If None, it will default to CameraNode.__camera_fov__.
        @param znear    The distance from position to the near clipping plane. If None, it will default to CameraNode.__camera_znear__.
        @param zfar     The distance from position to the far clipping plane. If None, it will default to CameraNode.__camera_zfar__.
        @param swidth   The initial screen width (in pixels). If None, it will default to CameraNode.__camera_swidth__.
        @param sheight  The initial screen height (in pixels). If None, it will default to CameraNode.__camera_sheight__.
        @param parent   The parent SceneGraphItem instance.
        """

        # Register the 'reset' data
        self._restore['_znear']        = znear or self.__camera_znear__
        self._restore['_zfar']         = zfar or self.__camera_zfar__
        self._restore['_screenwidth']  = swidth  or self.__camera_swidth__
        self._restore['_screenheight'] = sheight or self.__camera_sheight__
        self._restore['_fov']          = fov or self.__camera_fov__
        self._restore['_position']     = (position or self.__camera_position__).duplicate()
        self._restore['_target']       = (target or self.__camera_target__).duplicate()
        self._restore['_up']           = (up or self.__camera_upvector__).duplicate()
        self._restore['_viewport']     = self.viewport(self._restore['_fov'], self._restore['_screenwidth'], self._restore['_screenheight'], self._restore['_znear'])

        # Register the 'reset' data
        self._staticdata[QtCore.Qt.DisplayRole, SceneGraphItem.Fields.NAME]        = "Camera"
        self._staticdata[QtCore.Qt.DecorationRole, SceneGraphItem.Fields.NAME]     = QtGui.QIcon(QtGui.QPixmap(self.__icon__))
        self._staticdata[QtCore.Qt.ToolTipRole, SceneGraphItem.Fields.NAME]        = "Camera"
        self._staticdata[QtCore.Qt.AccessibleTextRole, SceneGraphItem.Fields.NAME] = "Camera"
        self._staticdata[QtCore.Qt.EditRole, SceneGraphItem.Fields.NAME]           = "Camera"

        self.reset()

    def resize(self, width, height):
        """
        Resizes the virtual screen.
        """
        self._viewport = self.viewport(self._fov, width, height, self._znear)
        self._screenminsize = min(width, height)
        self._screenwidth = width
        self._screenheight = height

        self._rotationspeed = self.__camera_max_screen_rotation__ / self._screenminsize
        self._pixelradians = math.radians(self._rotationspeed) 

    def viewport(self, fov, width, height, znear):
        """
        Calcaultes the Viewport dimensions.

        @param fov    The Field of View angle (in degrees).
        @param width  The screen width (in pixels).
        @param height The screen height (in pixels).
        @param znear  The z position of the near clipping plane.
        @returns      A tuple of (left, right, bottom, top) of the viewing frustrum at znear.
        """
        # Figure out the viewport rectangle that contains the conocircle along it's shortest
        # dimensions; maintain the ratio of the otherdimension.
        if width < height:
            znear_width  = conicwidth(fov, znear)
            znear_height = znear_width * height / width
        else:
            znear_height = conicwidth(fov, znear)
            znear_width  = znear_height * width / height

        # Center the viewport
        zleft   = - 0.5 * znear_width
        zright  =   0.5 * znear_width
        zbottom = - 0.5 * znear_height
        ztop    =   0.5 * znear_height
        
        return (zleft, zright, zbottom, ztop)

    def tumble(self, hdelta, vdelta):
        """
        This is equivalent of rotating the camera around it's target point while maintaining the direction vector; to reflect the change in view the camera will be rotated by the additive inverse of the deltas.

        @param hdelta The horizontal delta (the up vector rotation)
        @param vdelta The vertical delta (the right vector rotation)

        @see Maya Rotation defintions (http://download.autodesk.com/global/docs/maya2013/en_us/index.html?url=files/Viewing_the_scene_Tumble_track_dolly_or_tilt_the_view.htm,topicNumber=d30e15213)
        @see Rotation algorithm (http://gamedev.stackexchange.com/questions/20758/how-can-i-orbit-a-camera-about-its-target-point)
        """
        # Get the current look at vector (e.g inverse direction)
        idirection = self._position - self._target

        # Rotate the y-axis (aka 'up' vector) which is the plane normal coming out of the x-z plane.
        # The x-z plane is typically the horizontal plane and the yaw angle is measured by the horizontal delta parameter.
        hrotation  = - hdelta * self._pixelradians
        M          = Matrix4x4.rotation( hrotation, self.__camera_upvector__ )
        idirection = M * idirection
        self._up   = M * self._up
        right      = (self._up ^ idirection).normalized()

        # Now rotate the x-axis (aka 'right' vector) which is the plane normal coming out of the y-z plane.
        # The y-z plane is typically the vertical plane and the pitch angle is measured by the vertical delta parameter.
        vrotation  = - vdelta * self._pixelradians
        M          = Matrix4x4.rotation( vrotation, right )
        idirection = M * idirection
        self._up   = M * self._up

        # Update the camera's position
        self._position = self._target + idirection

    def roll(self, delta):
        """
        Executes a rotation operation around the z-axis

        This is equivalent of rotating the camera around it's z-axis; to reflect the change in view the camera will be rotated by the additive inverse of the delta.

        @param delta The rotation delta (the change in rotating around the direction vector)
        """
        # Get the current look at vector (e.g inverse direction)
        direction = self._target - self._position

        # Rotate the z-axis (aka 'look at' vector) which is the plane normal coming out of the x-y plane.
        # Since we're rotating the x-y plane, the concept of vertical or horizontal delta doesn't apply; it's
        # a straight up spin of the look at vector
        rotation = - delta * self._pixelradians
        M        = Matrix4x4.rotation( rotation, direction )
        self._up = M * self._up

    def track( self, hdelta, vdelta ):
        """
        Executes a translate operation the x-y axis.

        This is equivalent of moving the scene along the x-y axis; to reflect the change in view the camera will be translated by the additive inverse of the deltas.

        @param hdelta The horizontal delta (the change in distance along the right vector)
        @param vdelta The vertical delta (the change in distance along the up vector)
        """
        # We need to calculation a ratio of pixels to world units for speed.
        # Get the direction vector (normalized) and the distance.
        direction = self._target - self._position
        distance  = direction.length()
        direction = direction.normalized()

        # Get the view width at the point along the z-axis and build a pixels to unit ratio
        viewwidth = conicwidth(self._fov, distance)
        factor = viewwidth / self._screenminsize

        # Update the right vector
        right = direction ^ self._up

        # Calcaulte the x-y axis translation vector
        translation = right * (- hdelta * factor) + self._up * (- vdelta * factor)

        # Move the Position and Target
        self._position += translation
        self._target += translation

    def dolly( self, delta ):
        """
        Executes a translate operation the z-axis.

        This is equivalent of moving the camera along the z-axis; to reflect the change in view the camera will be translated by the additive inverse of the delta.

        @param delta The translation delta (the change in distance along the direction vector)
        """
        # We need to calculation a ratio of pixels to world units for speed.
        # Get the direction vector (normalized) and the distance.
        direction = self._target - self._position
        distance  = direction.length()
        direction = direction.normalized()

        # Get the view width at the point along the z-axis and build a pixels to unit ratio
        viewwidth = conicwidth(self._fov, distance)
        factor = viewwidth / self._screenminsize

        # Calculate the translation along the direction vector
        translation = direction * (- delta * factor)

        # Move the Position only; the look at point reamins unchanged.
        self._position += translation

    def zoom( self, delta ):
        """
        Executes a zoom operation.

        This is equivalent of zooming into the scene without moving the camera; to reflect the change in view the camera fov will be scaled by the additive inverse of the delta.

        @param delta The fov delta (the change in fov, in degrees)
        @see http://gamedev.stackexchange.com/questions/30357/3d-zooming-technique-to-maintain-the-relative-position-of-an-object-on-screen
        """
        # Clamp the __camera_fov__ (in degrees) to 1 and 180
        self._fov  = sorted((1, self._fov - delta, 180))[1]
        self._viewport = self.viewport(self._fov, self._screenwidth, self._screenheight, self._znear)
