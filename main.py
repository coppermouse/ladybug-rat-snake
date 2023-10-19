"""
    This is (of one of the) Python script to be called to start the game.
    Even though it is a script file and should belong in the source folder it is 
    placed in top folder for more easy access. 
"""

import os
import sys
import asyncio

source_dir = os.path.normpath( os.path.join( os.path.dirname( __file__ ), 'source' ) )
sys.path.append( source_dir )

from source.main import main

asyncio.run( main() )
