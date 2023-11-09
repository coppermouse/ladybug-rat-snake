# ----------------------------------------
# file: line.py
# class: Line
# ----------------------------------------

import pygame
import numpy as np
from display import Display
from in_environment import InEnvironment

class Line( InEnvironment ):

    many_scene_positions = True
    invisible = False
    draw_order = 10

    def __init__( self, color ):
        self.color = color
        InEnvironment.in_environments.add( self )


    @property
    def scene_positions( self ):
        return np.array( [ self.start, self.end ] )


    def environment_draw( self, points ):
        if self.invisible: return
        pygame.draw.line( Display.screen, self.color, points[0], points[1] )

 
