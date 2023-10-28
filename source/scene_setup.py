# ----------------------------------------
# file: scene_setup.py
# class: SceneSetup
# ----------------------------------------

from signal_listener import SignalListener
from hero import Hero
from monster import Monster
from laser import Laser
from laser_shadow import LaserShadow
from wall import Wall

class SceneSetup( SignalListener ):

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on setup', )


    def get_receive_signal_order( _type: str ) -> int:
        return 75


    @classmethod
    def on_signal( cls, _type: str, message = None ):

        if _type == 'on setup':
            Hero( (17.5,17.5,1/8) )
            Monster( (10.5,10.5,1/8) ) 
            Monster( (17.5,17.5,1/8) ) 
            Laser()
            LaserShadow() 

            wm = wall_margins = 2

            Wall( ( 0-wm,  32+wm,), ( 0-wm,  0-wm  ) )
            Wall( ( 0-wm,  0-wm, ), ( 32+wm, 0-wm  ) )
            Wall( ( 32+wm, 0-wm, ), ( 32+wm, 32+wm ) )
            Wall( ( 32+wm, 32+wm,), ( 0-wm,  32+wm ) )


