# ----------------------------------------
# file: mouse.py
# class: Mouse
# ----------------------------------------

import pygame
import numpy as np
from display import Display
from signal_listener import SignalListener
from signal_manager import SignalManager

draw_internal_position = False
mouse_speed = 1.2

class Mouse( SignalListener ):

    ignore_mouse_motion_positions = set()
    internal_position = None
    state = 0

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on event', 'on draw', 'on setup', 'on change open menu state' )


    def get_receive_signal_order( _type: str ) -> int:
        return 73


    @classmethod
    def on_signal( cls, _type: str, message = None ):

        if _type == 'on draw':
            if draw_internal_position:
                pygame.draw.circle( Display.screen, 'green', cls.internal_position, 10,1  )
        
        elif _type == 'on event':
            event = message
            if event.type == pygame.MOUSEMOTION:
                if event.pos in cls.ignore_mouse_motion_positions:
                    cls.ignore_mouse_motion_positions.add( event.pos )
                    return
                SignalManager.send_signal( 'on mouse motion', event.pos )

                if cls.state == 1:
                    return

                pygame.mouse.set_pos( Display.half_screen_size )
                cls.ignore_mouse_motion_positions.add( tuple(Display.half_screen_size) )
                cls.internal_position += [ round( c * mouse_speed ) for c in event.rel ]

        elif _type == 'on setup':
            cls.internal_position = np.array( Display.half_screen_size )
            pygame.mouse.set_visible( False )
        
        elif _type == 'on change open menu state':
            cls.state = 1 if message else 0
            pygame.mouse.set_visible( message )


    @classmethod
    def set_actual_position( cls, position ):
        cls.internal_position = np.array( position )


    def get_actual_position():
        return pygame.mouse.get_pos()


    @classmethod
    def get_internal_position( cls ):
        return cls.internal_position


    @classmethod
    def get_normalized_internal_position( cls ):
        p = cls.get_internal_position()
        return  ( np.array(p) / Display.full_screen_size ) * 2 - 1


