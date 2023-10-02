# ----------------------------------------
# file: camera.py
# class: Camera
# author: coppermouse
# ----------------------------------------

import math
import pygame
import numpy as np

class Camera:

    factors = ( 0.8, 2.2 )

    def get_position_xy():
        from hero import Hero
        v = Camera.get_angle()
        return pygame.math.Vector2( Hero.position[:2] ) + pygame.math.Vector2( 14.1, 0 ).rotate_rad( -v-math.pi*1.5 )


    def get_position_z():
        return 1


    def get_camera_position_xyz():
        return np.array ( list( Camera.get_position_xy() ) + [ Camera.get_position_z() ])


    def get_angle():
        from hero import Hero
        return math.radians( Hero.direction ) + math.pi*0.5


