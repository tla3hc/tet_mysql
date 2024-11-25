from views.main_window import MainWindow
# from models.modules.gui_interface.add_task import *
from abc import ABC, abstractmethod

# user request action directly from Controller.
# Controller request data from models.
# Models take action and send back data to Controller
# Controller send it to View.
# View show it to users.

class Controller(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def event_handler(self, event):
        pass
        
    pass
