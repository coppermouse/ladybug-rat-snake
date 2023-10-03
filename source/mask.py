# ----------------------------------------
# file: mask.py
# class: Mask
# author: coppermouse
# ----------------------------------------

import pygame
from display import Display
from signal_listener import SignalListener

class Mask( pygame.mask.Mask, SignalListener ):

    tile_size = 10

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on draw', 'on setup' )


    def get_receive_signal_order( _type: str ) -> int:
        return 95


    @classmethod
    def on_signal( cls, _type: str, message = None ):
        if _type == 'on draw':
            cls.on_draw()
        elif _type == 'on setup':
            cls.on_setup()


    @classmethod
    def on_setup(cls):
        world = pygame.image.load( '../assets/world.png' ) # TODO: use path.py
        tile_size = cls.tile_size
        cls.solid_mask = Mask( ( world.get_size()[0]*tile_size, world.get_size()[1]*tile_size ))

        tile = pygame.mask.Mask( (tile_size,)*2, fill = True )
        for x in range( world.get_size()[0] ):
            for y in range( world.get_size()[1] ):
                a = world.get_at((x,y)).a
                if a < 250:
                    cls.solid_mask.draw( tile, ( x*tile_size, y*tile_size ) )


    @classmethod
    def on_draw(cls):
        return # disable debug
        Display.screen.blit( cls.solid_mask.to_surface(), (0,0) )


