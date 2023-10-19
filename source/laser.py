# ----------------------------------------
# file: laser.py
# class: Laser
# ----------------------------------------

import pygame
from line import Line
from hero import Hero
from signal_listener import SignalListener
from target import Target

class Laser( Line, SignalListener ):

    def __init__(self):
        Line.__init__( self, color = 'magenta' )
        Laser.laser = self


    def get_listen_to_signal_types() -> list[str]:
        return ( 'on make map', )


    def get_receive_signal_order( _type: str ) -> int:
        return 181


    @classmethod
    def on_signal( cls, _type: str, message = None ):
        surface, factor, offset = message
        line = [ c[:2] * factor + offset for c in Laser.laser.scene_positions ]
        pygame.draw.line( surface, Laser.laser.color, *line )


    @property
    def start( self ):
        return Hero.hero.scene_position


    @property
    def end( self ):
        return Target.target_hit


