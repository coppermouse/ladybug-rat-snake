# ----------------------------------------
# file: monster.py
# class: Monster
# ----------------------------------------

import pygame
from in_environment import InEnvironment
from display import Display
from _resource import Resource

class Monster( InEnvironment ):

    def environment_draw( self, point, scale ):
        return
        screen = Display.screen
        s = pygame.transform.scale( Resource.imgs[2], (scale,)*2 )
        screen.blit( s, s.get_rect( center = point ) )


