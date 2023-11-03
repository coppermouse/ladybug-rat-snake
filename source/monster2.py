# ----------------------------------------
# file: monster.py
# class: Monster
# ----------------------------------------

import math
import pygame
import random
from common import normalize_angle
import numpy as np
from in_environment import InEnvironment
from display import Display
from _resource import Resource
from signal_listener import SignalListener
from common import lerp
from walk_node import WalkNode
cool_down = 20
from solid_color_surface import solid_color_surface
from functools import lru_cache

class Monster2( InEnvironment, SignalListener ):

    monsters = set()
    draw_order = -1

    def __init__(self, walk_node ):
        self.walk_node = walk_node
        Monster2.monsters.add(self)
        self.walk_cool_down = 0
        self.prev_walk_node = walk_node
        InEnvironment.in_environments.add( self )
        self.walk_anim = 0

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on frame', 'on event' )


    def get_receive_signal_order( _type: str ) -> int:
        return 109

    @classmethod
    @lru_cache(maxsize = 1)
    def get_top_mask(cls, a):

        a = normalize_angle(a)

        if 0 <= a < math.pi/2:
            return pygame.transform.flip( Resource.imgs[11], False, False )
        if math.pi/2 <= a < math.pi:
            return pygame.transform.flip( Resource.imgs[11], False, True )
        if math.pi <= a < math.pi*1.5:
            return pygame.transform.flip( Resource.imgs[11], True, True )
        return pygame.transform.flip( Resource.imgs[11], True, False )

    @classmethod
    def on_signal( cls, _type: str, message = None ):
        from camera import Camera

        if _type == 'on frame':



            for m in cls.monsters:
                if m.walk_anim > 0:
                    m.walk_anim += 1


                if 1:
                        x,y,z = m.walk_node.int_position
                        if cls.get_top_mask(Camera.top_view_angle).get_at((x,y)).b == 255:
                            m.draw_order = 10
                        else:
                            m.draw_order = -1
                        if x in range(12,20) and y in range(12,20):
                            m.draw_order = z
 

                if m.walk_cool_down > 0:
                    m.walk_cool_down -= 1


                    continue


                jjj = random.randrange(20)== 0

                b = m.walk_node
                
                l = random.sample(m.walk_node.adjs,len(m.walk_node.adjs))
                assert len(l) in range(1,5), len(l)
                assert m.walk_node not in l
            
                b = m.walk_node
                for adj_wn in l:

                    if adj_wn.color < m.walk_node.color or jjj:
                        if adj_wn.hold: continue
                        m.walk_node.hold = None
                        m.prev_walk_node = m.walk_node
                        m.walk_node = adj_wn
                        adj_wn.hold = m
                        m.walk_cool_down = cool_down

                        if m.walk_anim == 0:
                            m.walk_anim = random.randrange(200)
                       #if z > 0: m.draw_order = 5

                        break

                if b == m.walk_node:
                    m.walk_anim = 0

                #l = { wn: wn.hold for wn in WalkNode.walk_nodes.values() if wn.hold }
                #print("---")
                #for k,v in l.items():
                #3    print(k,v)
                l = [ wn.hold for wn in WalkNode.walk_nodes.values() if wn.hold ]
                assert len(l) == len(set(l)), l

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
 
    def f(self):
        return self.walk_cool_down/cool_down

    @property
    def scene_position( self ):
    

        self.lff = self.f()
        r = lerp(
            self.walk_node.scene_position,
            self.prev_walk_node.scene_position,
            self.lff
        )
        return r

    @lru_cache
    def get_scaled(index,scale,fog):

        scale = scale / 91

        if scale > 1.1: scale = 1.1

        s = pygame.transform.smoothscale( Resource.imgs[index], np.array(Resource.imgs[index].get_size())*scale )
        solid_color_surface( s,fog )
        return s

    def environment_draw( self, point, scale, fog ):
        from draw_text import draw_text
        screen = Display.screen
        s = Monster2.get_scaled( ( 12+(self.walk_anim//10)%2) if self.walk_anim else 10  ,round(scale), round(fog,1))
        #draw_text(str(self.walk_node.scene_position),point, color = 'darkred'  )
        #s = pygame.transform.smoothscale( Resource.imgs[8], (scale,)*2 )


        screen.blit( s, s.get_rect( midbottom = point ) )


