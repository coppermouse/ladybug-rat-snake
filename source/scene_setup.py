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

                    if xy in [
                        (19,19),(18,19),(17,19),(19,18),(19,17),
                        (12,12),(12,13),(12,14),(13,12),(14,12),
                        (12,19),(13,19),(14,19),(12,18),(12,17),
                        (19,12),(18,12),(17,12),(19,13),(19,14),
                        ]:
                        #continue
                        pass

                    if Resource.imgs[6].get_at(xy).a in (255,254,253):
                        WalkNode( (x,y,0), (x+.5,y+.5,1/8) ) 


                for z in range(1,7):
                    rz = z
                    if rz == 6: rz += 0.1
                    for xy in range2d( (12,20),(12,20) ):
                        x,y = xy
                        WalkNode( (x,y,z), (x+.5,y+.5,1/8+(1/7)*15*rz) ) 
 


                for z in range(7):            
                  for ip, wn in WalkNode.walk_nodes.items():

                    oz = ip[2]
                    if oz != z: continue
                    ip = ip[:2]


                    for adj in [(-1,0),(1,0),(0,-1),(0,1)]:

                        t = tuple([*offset2d(ip,adj),z])
                        if z == 0:
                            try:

                                if not (Resource.imgs[9].get_at(ip) == (0,0,0,255) or Resource.imgs[9].get_at(t[:2]) == (0,0,0,255)):
                                    if  Resource.imgs[9].get_at(ip) != Resource.imgs[9].get_at(t[:2]):
                                        continue
                            except IndexError:
                                pass
                        try:
                            wn.adjs.add(WalkNode.walk_nodes[ t])
                        except KeyError:
                            pass
                

                for z in range(6):

                    xy = (12,12) if z % 2 == 0 else (19,19)


                    l,r = WalkNode.walk_nodes[(*xy,z)], WalkNode.walk_nodes[(*xy,z+1)]
                    l.adjs.add(r)
                    r.adjs.add(l)

                #WalkNode.walk_nodes[()]



            wm = wall_margins = 2

            Wall( ( 0-wm,  32+wm,), ( 0-wm,  0-wm  ) )
            Wall( ( 0-wm,  0-wm, ), ( 32+wm, 0-wm  ) )
            Wall( ( 32+wm, 0-wm, ), ( 32+wm, 32+wm ) )
            Wall( ( 32+wm, 32+wm,), ( 0-wm,  32+wm ) )


