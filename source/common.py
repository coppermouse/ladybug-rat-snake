# ---------------------------------------- 
# file: common.py
# methods:
# -------
# diff2d
# euclidean_division2d
# factor2d
# _is
# lerp
# lerp2d
# offset2d
# normalize_angle
# range2d
# ----------------------------------------

import math
from functools import lru_cache

"""
    This file contains generic methods that are can be used by 
    other methods around the project.
"""


def diff2d( a, b ):
    return a[0] - b[0], a[1] - b[1]


def euclidean_division2d( item, denominator ):
    return item[0] // denominator, item[1] // denominator


def factor2d( item, factor ):
    return item[0] * factor, item[1] * factor


def _is( something, what ):
    return bool(
        hasattr( something, 'is_{0}'.format( what ) )
        and getattr( something, 'is_{0}'.format( what ) )
    )


def lerp( a, b, f ):
    return ( a + (b - a) * f )


def lerp2d( a, b, f ):
    return lerp( a[0], b[0], f ), lerp( a[1], b[1], f )


def offset2d( a, b ):
    return a[0] + b[0], a[1] + b[1]


def normalize_angle(v):
    while v < 0:
        v += math.tau
    while v >= math.tau:
        v -= math.tau
    assert 0 <= v <= math.tau, v
    return v


@lru_cache( maxsize = 32 )
def range2d( stops_x, stops_y ):
    #TODO: this could need to clean up. it has too many steps
    stops  = (stops_x, stops_y)
    r = list()
    for y in range( *((stops[1],) if type(stops[1]) == int else stops[1])):
        for x in range( *((stops[0],) if type(stops[0]) == int else stops[0])):
            r.append( (x,y) )
    return r


