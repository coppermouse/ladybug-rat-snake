# ----------------------------------------
# file: square.py
# class: Square
# author: coppermouse
# ----------------------------------------

from in_environment import InEnvironment
from display import Display

class Square( InEnvironment ):

    def environment_draw( self, point ):
        screen = Display.screen
        cls = InEnvironment
        screen.blit( cls.square, cls.square.get_rect( center = point ) )

