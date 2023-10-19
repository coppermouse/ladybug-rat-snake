# ----------------------------------------
# file: wall.py
# class: Wall
# ----------------------------------------

import pygame
import numpy as np
from line_intersect import real_line_intersect
from signal_listener import SignalListener

target_length_on_intersect = 1000

class Wall( SignalListener ):

    walls = set()

    def __init__( self, start, end ):
        self.start, self.end = np.array( start ), np.array( end )
        Wall.walls.add( self )


    def get_listen_to_signal_types() -> list[str]:
        return ( 'on make map', )


    def get_receive_signal_order( _type: str ) -> int:
        return 133


    @classmethod
    def on_signal( cls, _type: str, message = None ):
        from target import Target
        if _type == 'on make map':
            surface, factor, offset = message
            hdw = set( Target.get_hit_detectable_walls() )
            for wall in Wall.walls:
                line = np.array( [ wall.start, wall.end ] ) * factor + offset
                pygame.draw.line( surface, 'green' if wall in hdw else 'red', *line )


    def get_normal(self):
        v = self.start - self. end
        return -v[1], v[0]


    def get_intersect( self, line ):
        i = real_line_intersect( ( self.start, self.end ), line )
        if not i: return None
        return np.array(i)


    def get_intersect_by_target( self ):
        from target import Target
        a, b = ( 
            Target.get_start()[:2], 
            Target.get_start()[:2] + Target.get_real_vector()[:2] * target_length_on_intersect )
        return self.get_intersect( ( a,b ) )


