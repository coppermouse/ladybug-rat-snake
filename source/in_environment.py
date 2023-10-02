# ----------------------------------------
# file: in_environment.py
# class: InEnvironment
# author: coppermouse
# ----------------------------------------

import math
import pygame
from signal_listener import SignalListener
from projection import projection_vertices
from camera import Camera
from display import Display
from path import load_image
import numpy as np

class InEnvironment( SignalListener ):

    in_environments = set()

    def __init__( self, scene_position ):
        scene_position = np.array( scene_position ) 
        self.scene_position = scene_position
        InEnvironment.in_environments.add( self )

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on draw', 'on setup' )


    def get_receive_signal_order( _type: str ) -> int:
        return 182


    @classmethod
    def on_signal( cls, _type: str, message = None ):
        if _type == 'on draw':
            screen = Display.screen
            half_screen_size = np.array(screen.get_size()) // 2
            for ie in cls.in_environments:
                offset = ( list( Camera.get_position_xy() ) + [ Camera.get_position_z() ])

                projected_vertex = projection_vertices(
                    np.array( [ie.scene_position] ),
                    ( half_screen_size * Camera.factors ),
                    half_screen_size,
                    Camera.get_angle(),
                    offset,
                )[0]
                point = tuple(map(int, projected_vertex ))
                scale = (1/np.linalg.norm( ie.scene_position - Camera.get_camera_position_xyz() ))*2500
                if scale > 160: scale = 160
                ie.environment_draw( point, scale )

        elif _type == 'on setup':
            cls.monster = load_image( ':/assets/monster.png' ) # NOTE: monster thing is temp just 
                                                               # for testing this class

            cls.square = load_image( ':/assets/square.png' ) # NOTE: temp
