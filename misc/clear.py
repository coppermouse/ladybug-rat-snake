# ----------------------------------------
# file: clear.py
# ----------------------------------------

import os
import sys
import pygame

source_dir = os.path.normpath( os.path.join( os.path.dirname( __file__ ), '..', 'source' ) )
sys.path.append( source_dir )

from path import load_image
from path import save_image
from path import list_dir

for file in list_dir(':/assets/imgs'):
    path = ':/assets/imgs/{0}'.format( file )
    s = load_image( path )
    c = pygame.Surface( s.get_size(), pygame.SRCALPHA )
    c.blit( s, (0,0) )
    save_image( path, c )


