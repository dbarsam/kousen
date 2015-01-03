# -*- coding: utf-8 -*-
"""
This module provides all utility functions and class defintions for conic operations.
"""
import math

def coniclength(theta, diameter):
    """
    Calculates a length of a cone from the cone angle and and circular conic section's diameter.

    @param theta  The angle of the cone (in degrees).
    @param length The diamater of the conical section
    @returns      The distance down the center of the frustrum
    @see          http://docs.unity3d.com/Manual/FrustumSizeAtDistance.html
    """
    # Basically this is a trig problem and we can use 'tan() = O / A'
    # where O = than() * A and will be the radius of the section.
    theta = math.radians( theta / 2 )
    O     = diameter / 2
    A     = O / math.tan( theta )
    return A

def conicwidth(theta, length):
    """
    Caculates a diameter of a cone's circular conical section from the cone angle and length.

    @param theta  The angle of the cone (in degrees).
    @param length The distance down the center of the frustrum
    @returns      The diameter of the conical section
    @see          http://docs.unity3d.com/Manual/FrustumSizeAtDistance.html
    """
    # Basically this is a trig problem and we can use 'tan() = O / A'
    # where O = than() * A and will be the radius of the section.
    theta = math.radians( theta / 2 )
    A     = length
    O     = math.tan( theta ) * A
    return O * 2
