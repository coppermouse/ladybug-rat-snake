# ----------------------------------------
# file: ray.py
# method: ray
# ----------------------------------------

from config import visor_factor
from config import ray_step_size

def ray( origin, direction, visor, distance ):
    
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
        try:
            if visor[ j,k,l ]:
                break
        except IndexError:
            continue

    return target_x, target_y, target_z


