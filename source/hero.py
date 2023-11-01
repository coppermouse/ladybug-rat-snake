# ----------------------------------------
# file: hero.py
# class: Hero
# ----------------------------------------

import pygame
import math
from in_environment import InEnvironment
from camera import Camera
from mask import Mask
from display import Display
from signal_listener import SignalListener
from _resource import Resource
from config import mask_tile_size

class Hero( InEnvironment, SignalListener ):

    hero = None

    def __init__( self, scene_position ):
        InEnvironment.__init__( self, scene_position )
        Hero.hero = self


    def get_listen_to_signal_types() -> list[str]:
        return ( 'on frame', 'on make map' )


    def get_receive_signal_order( _type: str ) -> int:
        return 100


    @classmethod
    def on_signal( cls, _type: str, message = None ):

        if _type == 'on frame':
            for k, delta, right in (
                (pygame.K_w,-1,1), (pygame.K_s,1,1), (pygame.K_a,1,0), (pygame.K_d,-1,0) ):
                if pygame.key.get_pressed()[k]:
                    ca = Camera.top_view_angle

                    f,v = delta * 0.1, -ca + ( math.pi*0.5 * right )
                    _np = cls.hero.scene_position[:2] + ( math.cos(v)*f, math.sin(v)*f )

                    if _np[0] >= 0 and _np[1] >= 0 and _np[0] < 32 and _np[1] < 32:
                        if not Mask.solid_mask.overlap( *Hero.get_collision_mask( _np[:2] )):
                            cls.hero.scene_position[:2] = _np

        elif _type == 'on make map':
            surface, factor, offset = message
            ca = Camera.get_top_view_angle()
            hp = Hero.hero.scene_position[:2] * factor + offset

            pygame.draw.circle( surface, 'green',  hp, 5, 1  )
            f, v = 100, -ca -math.pi/2
            pygame.draw.line( surface, 'white', hp, hp + ( math.cos(v)*f, math.sin(v)*f ) )


    def get_collision_mask( new_scene_position_xy ):
        p = new_scene_position_xy
        assert len( p ) == 2, len( p )
        mask = pygame.mask.Mask( (7,7), fill = True )
        return mask, [ int(c*mask_tile_size)-3 for c in p ] 


    def environment_draw( self, point, scale ):
        screen = Display.screen
        s = pygame.transform.scale( Resource.imgs[1], (scale,)*2 )
        screen.blit( s, s.get_rect( center = point ) )


