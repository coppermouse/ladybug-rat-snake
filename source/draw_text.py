# ---------------------------------------- 
# file: draw_text.py
# methods: draw_text
# ----------------------------------------

from display import Display
from _resource import Resource

def draw_text( text, position = (0,0), size = 21, surface = None, color = 'white' ):
    fonts = Resource.fonts

    if surface is None: surface = Display.screen

    surface.blit( fonts[ size ].render( text, True, color ), position )


