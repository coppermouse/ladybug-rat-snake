# ----------------------------------------
# file: main.py
# ----------------------------------------

import asyncio
import pygame
import numpy
from setup_signal_listeners import setup_signal_listeners
from signal_manager import SignalManager
from globals import g
from config import fps

async def main():

    pygame.init()
    setup_signal_listeners()
    clock = pygame.time.Clock()
    g['clock'] = clock

    running = True

    SignalManager.send_signal( 'on setup' )
    screen = pygame.display.get_surface()

    while running:
        time_delta = clock.tick( fps )

        for event in pygame.event.get():
            SignalManager.send_signal( 'on event', event)
            if event.type == pygame.QUIT:
                running = False

        SignalManager.send_signal( 'on frame', time_delta )
        SignalManager.send_signal( 'on draw' )
        
        pygame.display.update()
        await asyncio.sleep(0)
        
    pygame.quit()


if __name__ == '__main__':
    asyncio.run( main() )


