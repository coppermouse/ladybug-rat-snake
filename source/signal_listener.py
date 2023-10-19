# ----------------------------------------
# file: signal_listener.py
# class: SignalListener
# ----------------------------------------

class SignalListener:
    """
        Makes so a class can listen and react to signals. 
        NOTE: the class, not the instances of the class.
    """

    def get_listen_to_signal_types() -> list[str]:
        """
            Return what signal types this something listen to.
            
            This is so save resources so the on_signal method does not has to be called
            for every signal type for every listener.
        """
        raise NotImplementedError()


    def get_receive_signal_order( _type: str ) -> int:
        """
            Return a number to determine in what order this signal should be handle on this class
            next to other classes based on type.

            ex: ClassA: if _type='on start': return 1, if _type='on new player' return 1
                ClassB: if _type='on start': return 5, if _type='on new player' return 2
                ClassC: if _type='on start': return 4, if _type='on new player' return 3

                when 'on start', order is ClassA, ClassC, ClassB
                when 'on new player', order is ClassA, ClassB, ClassC

            Setting order is good. For example handle a class's on keydown before anything else
            is good because then it can take the input and break it before any class else can
            handle it.
        """
        raise NotImplementedError()


    def on_signal( _type: str, message = None ):
        """
            Implement the logic of what is going to happen for a certain signal. 
            _type is the signal type.

            The message can contain information relevant to the signal.
            ex: what button is being pressed on a on-button-down signal.

            Return string 'break' to make sure classes after does not handle the signal.
            Return ('break except', *args), it will work as  same as 'break' but with 
            exception on the classes defined in *args.
            
            if no desire to break the signal just return None.
        """
        raise NotImplementedError()


