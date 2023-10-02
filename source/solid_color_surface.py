# ---------------------------------------- 
# file: solid_color_surface.py
# method: solid_color_surface
# author: coppermouse
# ----------------------------------------

import pygame

def solid_color_surface( surface, color ):
    return pygame.mask.from_surface( surface ).to_surface( unsetcolor=(0,)*4, setcolor=color )


