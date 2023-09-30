# ----------------------------------------
# file: make_environment.py
# method: make_enviroment 
# author: coppermouse
# ----------------------------------------

import pygame

def height_map_value_to_z( v ):
    return 5 - v

def make_environment():

    world = pygame.image.load( '../assets/world.png' ) # TODO: use path.py

    f = size_factor = 1
    zf = 0.05
    polygons = list()
    colors = list()

    for x in range( world.get_size()[0] ):
        for y in range( world.get_size()[1] ):

            if tuple( world.get_at((x,y)) ) == (0,0,0,255): continue

            z = height_map_value_to_z( world.get_at( (x,y) ).a )

            for offsets, delta in [
                ( [ (0,0,0),  (1,0,0),  (1,1,0),  (0,1,0)  ], None ),
                ( [ (0,0,-1), (1,0,-1), (1,0,0),  (0,0,0)  ], [0,-1] ),
                ( [ (0,1,0),  (1,1,0),  (1,1,-1), (0,1,-1) ], [0,1]  ),
                ( [ (1,0,-1), (1,1,-1), (1,1,0),  (1,0,0)  ], [1,0]  ),
                ( [ (0,0,0),  (0,1,0),  (0,1,-1), (0,0,-1) ], [-1,0] ),
            ]:
                dx, dy = delta if delta else (0,0)

                # only place polygon if free on the side of the cube
                try:
                    adj_height = height_map_value_to_z( world.get_at( (x+dx,y+dy)  ).a )
                    if adj_height >= z and delta is not None: continue
                    diff = abs(adj_height-z)
                except IndexError:
                    pass

                colors.append(
                    pygame.Color( world.get_at( (x,y) )).lerp( 
                        'black', 0.5 if delta is not None else 0 ))

                polygon = list()
                polygons.append( polygon )

                for dx, dy, dz in offsets:
                    polygon.append(( (x+dx)*f, (y+dy)*f, (z+dz*diff)*zf ))

    colors = [ tuple(c)[:3] for c in colors ]

    return polygons, colors


