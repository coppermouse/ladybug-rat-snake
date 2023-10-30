# ----------------------------------------
# file: display.py
# ----------------------------------------

import pygame

display_mode_flags = pygame.SCALED | pygame.NOFRAME
vsync = False
fps = 600

near = ( 4, 200 )

scale_in_environment_max = 160

map_margin = 80
map_size = 32
map_factor = 12
map_color = ( 100, 200, 134, 20 )

mask_tile_size = 10
mask_map_solid_color = ( 255, 255, 255, 40 )


visor_factor = 8
ray_step_size = 24

