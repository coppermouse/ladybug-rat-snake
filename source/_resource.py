# ---------------------------------------- 
# file: _resource.py
# class: Resource
# ----------------------------------------

import pygame
from signal_listener import SignalListener
from path import is_file
from path import load_image
from path import load_sound
from path import load_font

class Resource( SignalListener ):

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on setup', )

    
    def get_receive_signal_order( _type: str ) -> int:
        return 0


    @classmethod
    def on_signal( cls, _type: str, message = None ):

        # load images and sounds
        for key, project_path_struct, load in [
            ( 'imgs', ':/assets/imgs/img{0}.png', lambda a: load_image(a).convert_alpha() ),
            ( 'snds', ':/assets/sfxs/sfx{0}.ogg', lambda a: load_sound(a) ),
        ]:
            data = dict()
            setattr( cls, key, data )
            for i in range( 2**8 ):  # <-- have a hard limit instead of while loop, 
                                     #     while loop can freeze the game if bugs
                project_path = project_path_struct.format( str(i).zfill(3) )
                if is_file( project_path ):
                    data[i] = load( project_path )
                else:
                    break

        # --- load fonts
        if not pygame.font.get_init():
            pygame.font.init()

        fn = 'UbuntuMono-Regular.ttf'
        cls.fonts = {
            size: load_font( f':/assets/{fn}', size ) for size in [ 14, 16, 18, 21, 48 ] }
        # ---


