# ----------------------------------------
# file: level_loader.py
# class: LevelLoader
# ----------------------------------------

import pygame
from signal_listener import SignalListener
from signal_manager import SignalManager

class LevelLoader( SignalListener ):

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on event', )


    def get_receive_signal_order( _type: str ) -> int:
        return 101


    @classmethod
    def on_signal( cls, _type: str, message = None ):

        if _type == 'on event':
            event = message
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    SignalManager.send_signal( 'on level load', 1 )


