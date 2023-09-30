# ----------------------------------------
# file: path.py
# methods: project_path_to_path, is_file, load_json, load_image, load_sound, load_font
# author: coppermouse
# ----------------------------------------

import os
import json
import pygame

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


def load_json( project_path ):
    path = project_path_to_path( project_path )
    with open( path, 'r' ) as f:
        data = f.read()
    return json.loads( data )


def load_image( project_path ):
    path = project_path_to_path( project_path )
    return pygame.image.load( path )


def load_sound( project_path ):
    path = project_path_to_path( project_path )
    return pygame.mixer.Sound( path )


def list_dir( project_path ):
    path = project_path_to_path( project_path )
    for file in os.listdir( path ):
        yield file


def load_txt( project_path ):
    path = project_path_to_path( project_path )
    with open( path, 'r' ) as f:
        data = f.read()
    return data


def load_font( project_path, size ):
    path = project_path_to_path( project_path )
    return pygame.font.Font( path, size )


