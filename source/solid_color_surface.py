# ---------------------------------------- 
# file: solid_color_surface.py
# method: solid_color_surface
# ----------------------------------------

import pygame

def solid_color_surface( surface, f ):

    if f < 0.24:
        f = 0


    m = pygame.mask.from_surface( surface ).to_surface( unsetcolor=(0,)*4, setcolor = (0x43,0x4a,0x55,int(f*255)) )
    surface.blit(m,(0,0))
    return surface


