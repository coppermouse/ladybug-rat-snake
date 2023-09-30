# ----------------------------------------
# file: setup_signal_listeners.py
# method: setup_signal_listeners
# author: coppermouse
# ----------------------------------------

from path import list_dir
from path import load_txt
from file_to_class import file_to_class
from signal_manager import SignalManager

script_path = ':/source'

def setup_signal_listeners():
    """
        Adds every SignalListener to SignalManager.

        It also "setups" the SignalManager
    """
    
    SignalManager.setup()

    for file in list_dir( script_path ):
        if not file.endswith('.py'): continue
        if file == 'setup_signal_listeners.py': continue
        if file[:-3] == 'main': continue

       
        content = load_txt( script_path + '/' + file )
        if all([ needle in content for needle in
            [' SignalListener ):', 'author: coppermouse'  ] # really make sure we are not 
                                                            # importing unwanted scripts
        ]):
            m = __import__(file[:-3])
            SignalManager.add_listener( getattr( m, file_to_class(file[:-3]) ))

    SignalManager.validate()


