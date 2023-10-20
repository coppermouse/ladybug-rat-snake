# ----------------------------------------
# file: target.py
# class: Target
# ----------------------------------------

import pygame
from signal_listener import SignalListener
import numpy as np
from mouse import Mouse
from wall import Wall
from display import Display
from common import lerp2d
from ray import ray
from globals import g
from _resource import Resource
from project import project

class Target( SignalListener ):

    target_hit = None
    focus_point = None

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on make map', 'on draw', 'on frame', 'on mouse motion' )


    def get_receive_signal_order( _type: str ) -> int:
        return 132


    @classmethod
    def on_signal( cls, _type: str, message = None ):
        from visor import Visor

        if _type == 'on make map':
            surface, factor, offset = message

            p = Target.get_wall_hit()
            if p is not None:
                pygame.draw.circle( surface, 'green',  p * factor + offset , 5, 1  )

            aim = Resource.imgs[0]
            dp = ( np.array( Target.target_hit[:2] ) ) * factor + offset
            surface.blit( aim, aim.get_rect( center = dp ) )

            if Target.focus_point:
                dp = ( np.array(Target.focus_point[:2]) ) * factor + offset
                pygame.draw.circle( surface, 'cyan', dp, 9, 1 )

        elif _type == 'on draw':
            aim = Resource.imgs[0]
            Display.screen.blit( aim, aim.get_rect( center = Mouse.get_internal_position() ) )

        elif _type == 'on frame':
            target_vector = Target.get_real_vector()
            cls.target_hit = ray(
                cls.get_start(),
                target_vector, 
                Visor.visor, 
            )
            if cls.target_hit is None:
                cls.target_hit = cls.get_start() + target_vector * Target.get_distance_to_wall()

            if cls.focus_point is not None:
                a = Mouse.get_internal_position()
                b = project( cls.focus_point )[0]
                f = g['mouse-to-cursor-factor']
                Mouse.set_actual_position( lerp2d( a, b, f ) )

        elif _type == 'on mouse motion':
            cls.focus_point = cls.target_hit


    def get_vector():
        from camera import Camera
        x, y = Mouse.get_normalized_internal_position()
        factors = Camera.factors
        rm = Camera.get_rotation_matrix_inv()
        v = np.array( ( x / factors[0], 1, y / factors[1] ) )
        r = v.dot( rm )
        return r


    @classmethod
    def get_real_vector( cls ): # this point in the right direction.
        return cls.get_vector() * -1


    def get_start():
        from camera import Camera
        return Camera.get_scene_position()


    @classmethod
    def get_wall_hit( cls ):
        for wall in cls.get_hit_detectable_walls():
            p = wall.get_intersect_by_target()
            if p is None: continue
            return p


    @classmethod
    def get_distance_to_wall( cls ):
        for wall in cls.get_hit_detectable_walls():
            v = Target.get_real_vector()[:2]
            s = cls.get_start()[:2]
            p = wall.get_intersect( ( s, s + v * 1000 ) )
            if p is None: continue
            return np.linalg.norm( p - s ) / np.linalg.norm( v )
        raise Exception()


    @classmethod
    def get_hit_detectable_walls( cls ):
        v = cls.get_real_vector()[:2]
        for wall in Wall.walls:
            if v.dot( wall.get_normal() ) > 0:
                yield wall


