# ----------------------------------------
# file: walk_node.py
# class: WalkNode
# ----------------------------------------

import pygame
import numpy as np
from in_environment import InEnvironment
from display import Display
from _resource import Resource

class WalkNode( InEnvironment ):

    walk_nodes = dict()

    def __init__( self, int_position, scene_position ):
        self.int_position = int_position
        self.adjs = set()
        self.color = 0
        self.hold = None
        self.scene_position = np.array(scene_position)
        #InEnvironment.__init__( self, scene_position )
        WalkNode.walk_nodes[ int_position ] = self

    def environment_draw( self, point, scale ):
        screen = Display.screen
        pygame.draw.circle( screen, self.color if self.color else 'white', point, 6, 1 )


    def __str__( self ):
        return str(self.int_position)

