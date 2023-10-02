# ----------------------------------------
# file: monster.py
# class: Monster
# author: coppermouse
# ----------------------------------------

from in_environment import InEnvironment
from display import Display

class Monster( InEnvironment ):

    def environment_draw( self, point ):
        screen = Display.screen
        cls = InEnvironment
        screen.blit( cls.monster, cls.monster.get_rect( center = point ) ) # NOTE: temp

