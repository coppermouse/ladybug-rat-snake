# ----------------------------------------
# file: display.py
# class: Display
# author: coppermouse
# ----------------------------------------

import pygame
import numpy as np
from signal_listener import SignalListener

class Display( SignalListener ):
    
    def get_listen_to_signal_types() -> list[str]:
        return ( 'on setup', )


    def get_receive_signal_order( _type: str ) -> int:
        return -2


    @classmethod
    def on_signal( cls, _type: str, message = None ):
        cls.screen = screen = pygame.display.set_mode(
            (1920, 1080), 
            pygame.SCALED | pygame.NOFRAME ,
            # vsync=True
        )

        half_screen_size = np.array(screen.get_size()) // 2


