
from signal_listener import SignalListener
from in_environment import InEnvironment
from house import House

class Drawer( SignalListener ):

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on draw', )


    def get_receive_signal_order( _type: str ) -> int:
        return 78


    @classmethod
    def on_signal( cls, _type: str, message = None ):

        InEnvironment.draw( range(-1,0) )
        House.draw()
        for i in range(7):
            House.draw_floor(i)
            InEnvironment.draw( range(i,i+1) )
