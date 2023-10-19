# ---------------------------------------- 
# file: profiler.py
# class: Profiler
# ----------------------------------------

import pygame
from signal_listener import SignalListener
import io
from draw_text import draw_text

class Profiler( SignalListener ):

    profiler = None

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on event', 'on draw' )
    

    def get_receive_signal_order( _type: str ) -> int:
        return 200


    def on_signal( _type: str, message = None ):

        if _type == 'on event' and message.type == pygame.KEYDOWN and message.key == pygame.K_F9:
            # TODO: implement skip if activate if not working (use try catch)
            # TODO: implement deactivate if press again
            import cProfile
            Profiler.profiler = cProfile.Profile()
            Profiler.profiler.enable()

        elif _type == 'on draw':
            # TODO: implement not refresh every draw?
            profiler = Profiler.profiler
            if profiler is None: return
            from pstats import Stats
            sio = io.StringIO()
            stats = Stats( profiler, stream = sio )
            stats.sort_stats( 'tottime' ).print_stats(20)
            info_str = sio.getvalue()
            profiler.enable()
            
            for e, line in enumerate( info_str.split('\n') ):
                draw_text( line, ( 0, e*20 ), size = 14, color = 'white' )


