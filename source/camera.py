# ----------------------------------------
# file: camera.py
# class: Camera
# ----------------------------------------

import math
import numpy as np
from signal_listener import SignalListener
from mouse import Mouse
from rotate import rotation_matrix_by_axis_and_theta
from globals import g

class Camera( SignalListener ):

    factors = ( 0.8, 2.2 )
    look_down = 0.4
    cached_rm = None
    cached_rm_angle = None
    top_view_angle = 0

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on frame', )


    def get_receive_signal_order( _type: str ) -> int:
        return 78


    @classmethod
    def on_signal( cls, _type: str, message = None ):
        if _type == 'on frame':
            cls.top_view_angle += Mouse.get_normalized_internal_position()[0] * g['camera-turn-speed']


    def get_fov():
        return [ math.degrees( math.atan(1/c) ) * 2 for c in Camera.factors ]


    def get_scene_position():
        from hero import Hero
        c = Camera.get_top_view_angle()
        f, z = 14.1, 13.5
        v = - c - math.pi * 1.5
        xy = Hero.hero.scene_position[:2] + ( math.cos(v)*f, math.sin(v)*f )
        return np.array([ *xy, z ])


    @classmethod
    def get_top_view_angle( cls ):
        return cls.top_view_angle


    @classmethod
    def get_rotation_matrix( cls ):
        # TODO: test how often it hits cache. if not often try cache angle before passing 
        #       it as argument.
        if cls.cached_rm_angle != cls.top_view_angle:
            cls.cached_rm_angle = cls.top_view_angle

            view_top_rotate_matrix = rotation_matrix_by_axis_and_theta( (0,0,1), -cls.top_view_angle )
            look_down_rotate_matrix = rotation_matrix_by_axis_and_theta( (1,0,0), cls.look_down )
            final_rotate_matrix = view_top_rotate_matrix.dot( look_down_rotate_matrix )
            cls.cached_rm = final_rotate_matrix

        return cls.cached_rm


    @classmethod
    def get_rotation_matrix_inv( cls ):
        return np.linalg.inv( cls.get_rotation_matrix() )


