# ----------------------------------------
# file: ray.py
# method: ray
# ----------------------------------------

import numpy as np
from config import visor_factor
from config import ray_step_size
from box_line_intersect import box_line_intersect

def ray( origin, direction, visor ):

    rect = (32,32,2) # NOTE: hard code this for now
    bli = box_line_intersect( origin, direction, rect )
    
    if bli is None: return None

    intersect_start, intersect_end = bli

    origin += direction * intersect_start
    distance = int(np.linalg.norm( intersect_start - intersect_end )) + 1

    x,y,z = origin
    vf = visor_factor
    step_size = ray_step_size

    nvx, nvy, nvz = direction
    target_x, target_y, target_z = x, y, z

    for distance in range( distance * step_size ):
        target_x = float( x + nvx * distance / step_size )
        target_y = float( y + nvy * distance / step_size )
        target_z = float( z + nvz * distance / step_size )
        j,k,l = int( target_x * vf ), int( target_y * vf ), int( target_z * vf )
        if j < 0 or k < 0 or l < 0: continue
        try:
            if visor[ j,k,l ]:
                return target_x, target_y, target_z
        except:
            continue
    return None

