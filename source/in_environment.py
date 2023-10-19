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
            sie = sorted_in_environments = sorted( cls.in_environments, key = lambda ie: ie.draw_order )

            flatten_sorted_in_environment_scene_positions = [ 
                  sp for ie in sie for sp in ( ie.scene_positions 
                  if ie.many_scene_positions else [ie.scene_position] ) ]

            nsie = np.concatenate( flatten_sorted_in_environment_scene_positions )

            projected_vertices, mask, scale = projection_vertices(
                nsie.reshape( len(nsie) // 3, 3 ),
                Camera.get_scene_position(),
                Camera.get_rotation_matrix(),
                ( Display.half_screen_size * Camera.factors ),
                Display.half_screen_size,
                near,
            )

            i = 0
            for ie in sorted_in_environments:
                if not ie.many_scene_positions:
                    if mask[i]:
                        ie.environment_draw(
                            projected_vertices[i], min( scale[i], scale_in_environment_max ) )
                else:
                    ie.environment_draw( projected_vertices[ i : i + len(ie.scene_positions) ] )

                i += 1 if not ie.many_scene_positions else len(ie.scene_positions)


