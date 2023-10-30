# ----------------------------------------
# file: boxes.py
# class: Boxes
# ----------------------------------------

import numpy as np
from signal_listener import SignalListener
from _resource import Resource
from common import range2d

class Boxes( SignalListener ):

    array = None

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on level load', )


    def get_receive_signal_order( _type: str ) -> int:
        return 72


    @classmethod
    def on_signal( cls, _type: str, message = None ):

        if _type == 'on level load':
            if message != 2: return
            world = Resource.imgs[5]

            array = np.zeros(world.get_size())

            for xy in range2d( *world.get_size() ):
                a = world.get_at( xy ).r
                array[ xy  ] = a


            Boxes.array = array

