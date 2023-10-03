# ----------------------------------------
# file: hero.py
# class: Hero
# author: coppermouse
# ----------------------------------------

import pygame
from in_environment import InEnvironment
from camera import Camera
from mask import Mask
from display import Display
from signal_listener import SignalListener
from rotate import rotate
import numpy as np
from projection import projection_vertices

class Hero( InEnvironment, SignalListener ):

    hero = None

    def __init__( self, scene_position ):
        InEnvironment.__init__( self, scene_position )
        self.direction = 0
        Hero.hero = self

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on event', 'on frame', 'on draw' )


    def get_receive_signal_order( _type: str ) -> int:
        return 100


    @classmethod
    def on_signal( cls, _type: str, message = None ):
        if _type == 'on event':
            event = message
            if event.type == pygame.MOUSEMOTION:
                cls.hero.direction += event.rel[0]

        elif _type == 'on frame':
            for k, delta in ( (pygame.K_w,-1), (pygame.K_s,1) ):
                if pygame.key.get_pressed()[k]:
                    v = 0.1 * delta
                    _np = cls.hero.scene_position + pygame.math.Vector3( v,0,0 ).rotate( -Hero.hero.direction , (0,0,1) )
                    if _np[0] >= 0 and _np[1] >= 0 and _np[0] < 32 and _np[1] < 32:
                        if not Mask.solid_mask.overlap( *Hero.get_collision_mask( _np[:2] )):
                            cls.hero.scene_position = _np

        elif _type == 'on draw':
            mask, offset = cls.get_collision_mask( cls.hero.scene_position[:2] )
            Display.screen.blit( mask.to_surface( setcolor = 'blue' ), offset )
            pygame.draw.rect( Display.screen, 'red', (*[ int(c*Mask.tile_size) for c in cls.hero.scene_position[:2]  ], 1, 1 ), 1 )


    def get_collision_mask( new_pos ):
        assert len(new_pos) == 2, len(new_pos)
        mask = pygame.mask.Mask( (7,7), fill = True )
        return mask, [ int(c*Mask.tile_size)-3 for c in new_pos ] 


    def environment_draw( self, point, scale ):
        pass
