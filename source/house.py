import math
import numpy as np
import pygame
from display import Display
from make_house import make_house
from signal_listener import SignalListener
from projection import projection_polygons
from camera import Camera
from rotate import rotate
from _resource import Resource

fog_color = [ 0x43, 0x4a, 0x55 ]


wall_color = '#252528' 
frame_color = '#131316'
floor_color = '#1e1e1e' 
inner_wall_color = tuple(pygame.Color('#161616'))[:3]


def make_wall(side):
            tile = Resource.imgs[7]

            walls = []

            colors = []            
            h = height = 1/7
            for x in range(8):
                ly = 0
                state = 0 if tile.get_at((x,0)).r != 255 else 1
                l = 0

                if state == 1:
                            wall = [(0,0,0),(1,0,0),(1,0,0.1),(0,0,0.1)][::1]
                            wall = [ (x,z,y) for x,y,z in wall ]
                            wall = np.array(wall, dtype = np.float64)
                            wall += (12+x,12,0+1/8)
                            walls.append(wall)
                            colors.append(frame_color)



                for y in range(100-7):
                    if (tile.get_at((x,y)).r == 255 and state == 0) or y == 99-7:
                        l = y
                        wall = [(0,0,0),(1,0,0),(1,0,h*(y-ly)),(0,0,h*(y-ly))][::1]
                        wall = [ (x,y,z) for x,y,z in wall ]
                        wall = np.array(wall, dtype = np.float64)
                        wall += (12+x,12,ly*h+1/8)
                        walls.append(wall)
                        colors.append(wall_color)

                        if y != 99-7:
                            wall = [(0,0,0),(1,0,0),(1,0,0.1),(0,0,0.1)][::1]
                            wall = [ (x,z,y) for x,y,z in wall ]
                            wall = np.array(wall, dtype = np.float64)
                            wall += (12+x,12,y*h+1/8)
                            walls.append(wall)
                            colors.append(frame_color)



                        state = 1
                    elif (tile.get_at((x,y)).r != 255 and state == 1):
                        state = 0
                        ll = (y-l)*h

                        if tile.get_at((x-1,l)).r != 255: 
                            wall = [(0,0,0),(.1,0,0),(.1,0,ll),(0,0,ll)][::1]
                            wall = [ (y,x,z) for x,y,z in wall ]
                            wall = np.array(wall, dtype = np.float64)
                            wall += (12+x,12,l*h+1/8)
                            walls.append(wall)
                            colors.append(frame_color)

                        if tile.get_at((x+1,l)).r != 255: 
                            wall = [(0,0,0),(.1,0,0),(.1,0,ll),(0,0,ll)][::-1]
                            wall = [ (y+1,x,z) for x,y,z in wall ]
                            wall = np.array(wall, dtype = np.float64)
                            wall += (12+x,12,l*h+1/8)
                            walls.append(wall)
                            colors.append(frame_color)




                        ly = y

            walls = np.array(walls)
            rotate( walls.reshape(-1,3), (0,0,1), math.tau*(side/4), (16,16,0) )
            return walls, colors


class House( SignalListener ):

    loaded = False

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on draw', 'on level load' )


    def get_receive_signal_order( _type: str ) -> int:
        return 106


    @classmethod
    def on_signal( cls, _type: str, message = None ):

        if _type == 'on draw':

            if not cls.loaded: return

            screen = Display.screen
            half_screen_size = Display.half_screen_size

            outer_wall_visible = set()
            for e, inner_wall in enumerate(cls.inner_walls):
                r = projected_polygons, filtered_colors = projection_polygons( 
                    np.array([inner_wall]), 
                    np.array([[0,0,0]]), 
                    Camera.get_scene_position(), 
                    Camera.get_rotation_matrix(),
                    half_screen_size * Camera.factors, 
                    half_screen_size, 
                    near = ( 4, 200 ),
                    edges = [ 1 / c for c in Camera.factors ],
                    fog_color = fog_color,
                )
                if len(r[0]) == 0: outer_wall_visible.add(e)

            outer_wall_visible = frozenset(outer_wall_visible)

            a, b = cls.set[outer_wall_visible]

            projected_polygons, filtered_colors = projection_polygons( 
                *cls.set[outer_wall_visible], 
                Camera.get_scene_position(), 
                Camera.get_rotation_matrix(),
                half_screen_size * Camera.factors, 
                half_screen_size, 
                near = ( 4, 200 ),
                edges = [ 1 / c for c in Camera.factors ],
                fog_color = None,
            )

            for polygon, color in zip( projected_polygons, filtered_colors ):
                pygame.draw.polygon( screen, color, polygon )


        elif _type == 'on level load':
            if message != 3: return
            cls.loaded = True
            h = 1/7
            cx, cy = corner = 12,12
            width, height = 8, 12
            rw = row_width = 1

            polygons = [ [(cx,cy,0),(cx+width,cy,0),(cx+width,cy,height),(cx,cy,height)][::-1]  ]
            colors = [ inner_wall_color ] * 4

            #polygons, colors = make_house()
            polygons = np.array( polygons, dtype=np.float64 )


            inner_wall_colors = np.array( colors )

            polygons = np.concatenate(
                [
                    rotate( polygons.copy().reshape( (-1,3) ), (0,0,1), math.tau*(i/4), (16,16,0)).reshape(-1,4,3)  
                    for i in range(4)
                ])
            inner_wall_polygons = polygons.copy()


            wall_polygons = [None]*4
            wall_colors = [None]*4

            
            floors = [[(12,12,z*15*h),(20,12,z*15*h),(20,20,z*15*h),(12,20,z*15*h)] for z in [0,1,2,3,4,5,6.125]]
            floors_colors = [ floor_color]*len(floors)


            floors = np.array( floors )
            floors_colors = np.array( floors_colors )
            floors += (0,0,h)
            for side in range(4):
                wall_polygons[side], wall_colors[side] = make_wall(side)
                colors += wall_colors[side]

            cls.inner_walls = polygons

            polygons = np.concatenate( [ polygons ] + [ wall_polygons[i] for i in range(4)] )


            print(wall_colors) 
            floors_colors = [ tuple(pygame.Color(c))[:3] for c in floors_colors ]
            for i in range(4):
                wall_colors[i] = [ tuple(pygame.Color(c))[:3] for c in wall_colors[i] ]

            cls.set = dict()
            for k in j():

                assert len(inner_wall_polygons) == len(inner_wall_colors), (len(inner_wall_polygons), len(inner_wall_colors))

                cls.set[k] = (
                    np.concatenate( [ inner_wall_polygons ] + [floors ] + [ wall_polygons[i] for i in k ] ),
                    np.concatenate( [ inner_wall_colors ] + [floors_colors]+[ wall_colors[i] for i in k ] ),

                )




def j():
    import itertools

    stuff = {0,1,2,3}
    for L in range(len(stuff) + 1):
        for subset in itertools.combinations(stuff, L):
            yield frozenset(subset)

