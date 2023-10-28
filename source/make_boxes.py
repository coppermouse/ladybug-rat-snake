# ----------------------------------------
# file: make_boxes.py
# method: make_boxes
# ----------------------------------------

import pygame
from _resource import Resource

# NOTE: this code is very temp. a better solution is needed if the 
#       prototype is an indicator that this could be a good game worth to work further on

def make_boxes():

    world = Resource.imgs[5]

    polygons = []
    colors = []

    z = 1
    for x in range( world.get_size()[0] ):
        for y in range( world.get_size()[1] ):

            if tuple(world.get_at( (x,y) )) == (0,255,255,255):
                continue

            for offsets, delta in [
                ( [ (0,0,0),  (1,0,0),  (1,1,0),  (0,1,0)  ], None ),
                ( [ (0,0,-1), (1,0,-1), (1,0,0),  (0,0,0)  ], [0,-1] ),
                ( [ (0,1,0),  (1,1,0),  (1,1,-1), (0,1,-1) ], [0,1]  ),
                ( [ (1,0,-1), (1,1,-1), (1,1,0),  (1,0,0)  ], [1,0]  ),
                ( [ (0,0,0),  (0,1,0),  (0,1,-1), (0,0,-1) ], [-1,0] ),
            ]:
 
                polygon = []
                for offset in offsets:
                    dx, dy, dz = offset
                    polygon.append( (x+dx,y+dy,z+dz) )
                polygons.append( polygon )

                r = world.get_at((x,y)).r 
                health = r * ( 20/255 )
                color = pygame.Color( '#6d6967').lerp( '#550055', ( 1-(health/20))*0.5 )

                colors.append(
                    pygame.Color( color ).lerp( 
                        'black', 0.5 if delta is not None else 0 ))

    colors = [ tuple(c)[:3] for c in colors ]
    return polygons, colors


