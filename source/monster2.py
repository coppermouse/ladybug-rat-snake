# ----------------------------------------
# file: monster.py
# class: Monster
# ----------------------------------------

import pygame
import random
from in_environment import InEnvironment
from display import Display
from _resource import Resource
from signal_listener import SignalListener
from common import lerp

cool_down = 7

class Monster2( InEnvironment, SignalListener ):

    monsters = set()

    def __init__(self, walk_node ):
        self.walk_node = walk_node
        Monster2.monsters.add(self)
        self.walk_cool_down = 0
        InEnvironment.in_environments.add( self )

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on frame', )


    def get_receive_signal_order( _type: str ) -> int:
        return 109


    @classmethod
    def on_signal( cls, _type: str, message = None ):

        if _type == 'on frame':
            for m in cls.monsters:
                if m.walk_cool_down > 0:
                    m.walk_cool_down -= 1
                    continue

                m.prev_walk_node = m.walk_node
                m.walk_node = random.choice( list( m.walk_node.adjs ) )
                m.walk_cool_down = cool_down


    @property
    def scene_position( self ):
        if self.walk_cool_down == 0:
            return self.walk_node.scene_position
        
        r = lerp( self.walk_node.scene_position,  self.prev_walk_node.scene_position, self.walk_cool_down/cool_down)
        print(r)
        return r


    def environment_draw( self, point, scale ):
        screen = Display.screen
        s = pygame.transform.smoothscale( Resource.imgs[8], (scale,)*2 )
        screen.blit( s, s.get_rect( center = point ) )


