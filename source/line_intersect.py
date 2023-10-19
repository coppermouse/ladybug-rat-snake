# ---------------------------------------- 
# file: line_intersect.py
# methods: line_intersect, real_line_intersect 
# ----------------------------------------

"""
    This file contain methods relevant to line intersection detection.
"""

import pygame

def line_intersect( i, j ):
    """
        Returns the intersection of two lines assuming infinite lengths. Returns False if no 
        intersection (that means the lines are parallel to each other)

        The actual points of the lines are there to help represent the line, they
        do not represent the start and end-position of the lines because there are none.
    """
    return _m( _f(*i), _f(*j) )


def real_line_intersect( i, j ):
    """
        The "real" line intersect method. This is more real than the line_intersect-method
        because this takes start and end-position of the lines into account.

        Returns the intersection of two lines. Returns False if no intersection. 
    """
    if p := line_intersect(i,j):
        a,b,c,d = i[0],i[1],j[0],j[1]
        if (p-c).dot(p-d) < 0 and (p-a).dot(p-b) < 0: return p
    return False


def _f( a, b ):
    return a[1]-b[1], b[0]-a[0], -(a[0]*b[1] - b[0]*a[1])


def _m( a, b ):
    c  = a[0] * b[1] - a[1] * b[0]
    if c != 0:
        return pygame.math.Vector2( ( a[2]*b[1] - a[1]*b[2] ) / c, ( a[0]*b[2] - a[2]*b[0] ) / c )
    else:
        return False


