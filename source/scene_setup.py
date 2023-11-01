# ----------------------------------------
# file: scene_setup.py
# class: SceneSetup
# ----------------------------------------

from signal_listener import SignalListener
from hero import Hero
from monster import Monster
from monster2 import Monster2
from laser import Laser
from laser_shadow import LaserShadow
from wall import Wall
from walk_node import WalkNode
from common import range2d
from _resource import Resource
from common import offset2d

class SceneSetup( SignalListener ):

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on level load', )


    def get_receive_signal_order( _type: str ) -> int:
        return 75


    @classmethod
    def on_signal( cls, _type: str, message = None ):

        if _type == 'on level load':
           
            if message in (1,2):
                Hero( (17.5,17.5,1/8) )
                Laser()
                LaserShadow() 
                Monster( (10.5,10.5,1/8) ) 
                Monster( (17.5,17.5,1/8) ) 


            if message == 3:
                for xy in range2d( 32,32 ):
                    x,y = xy
                    if Resource.imgs[6].get_at(xy).a in (255,254,253):
                        WalkNode( (x,y), (x+.5,y+.5,1/8) ) 

            
                for ip, wn in WalkNode.walk_nodes.items():

                    for adj in [(-1,0),(1,0),(0,-1),(0,1)]:
                        try:
                            wn.adjs.add(WalkNode.walk_nodes[ offset2d(ip,adj) ])
                        except KeyError:
                            pass
                
                Monster2( WalkNode.walk_nodes[(5,5)] ) 



            wm = wall_margins = 2

            Wall( ( 0-wm,  32+wm,), ( 0-wm,  0-wm  ) )
            Wall( ( 0-wm,  0-wm, ), ( 32+wm, 0-wm  ) )
            Wall( ( 32+wm, 0-wm, ), ( 32+wm, 32+wm ) )
            Wall( ( 32+wm, 32+wm,), ( 0-wm,  32+wm ) )


