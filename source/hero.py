# ----------------------------------------
# file: hero.py
# class: Hero
# author: coppermouse
# ----------------------------------------

import pygame
from camera import Camera
from mask import Mask
from display import Display
from signal_listener import SignalListener
from rotate import rotate
import numpy as np
from projection import projection_vertices

class Hero( SignalListener ):

    direction = 0
    position = pygame.math.Vector3( 9, 10, -12.4 )

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on event', 'on frame', 'on draw' )


    def get_receive_signal_order( _type: str ) -> int:
        return 100


    @classmethod
    def on_signal( cls, _type: str, message = None ):
        if _type == 'on event':
            event = message
            if event.type == pygame.MOUSEMOTION:
                cls.direction += event.rel[0]

        elif _type == 'on frame':
            for k, delta in ( (pygame.K_w,-1), (pygame.K_s,1) ):
                if pygame.key.get_pressed()[k]:
                    v = 0.1 * delta
                    _np = cls.position + pygame.math.Vector3( v,0,0 ).rotate( -Hero.direction , (0,0,1) )
                    if _np[0] >= 0 and _np[1] >= 0 and _np[0] < 32 and _np[1] < 32:
                        if not Mask.solid_mask.overlap( *Hero.get_collision_mask( _np[:2] )):
                            cls.position = _np

        elif _type == 'on draw':
            screen = Display.screen
            half_screen_size = np.array(screen.get_size()) // 2
            points = [ pygame.math.Vector3( ( Hero.position ) ) + pygame.math.Vector3( 0.4,0,0).rotate(v+45,(0,0,1)) 
                for v in range(0,360,360//4)
            ]

            points.append( pygame.math.Vector3( Hero.position  ) + pygame.math.Vector3(-1,0,0).rotate( -Hero.direction, (0,0,1) )  )

            points = [ tuple(p) for p in points ]

            points = np.array( points ) - ( list( Camera.get_position_xy() ) + [ Camera.get_position_z() ])
            rotate( points, (0,0,1), -Camera.get_angle() )
            rotate( points, (1,0,0), 0.4 )

            projected_points = projection_vertices( points, ( half_screen_size * Camera.factors ), half_screen_size )

            for projected_point in projected_points:
                screen.set_at( tuple( map( int, projected_point )), 'white' )

            mask, offset = cls.get_collision_mask( cls.position[:2] )
            Display.screen.blit( mask.to_surface( setcolor = 'blue' ), offset )
            pygame.draw.rect( Display.screen, 'red', (*[ int(c*Mask.tile_size) for c in cls.position[:2]  ], 1, 1 ), 1 )


    def get_collision_mask( new_pos ):
        assert len(new_pos) == 2, len(new_pos)
        mask = pygame.mask.Mask( (7,7), fill = True )
        return mask, [ int(c*Mask.tile_size)-3 for c in new_pos ] 


