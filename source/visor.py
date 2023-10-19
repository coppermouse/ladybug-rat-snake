# ----------------------------------------
# file: visor.py
# class: Visor
# ----------------------------------------

from signal_listener import SignalListener
from path import is_file
from path import save_pickle
from path import load_pickle
from config import visor_factor
from _resource import Resource
import numpy as np

class Visor( SignalListener ):

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on setup', )


    def get_receive_signal_order( _type: str ) -> int:
        return 71


    @classmethod
    def on_signal( cls, _type: str, message = None ):

        if _type == 'on setup':
            cache_points_file = ':/visor.pickle.gz'

            # NOTE: a lot of hardcoded values here. that will work for now till I 
            #       have a better understanding of the future of the project and its solutions

            if not is_file( cache_points_file ): 
                world = Resource.imgs[3]
                f = visor_factor
                visor = np.zeros((32*f,32*f,32*4), dtype = np.bool_)
                for x in range(32):
                    for y in range(32):
                        for z in range(32):
                            if not ( 255-world.get_at((x,y)).a < z):
                                for dx in range(f):
                                    for dy in range(f):
                                        visor[(x*f+dx,y*f+dy,z)] = True

                # points can be used for debug to see visor data in environment
                points = list()
                for x in range(32*f):
                    for y in range(32*f):
                        for z in range(32):
                            if visor[(x,y,z)]:
                                points.append( (x,y,z) )
        
                cls.points = np.array( points, dtype = np.float64 )
                cls.points *= ( 1/f, 1/f, 1/8 )
                cls.visor = visor
                save_pickle( cache_points_file, ( cls.visor, cls.points ) )       

            else:
                cls.visor, cls.points = load_pickle( cache_points_file )


