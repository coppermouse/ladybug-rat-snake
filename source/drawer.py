import pygame
from display import Display
from signal_listener import SignalListener
from in_environment import InEnvironment
from house import House

class Drawer( SignalListener ):

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on draw', )


    def get_receive_signal_order( _type: str ) -> int:
        return 78


    @classmethod
    def on_signal( cls, _type: str, message = None ):

        pygame.draw.rect( Display.screen, '#111111', (0,0,120,30))
        pygame.draw.rect( Display.screen, '#434a55', (804,80-24,320,230+24))

        InEnvironment.draw( range(-1,0) )
        j = House.draw()
        for i in range(7):
            House.draw_floor(i)
            InEnvironment.draw( range(i,i+1) )
        House.draw_outer(j)
        InEnvironment.draw( range(10,11) )
