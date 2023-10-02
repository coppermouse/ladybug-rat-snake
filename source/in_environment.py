# ----------------------------------------
# file: in_environment.py
# class: InEnvironment
# author: coppermouse
# ----------------------------------------

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
                #pygame.draw.circle( screen, 'red', point, 12, 3 )
                screen.blit( cls.monster, cls.monster.get_rect( center = point ) ) # NOTE: temp

        elif _type == 'on setup':
            cls.monster = load_image( ':/assets/monster.png' ) # NOTE: monster thing is temp just 
                                                               # for testing this class

