# ----------------------------------------
# file: main.py
# author: coppermouse
# ----------------------------------------

import asyncio
import pygame
from display import Display
from setup_signal_listeners import setup_signal_listeners
from signal_manager import SignalManager

async def main():

    setup_signal_listeners()
    pygame.init()
    clock = pygame.time.Clock()
    pygame.font.init()
    font = pygame.font.SysFont( None, 30 )

    running = True

    SignalManager.send_signal( 'on setup' )
    while running:

        for event in pygame.event.get():
            SignalManager.send_signal( 'on event', event)
            if event.type == pygame.QUIT:
                running = False
        
        SignalManager.send_signal( 'on frame' )
        SignalManager.send_signal('on draw')

        Display.screen.blit( font.render('fps: {0}'.format( round( clock.get_fps(), 2) ), True, 'white' ), (20,620)  )

        pygame.display.flip()

        clock.tick(60)
        await asyncio.sleep(0)
        
    pygame.quit()

asyncio.run( main() )


