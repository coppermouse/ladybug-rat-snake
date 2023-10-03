# ----------------------------------------
# file: scene_setup.py
# class: SceneSetup
# author: coppermouse
# ----------------------------------------

from hero import Hero
from monster import Monster
from square import Square
from signal_listener import SignalListener
from in_environment import InEnvironment


class SceneSetup( SignalListener ):

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on setup', )


    def get_receive_signal_order( _type: str ) -> int:
        return 75


    @classmethod
    def on_signal( cls, _type: str, message = None ):
        if _type == 'on setup':
            Hero()
            Monster( (10.5,10.5,-12.4) ) 
            Square( (17.5,17.5,-12.4) ) 


