# ----------------------------------------
# file: fps_counter.py
# class: FpsCounter
# ----------------------------------------

from signal_listener import SignalListener
from globals import g
from draw_text import draw_text

class FpsCounter( SignalListener ):

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on draw', )


    def get_receive_signal_order( _type: str ) -> int:
        return 287


    @classmethod
    def on_signal( cls, _type: str, message = None ):
        if _type == 'on draw':
            clock = g['clock'] 
            draw_text( 'fps: {0}'.format( round( clock.get_fps(), 2 )))


