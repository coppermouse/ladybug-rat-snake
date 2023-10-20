# ----------------------------------------
# file: laser_shadow.py
# class: LaserShadow
# ----------------------------------------

import numpy as np
from line import Line
from hero import Hero
from target import Target

class LaserShadow( Line ):

    draw_order = -1

    def __init__(self):
        Line.__init__( self, color = 'black' )
        LaserShadow.laser_shadow = self

    @property
    def start( self ):
        return np.array( list(Hero.hero.scene_position[:2]) + [0] )


    @property
    def end( self ):
        return tuple(Target.target_hit[:2]) + (0,)


