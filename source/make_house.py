import pygame
from _resource import Resource

def make_house():

   
    polygons = []

    
    polygon = []


    tile = Resource.imgs[7]

    ff = 7
    zf = 1/ff
    y = 12

    top = False
    colors = []
    for i in range(7):    
    #for i in [1,16,16+15,16+15*2, 16+15*3]:    
        if i == 6: top = True
        i *= 15
        i += 1
        if top:
            i += 1.9
            colors.append( pygame.Color('#070905') )
        else:
            colors.append( pygame.Color('#1b1915') )
        polygons.append( [(12,12,zf*i), (12,20,zf*i), (20,20,zf*i),(20,12,zf*i)][::-1]  )

    zs = 14
    l = 1/8
    state = 0
    for r in range(2):
        for x in range(12,12+8):
            iz = 0 if tile.get_at( (x-12,0) ).r == 255 else -1
            for z in range(0,zs*ff):
                if (tile.get_at( (x-12,z) ).r == 255 and state == 0) or z == zs*ff-1:
                    if z == zs*ff-1: z-= 5
                    for o,i in [ (0,-1), (8,1) ]:
                        polygon = [ (x,y+o,iz*zf+l), (x,y+o,z*zf+l), (x+1,y+o,z*zf+l), (x+1,y+o,iz*zf+l)  ][::i]
                        if r == 1:
                            polygon = [ (y,x,z) for x,y,z in polygon  ][::-1]

                        polygons.append( polygon  )
                        

                        colors.append( pygame.Color('#2a2a28')  )

                    iz = z
                    state = 1
                if tile.get_at( (x-12,z) ).r != 255 and state == 1:

                    for o,i in [ (0,-1), (8,1) ]:
                        polygon = [ (x,y+o,iz*zf+l), (x,y+o,z*zf+l), (x,y+o-0.1*i,z*zf+l), (x,y+o-0.1*i,iz*zf+l)  ][::i]
                        if r == 1:
                            polygon = [ (y,x,z) for x,y,z in polygon  ][::-1]




                        polygons.append( polygon  )
                        colors.append( pygame.Color('#080806')  )
                    iz = z
                    state = 0


    colors = [ tuple(c)[:3] for c in colors ]
    return polygons, colors





