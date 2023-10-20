# ---------------------------------------- 
# file: box_line_intersect.py
# method: box_line_intersect
# ----------------------------------------

import numpy as np
from consts import epsilon

def box_line_intersect( line_start, line_direction, box ):
    line_start, line_direction = np.array( line_start ), np.array( line_direction)

    e = epsilon

    intersects = set()
    for pt, pn in [
        ( (0,0,0), (1,0,0) ),
        ( (0,0,0), (0,1,0) ),
        ( (0,0,0), (0,0,1) ),
        ( box, (1,0,0) ),
        ( box, (0,1,0) ),
        ( box, (0,0,1) ),
    ]:
        intersect = _intersect_line_plane(
            line_start, line_direction, np.array(pt), np.array(pn) )

        if intersect is None: continue

        if intersect[0] < -e: continue
        if intersect[0] > box[0] + e: continue
        if intersect[1] < -e: continue
        if intersect[1] > box[1] + e: continue
        if intersect[2] < -e: continue
        if intersect[2] > box[2] + e: continue

        intersects.add( tuple(intersect) )

    assert len( intersects ) == 2

    intersect_distances = { - line_direction.dot( line_start - intersect ) for intersect in intersects }

    sid = sorted_intersect_distances = sorted( intersect_distances )

    return sid[0], sid[1]


def _intersect_line_plane( line_start, line_direction, plane_tangent, plane_normal ):
    ls, ld, pt, pn = line_start, line_direction, plane_tangent, plane_normal


    dot = pn.dot( ld )
    if abs( dot ) > epsilon:
        ld = ld * - pn.dot( ls - pt ) / dot
        return ls + ld

    return None


