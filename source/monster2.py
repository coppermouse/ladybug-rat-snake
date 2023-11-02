# ----------------------------------------
# file: monster.py
# class: Monster
# ----------------------------------------

import pygame
import random
import numpy as np
from in_environment import InEnvironment
from display import Display
from _resource import Resource
from signal_listener import SignalListener
from common import lerp
from walk_node import WalkNode
cool_down = 20
from functools import lru_cache

class Monster2( InEnvironment, SignalListener ):

    monsters = set()
    draw_order = -1

    def __init__(self, walk_node ):
        self.walk_node = walk_node
        Monster2.monsters.add(self)
        self.walk_cool_down = 0
        self.prev_walk_node = None
        InEnvironment.in_environments.add( self )

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on frame', 'on event' )


    def get_receive_signal_order( _type: str ) -> int:
        return 109


    @classmethod
    def on_signal( cls, _type: str, message = None ):

        if _type == 'on frame':
            for m in cls.monsters:
                if m.walk_cool_down > 0:
                    m.walk_cool_down -= 1
                    continue


                jjj = random.randrange(20)== 0

                for adj_wn in random.sample(m.walk_node.adjs,len(m.walk_node.adjs)):
                    if adj_wn.color < m.walk_node.color or jjj:
                        if adj_wn.hold: continue
                        if m.prev_walk_node:
                            m.prev_walk_node.hold = None
                        m.prev_walk_node = m.walk_node
                        m.walk_node = adj_wn
                        adj_wn.hold = m
                        m.walk_cool_down = cool_down

                        x,y,z = m.walk_node.int_position
                        if x in range(12,20) and y in range(12,20):
                            m.draw_order = z
                        #if z > 0: m.draw_order = 5

                        break
                else:
                    pass


        if _type == 'on event':
            event = message
            if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                for wn in WalkNode.walk_nodes.values():
                    wn.hold = None
                for m in Monster2.monsters:
                    m.prev_walk_node = None
                    m.walk_cool_down = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                for x in range(32):
                    try:
                        Monster2( WalkNode.walk_nodes[(x,0,0)] ) 
                    except KeyError:
                        pass

                    try:
                        Monster2( WalkNode.walk_nodes[(0,x,0)] ) 
                    except KeyError:
                        pass
 
                    try:
                        Monster2( WalkNode.walk_nodes[(x,31,0)] ) 
                    except KeyError:
                        pass

                    try:
                        Monster2( WalkNode.walk_nodes[(31,x,0)] ) 
                    except KeyError:
                        pass
 

    @property
    def scene_position( self ):
        if self.walk_cool_down == 0:
            return self.walk_node.scene_position
        
        r = lerp( self.walk_node.scene_position,  self.prev_walk_node.scene_position, self.walk_cool_down/cool_down)
        return r

    @lru_cache
    def get_scaled(scale):

        scale = scale / 91

        if scale > 1.1: scale = 1.1

        return pygame.transform.smoothscale( Resource.imgs[10], np.array(Resource.imgs[10].get_size())*scale )

    def environment_draw( self, point, scale ):
        screen = Display.screen
        s = Monster2.get_scaled(round(scale))
        #s = pygame.transform.smoothscale( Resource.imgs[8], (scale,)*2 )
        screen.blit( s, s.get_rect( midbottom = point ) )


