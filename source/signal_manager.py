# ----------------------------------------
# file: signal_manager.py
# class: SignalManager
# ----------------------------------------

from signal_types import signal_types

class SignalManager:
    """
        Makes it easy for classes to listen and react to each other.

        When a signal is being sent (through this class) all classes
        that have signed up to listen to that type of signal will receive it.

        All classes that should receive signals must implement SignalListener
        and its methods.
    """

    # TODO: there is a lot of data handling being done "at the fly" on these methods.
    #       I think to should be more cost effective and also a bit less complex if these
    #       were done in a dedicated method after all signal listeners been setup.

    been_setup = False
    listeners = set()
    listeners_on_signal_types = dict() # this is being populated in setup
    cached_sorted_listeners = dict()

    def setup():
        if SignalManager.been_setup is True: return
        SignalManager.been_setup = True
        
        SignalManager.listeners_on_signal_types = { 
            st: set() for st in signal_types 
        } 


    @classmethod
    def validate( cls ):
        for signal_type in sorted( signal_types ):
            orders = [ l.get_receive_signal_order( signal_type ) for l in cls.listeners if signal_type in l.get_listen_to_signal_types() ]
            assert { type(order) for order in orders } == { int }, orders
            assert len( orders ) == len(list(set( orders )))


    def listener_sorter( listener, signal_type ):
        return listener.get_receive_signal_order( signal_type )
 

    def add_listener( listener ):
        from signal_listener import SignalListener
        if SignalListener not in listener.mro(): 
            raise ValueError( 'listener is not an SignalListener: {0}'.format( listener ) )
        
        SignalManager.cached_sorted_listeners.clear()
        SignalManager.listeners.add( listener )
       
        if type( listener ) != type: raise ValueError()
 
        try:
            for signal_type in (
                listener.get_listen_to_signal_types() 
            ):
                SignalManager.listeners_on_signal_types[ signal_type ].add( listener )
        except NotImplementedError as e:
            # print( listener ) <-- uncomment to investigate what listener it raised on
            raise e


    def send_signal( _type, message = None ):

        signal_type = _type
        
        if _type not in signal_types:
            raise ValueError( 'signal type does not exist: {0}'.format( signal_type ) )
        
        listeners = SignalManager.listeners_on_signal_types.get(
            signal_type, SignalManager.listeners 
        )

        sorted_listeners = SignalManager.cached_sorted_listeners.get( 
            id( listeners ), 
            sorted( listeners, key= lambda sl: SignalManager.listener_sorter( sl, signal_type ) ) 
        )
        SignalManager.cached_sorted_listeners[ id( listeners ) ] = sorted_listeners
        
        break_except = None
        for listener in sorted_listeners:
            if break_except: 
                if listener not in break_except: continue

            response = listener.on_signal( _type, message )
            if response == 'break': 
                break

            if type(response) == tuple and response[0] == 'break except':
                _, *break_except = response


