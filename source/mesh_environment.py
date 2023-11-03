# ----------------------------------------
# file: mesh_environment.py
# class: MeshEnvironment
# ----------------------------------------

import pygame
from make_environment import make_environment
from make_boxes import make_boxes
from signal_listener import SignalListener
from projection import projection_polygons
from camera import Camera
from display import Display
from make_house import make_house
import numpy as np

fog_color = [ 0x43, 0x4a, 0x55 ]

class MeshEnvironment( SignalListener ):

    loaded = False
    cache_screen = None

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on draw', 'on setup', 'on level load' )


    def get_receive_signal_order( _type: str ) -> int:
        return 70


    @classmethod
    def on_signal( cls, _type: str, message = None ):

        if _type == 'on level load':
            level = message
            cls.level = message
            polygons, colors = make_environment( level )
            
            # temp solution, we are trying to prototype here...
            if level == 2:
                boxes = make_boxes()
                polygons += boxes[0]
                colors += boxes[1]

               

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

            cls.loaded = True

        if _type == 'on draw':
            if not cls.loaded: return

            if cls.cache_screen:
                Display.screen.blit( cls.cache_screen, (1920//2-620,1080//2-250))
                return

            screen = pygame.Surface( (1240,790) )
            screen.fill( fog_color )
            half_screen_size = Display.half_screen_size

            projected_polygons, filtered_colors = projection_polygons( 
                cls.polygons, 
                cls.colors, 
                Camera.get_scene_position(), 
                Camera.get_rotation_matrix(),
                half_screen_size * Camera.factors, 
                (620,250), 
                near = ( 4, 200 ),
                edges = [ 1 / c for c in Camera.factors ],
                fog_color = fog_color,
                fog_offset = (0,-34,0) if cls.level == 3 else (0,0,0),
                fog_factor = 0.03 if cls.level == 3 else 0.015,
            )

            for polygon, color in zip( projected_polygons, filtered_colors ):
                pygame.draw.polygon( screen, color, polygon )

            cls.cache_screen = screen

            Display.screen.blit( screen, (1920//2-620,1080//2-250))


