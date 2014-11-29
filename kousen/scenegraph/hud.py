# -*- coding: utf-8 -*-
from kousen.math import Matrix4x4
from kousen.scenegraph import ViewportNode

class CameraHUDNode(ViewportNode):
    """
    The Camera HUD Node provides a Camera Data HUD implementation of a AbstractSceneGraphItem.
    """
    # Additional Meta Information
    __category__     = "HUD Node"
    __icon__         = ":/icons/hud-camera.png"
    __instantiable__ = True

    def __init__(self, camera, parent):
        """
        Constructor.

        @param camera   An instance of CameraNode to monitor.
        @param parent   The parent AbstractSceneGraphItem instance.
        """
        super(CameraHUDNode, self).__init__("CameraHUD", parent)
        self._transform = Matrix4x4()
        self._camera = camera

    @property
    def camera(self):
        """
        Convenience property to access the monitored Camera Node.

        @returns An instance of a CameraNode if valid; None otherwise.
        """
        return self._camera

    @camera.setter
    def camera(self, value):
        """
        Convenience property to access the monitored Camera Node.

        @param value An instance of a CameraNode.
        """
        self._camera = value