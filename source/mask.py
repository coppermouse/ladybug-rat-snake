# ----------------------------------------
# file: mask.py
# class: Mask
# ----------------------------------------

import pygame
import numpy as np
from signal_listener import SignalListener
from _resource import Resource
from config import mask_tile_size
from common import range2d
from config  import mask_map_solid_color

class Mask( pygame.mask.Mask, SignalListener ):

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on level load', 'on make map' )


    def get_receive_signal_order( _type: str ) -> int:
        return 95


    @classmethod
    def on_signal( cls, _type: str, message = None ):
        
        if _type == 'on level load':
            level = message
            cls.on_level_load( level )

        elif _type == 'on make map':
            surface, factor, offset = message
            m = Mask.solid_mask.to_surface( setcolor = mask_map_solid_color, unsetcolor = (0,0,0,0) )
            m = pygame.transform.scale( m, np.array( m.get_size() ) * ( factor / mask_tile_size ))
            surface.blit( m, (offset,)*2 )


    @classmethod
    def on_level_load( cls, level ):
        world = Resource.imgs[{1:3,2:4}[level]]
        tile_size = mask_tile_size
        cls.solid_mask = Mask( np.array( world.get_size() ) * tile_size )

        tile = pygame.mask.Mask( (tile_size,)*2, fill = True )
        for xy in range2d( *world.get_size() ):
            a = world.get_at( xy ).a
            if a < 250:
                cls.solid_mask.draw( tile, np.array( xy ) * tile_size )


