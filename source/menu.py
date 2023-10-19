# ----------------------------------------
# file: menu.py
# class: Menu
# ----------------------------------------

import pygame
import pygame_gui
from signal_listener import SignalListener
from signal_manager import SignalManager
from display import Display
from globals import g
from fps_counter import FpsCounter

menu_width = 720
menu_height = 400
menu_background_color = '#071116'
menu_blur_radius = 4

class Menu( SignalListener ):

    open = False
    background = None
    ui_elements = dict()

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on event', 'on draw', 'on frame', 'on setup' )


    def get_receive_signal_order( _type: str ) -> int:
        return -100


    @classmethod
    def on_signal( cls, _type: str, message = None ):

        if _type == 'on draw':
            if cls.open:
                Display.screen.blit( cls.background, (0,0) )
                cls.manager.draw_ui( Display.screen )
                return 'break except', FpsCounter

        elif _type == 'on event':
            event = message
            cls.manager.process_events(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                cls.open = not cls.open

                SignalManager.send_signal( 'on change open menu state', cls.open )

                if cls.open:
                    ss = Display.screen.get_size()
                    cls.background = pygame.Surface( ss )
                    pygame.draw.rect(
                        cls.background, menu_background_color, 
                        ( 0, 0, menu_width, ss[1] ))

                    blur = pygame.Surface( ( ss[0] - menu_width, ss[1] ) )
                    blur.blit( Display.screen, ( -menu_width, 0 ))

                    # NOTE: I think it could a bit faster using a subsurface of cls.background 
                    #       and dest to it
                    blur = pygame.transform.box_blur( blur, menu_blur_radius )
                    cls.background.blit( blur, ( menu_width, 0 )  )
                    # ---


            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                     if event.ui_element.is_selected:
                         event.ui_element.unselect()
                     else:
                         event.ui_element.select()

                     g['map on'] = event.ui_element.is_selected

        elif _type == 'on frame':
            delta_time = message
            cls.manager.update( delta_time )

            for key in ['camera-turn-speed', 'mouse-to-cursor-factor']:
                v = cls.ui_elements['uih-{0}'.format(key) ].get_current_value()
                cls.ui_elements['uil-{0}'.format(key) ].set_text( str(v ) )
                g[key] = v

            if cls.open:
                return 'break'

        elif _type == 'on setup':
            cls.manager = pygame_gui.UIManager(( menu_width, menu_height ))
 

            pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 205), (120, 50)),
                                             text='Map on/off',)

            for y, key, _range in [
                ( 310, 'camera-turn-speed', (0.0,0.4) ), ( 340, 'mouse-to-cursor-factor', (0,1) ) ]:

                cls.ui_elements[ 'uih-{0}'.format(key) ] = pygame_gui.elements.UIHorizontalSlider(
                    pygame.Rect( 10, y, 400, 26 ), g[key], _range )

                cls.ui_elements[ 'uil-{0}'.format(key) ] = pygame_gui.elements.UILabel(
                    pygame.Rect( 420, y, 40, 26 ), '.', )


