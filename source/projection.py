# ---------------------------------------- 
# file: projection.py
# methods: projection_vertices, projection_polygons
# ----------------------------------------

import numpy as np

def projection_vertices( vertices, offset, rotation_matrix, projection_factor, projection_offset, near ):
    v = ( vertices - offset ).dot( rotation_matrix )
    projected_vertices = np.flip( np.rot90(
        np.concatenate(( np.array( [ v[:,2] / v[:,1] ]), np.array([ v[:,0] / v[:,1] ]) )))) 

    look_vector = np.array([0,1,0]).dot( np.linalg.inv( rotation_matrix ) )
    mask = np.logical_and( 
        ( vertices - offset ).dot( look_vector ) > -near[1],
        ( vertices - offset ).dot( look_vector ) < -near[0],
    )

    scale = ( 1 / np.apply_along_axis( np.linalg.norm, 1, vertices - offset ) ) * 2500

    return projected_vertices *  projection_factor + projection_offset, mask, scale


def projection_polygons( polygons, colors, offset, rotation_matrix, 
                         projection_factor, projection_offset, edges, near, fog_color ):

    rm = rotation_matrix
    look_vector = np.array([0,1,0]).dot( np.linalg.inv(rm) )

    # --- filter on near and adjust roation and offset to be in line with the look
    near_and_adjusted_polygons, colors = _filter_polygons_based_on_near(
        polygons, offset, colors, look_vector, near )
    near_and_adjusted_points = near_and_adjusted_polygons.reshape( 
        len( near_and_adjusted_polygons )*4, 3 )
    
    near_and_adjusted_points -= offset
    near_and_adjusted_points[:] = near_and_adjusted_points[:].dot( rm )
    # ---

    # --- fog
    fog = np.array( fog_color )
    colors = _fogify( colors, fog, np.linalg.norm( -near_and_adjusted_polygons[:,0], axis = 1 ) )
    # ---

    # --- project 3d to 2d
    naps = near_and_adjusted_points
    projected_polygons = np.flip( np.rot90( np.concatenate((
        np.array([ naps[:,2] / naps[:,1] ]),
        np.array([ naps[:,0] / naps[:,1] ])
    )))).reshape( len( naps )//4, 4, 2 )
    # ---

    # --- back-face culling
    flat = projected_polygons.reshape( len( projected_polygons ), 8 )
    front_mask = (
        (( flat[:,2] - flat[:,0] ) * ( flat[:,3] + flat[:,1] )) +
        (( flat[:,4] - flat[:,2] ) * ( flat[:,5] + flat[:,3] )) +
        (( flat[:,6] - flat[:,4] ) * ( flat[:,7] + flat[:,5] )) +
        (( flat[:,0] - flat[:,6] ) * ( flat[:,1] + flat[:,7] ))
    ) > 0
    flat = flat[ front_mask ]
    front_faced_projected_polygons = flat.reshape( flat.shape[0], 4, 2 )
    colors = colors[ front_mask ]
    # ---

    # --- filter polygons out of view/edges
    front_faced_and_in_view_projected_polygons, colors = _filter_projected_polygons_out_of_view( 
            front_faced_projected_polygons, colors, edges )
    # ---

    # --- return ( and factor and offset )
    return ( 
        front_faced_and_in_view_projected_polygons * projection_factor + projection_offset,
        colors
    )
    # ---


def _filter_projected_polygons_out_of_view( projected_polygons, colors, edges ):
    pp = projected_polygons
    xe, ye = edges
    assert pp.shape[1] == 4 and pp.shape[2] == 2

    assert projected_polygons.shape[0] == colors.shape[0], (projected_polygons.shape[0], colors.shape[0])

    mask = np.logical_and(
        np.logical_and( pp[:,:,0]>=-xe, pp[:,:,0] <= xe),
        np.logical_and( pp[:,:,1]>=-ye, pp[:,:,1] <= ye),
    ).any( axis = 1 ) 
    
    return pp[ mask ], colors[ mask ]


def _filter_polygons_based_on_near( polygons, offset, colors, look_vector, near ):
    mask = np.logical_and( 
        ( polygons - offset )[:,0].dot( look_vector ) > -near[1],
        ( polygons - offset )[:,0].dot( look_vector ) < -near[0],
    )
    return polygons[ mask ], colors[ mask ]


def _fogify( colors, fog, factors ):
    assert colors.shape[0] == factors.shape[0]
    assert colors.shape[1] == 3
    assert len( colors.shape ) == 2
    assert fog.shape == (3,)
    assert len( factors.shape ) == 1
    return colors + ( fog - colors ) * np.clip( factors.reshape( factors.shape[0], 1 ) * 0.015, 0, 1 )


