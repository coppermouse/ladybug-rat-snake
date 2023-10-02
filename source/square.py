# ----------------------------------------
# file: square.py
# class: Square
# author: coppermouse
# ----------------------------------------

import pygame
from in_environment import InEnvironment
from display import Display

class Square( InEnvironment ):

    def environment_draw( self, point, scale ):
        screen = Display.screen
        cls = InEnvironment
        s = pygame.transform.scale( cls.square, (scale,)*2 )
        screen.blit( s, s.get_rect( center = point ) )

