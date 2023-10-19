# ----------------------------------------
# file: path.py
# methods: project_path_to_path, is_file, list_dir, load_json, load_image, 
#          save_image, load_sound, load_txt, load_font, load_pickle, save_pickle
# ----------------------------------------

import os
import json
import pygame
import pickle

# ---
# we are compressing some data  
# see: https://stackoverflow.com/questions/57983431/whats-the-most-space-efficient-way-to-compress-serialized-python-data
import bz2
import gzip
# import lzma # <- does not seem to work in pygbag
# ---

def project_path_to_path( project_path : str ):
    if not type( project_path ) == str: raise TypeError()
    if not project_path.startswith( ':/' ): raise ValueError()

    r = os.path.normpath(
        os.path.join(
            os.path.dirname(
                __file__
            ),
            '..', *project_path[2:].split('/')
        )
    )
    return r


def is_file( project_path ):
    return os.path.isfile( project_path_to_path( project_path ))


def list_dir( project_path ):
    path = project_path_to_path( project_path )
    for file in os.listdir( path ):
        yield file


def load_json( project_path ):
    path = project_path_to_path( project_path )
    with open( path, 'r' ) as f:
        data = f.read()
    return json.loads( data )


def load_image( project_path ):
    path = project_path_to_path( project_path )
    return pygame.image.load( path )


def save_image( project_path, surface ):
    path = project_path_to_path( project_path )

    assert path.endswith( '.png' ), path
    assert path.endswith( project_path.split('/')[-1] ), path

    pygame.image.save( surface, path )


def load_sound( project_path ):
    path = project_path_to_path( project_path )
    return pygame.mixer.Sound( path )


def load_txt( project_path ):
    path = project_path_to_path( project_path )
    with open( path, 'r' ) as f:
        data = f.read()
    return data


def load_font( project_path, size ):
    path = project_path_to_path( project_path )
    return pygame.font.Font( path, size )


def load_pickle( project_path ):
    # TODO: only do gzip if gz-extension in filename
    path = project_path_to_path( project_path )

    with gzip.open( path, 'rb' ) as f:
        r = pickle.load( f )
    
    return r


def save_pickle( project_path, data ):
    # TODO: only do gzip if gz-extension in filename
    path = project_path_to_path( project_path )

    assert path.endswith( '.gz' ), path
    assert path.endswith( project_path.split('/')[-1] ), path

    with gzip.open( path, 'wb' ) as f:
        pickle.dump( data, f )


