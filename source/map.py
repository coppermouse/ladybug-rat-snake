# ----------------------------------------
# file: map.py
# class: Map
# ----------------------------------------

import pygame
import numpy as np
from signal_listener import SignalListener
from signal_manager import SignalManager
from display import Display
from globals import g
from config import map_margin
from config import map_size
from config import map_factor
from config import map_color

class Map( SignalListener ):

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on draw', )


    def get_receive_signal_order( _type: str ) -> int:
        return 128


    @classmethod
    def on_signal( cls, _type: str, message = None ):

        if not g.get('map on'):
            return

        size = np.array( ( map_size * map_factor, ) * 2  ) + map_margin * 2
        surface = pygame.Surface( size, pygame.SRCALPHA )
        surface.fill( map_color )
        SignalManager.send_signal( 'on make map', ( surface, map_factor, map_margin ) )
        Display.screen.blit( surface, (0,0) )


