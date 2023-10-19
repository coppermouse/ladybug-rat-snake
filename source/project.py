# ----------------------------------------
# file: project.py
# mehtod: project
# ----------------------------------------

import numpy as np
from display import Display
from camera import Camera
from projection import projection_vertices

def project( vertex ):

    screen = Display.screen
    half_screen_size = np.array(screen.get_size()) // 2

    return projection_vertices(
        np.array( [vertex] ),
        Camera.get_scene_position(),
        Camera.get_rotation_matrix(),
        ( half_screen_size * Camera.factors ),
        half_screen_size,
        near = ( -1, 1 ) # <-- these numbers doesn't matter at the moment
    )[0]


