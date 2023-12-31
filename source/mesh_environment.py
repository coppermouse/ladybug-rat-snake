# ----------------------------------------
# file: mesh_environment.py
# class: MeshEnvironment
# ----------------------------------------

import pygame
from make_environment import make_environment
from signal_listener import SignalListener
from projection import projection_polygons
from camera import Camera
from display import Display
import numpy as np

fog_color = [ 0x43, 0x4a, 0x55 ]

class MeshEnvironment( SignalListener ):

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on draw', 'on setup' )


    def get_receive_signal_order( _type: str ) -> int:
        return 70


    @classmethod
    def on_signal( cls, _type: str, message = None ):

        if _type == 'on setup':

            polygons, colors = make_environment()
            
            # --- sort the polygons based on positions, make sure colors also being sorted becuase its order correspond to polygons order
            sorter = list( zip( polygons, colors ) )
            sorter.sort( key = lambda a:a[0][0][2] + a[0][1][2] + a[0][2][2] + a[0][3][2] )
            polygons = [ c[0] for c in sorter ]
            colors = [ c[1] for c in sorter ]
            # ---

            # numpyify the environment
            polygons = np.array( polygons )
            colors = np.array( colors )

            cls.polygons = polygons
            cls.colors = colors


        if _type == 'on draw':
            screen = Display.screen
            half_screen_size = Display.half_screen_size

            projected_polygons, filtered_colors = projection_polygons( 
                cls.polygons, 
                cls.colors, 
                Camera.get_scene_position(), 
                Camera.get_rotation_matrix(),
                half_screen_size * Camera.factors, 
                half_screen_size, 
                near = ( 4, 200 ),
                edges = [ 1 / c for c in Camera.factors ],
                fog_color = fog_color,
            )

            screen.fill( fog_color )
            for polygon, color in zip( projected_polygons, filtered_colors ):
                pygame.draw.polygon( screen, color, polygon )


