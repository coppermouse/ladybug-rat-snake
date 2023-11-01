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
    height = 13.5
    type = 0

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on frame', 'on level load')


    def get_receive_signal_order( _type: str ) -> int:
        return 78


    @classmethod
    def on_signal( cls, _type: str, message = None ):
        if _type == 'on frame':
            
            if cls.type == 0:
                cls.top_view_angle += Mouse.get_normalized_internal_position()[0] * g['camera-turn-speed']
            else:
                cls.top_view_angle -= 0.007


        if _type == 'on level load':
            if message == 3:
                Camera.height = 18
                Camera.look_down = 0.5
                Camera.type = 1

    def get_fov():
        return [ math.degrees( math.atan(1/c) ) * 2 for c in Camera.factors ]


    @classmethod
    def get_scene_position( cls ):


        if cls.type == 1:
            f,v = 30, -cls.top_view_angle + math.pi*0.5
            return np.array([16,16,cls.height]) + ( math.cos(v)*f, math.sin(v)*f, 0 )

        else:
            from hero import Hero

            if not Hero.hero: return np.array((.0,.0,.0))

            c = Camera.top_view_angle
            f, z = 20.1, Camera.height
            v = - c - math.pi * 1.5
            xy = Hero.hero.scene_position[:2] + ( math.cos(v)*f, math.sin(v)*f )
            return np.array([ *xy, z ])


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


