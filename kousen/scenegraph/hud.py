# -*- coding: utf-8 -*-
"""
This module provides HUD specializations of viewport nodes.
"""
from kousen.scenegraph import ViewportNode
from kousen.scenegraph.quadric import QuadricGnomonNode

class CameraHUDNode(ViewportNode):
    """
    The Camera HUD Node provides a Camera Data HUD implementation of a AbstractSceneGraphItem.
    """
    # Additional Meta Information
    __category__     = "HUD Node"
    __icon__         = ":/icons/hud-camera.png"
    __description__  = "Camera HUD"
    __instantiable__ = True

    def __init__(self, camera=None, parent=None):
        """
        Constructor.

        @param camera   An instance of CameraNode to monitor.
        @param parent   The parent AbstractSceneGraphItem instance.
        """
        super(CameraHUDNode, self).__init__("CameraHUD", parent)
        self._camera = camera
        self._gnomon = QuadricGnomonNode(0.4, 0.005, 0.05, 0.8, 32, 32, 5, self)
        self.appendChild( self._gnomon )

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