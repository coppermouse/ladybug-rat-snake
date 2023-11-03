# ----------------------------------------
# file: in_environment.py
# class: InEnvironment
# ----------------------------------------

import numpy as np
from signal_listener import SignalListener
from display import Display
from projection import projection_vertices
from config import near
from config import scale_in_environment_max
from camera import Camera

class InEnvironment( SignalListener ):

    many_scene_positions = False
    in_environments = set()
    draw_order = 0

    def __init__( self, scene_position_or_scene_positions ):
        
        sposp = scene_position_or_scene_positions
        if not self.many_scene_positions:
            scene_position = np.array( sposp ) 
            self.scene_position = scene_position
        else:
            scene_positions = np.array( sposp ) 
            self.scene_positions = scene_positions
 
        InEnvironment.in_environments.add( self )


    def get_listen_to_signal_types() -> list[str]:
        return ( 'on draw', )


    def get_receive_signal_order( _type: str ) -> int:
        return 182


    @classmethod
    def on_signal( cls, _type: str, message = None ):
        if _type == 'on draw':
            #cls.draw()
            pass

    @classmethod
    def draw(cls, draw_order_filter = range(-15,16)):
            sie = sorted_in_environments = [ c for c in cls.in_environments if c.draw_order in draw_order_filter]

            flatten_sorted_in_environment_scene_positions = [ 
                  sp for ie in sie for sp in ( ie.scene_positions 
                  if ie.many_scene_positions else [ie.scene_position] ) ]

            if not flatten_sorted_in_environment_scene_positions:
                return

            nsie = np.concatenate( flatten_sorted_in_environment_scene_positions )

            projected_vertices, mask, scale, colors = projection_vertices(
                nsie.reshape( len(nsie) // 3, 3 ),
                Camera.get_scene_position(),
                Camera.get_rotation_matrix(),
                ( Display.half_screen_size * Camera.factors ),
                Display.half_screen_size,
                near,
                fog_offset = (0,-34,0)
            )

            i = 0
            draws = list()
            for ie in sorted_in_environments:
                if mask[i]:
                        draws.append((ie,
                            projected_vertices[i], min( scale[i], scale_in_environment_max ) , colors[i], scale[i]  ))
                else:
                        assert 0

                i += 1

            for d in sorted(draws, key=lambda a:a[-1]):
                ie = d[0]
                d = d[1:4]
                ie.environment_draw( *d )


