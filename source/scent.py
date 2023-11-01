
from signal_listener import SignalListener
from walk_node import WalkNode

class Scent( SignalListener ):

    def get_listen_to_signal_types() -> list[str]:
        return ( 'on level load', )


    def get_receive_signal_order( _type: str ) -> int:
        return 114


    @classmethod
    def on_signal( cls, _type: str, message = None ):

        if _type == 'on level load':

            

            try:
                wn = WalkNode.walk_nodes[(12,12,6)]
            except KeyError:
                return

            edges = {wn}
            taken = {wn}
            for g in range(125):
                edges = j(edges,taken,g)

def j(edges, taken, g):

    r = set()
    for edge in edges:
        for adj in edge.adjs:
            if adj in taken: continue
            adj.color = g*12
            r.add(adj)
            taken.add(adj)
    return r
