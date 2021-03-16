from lib.baseScript import *
from lib.tools import *


class Script(BaseScript):
    def __init__(self, files):
        super().__init__()

##    def move(self):
##        window,game,eventMgr,gevent,wevent,mouse,keyboard, = self.tool_box
##        mouse.move((100,100),5)
##        event(self.move)
            
    def run(self):
        window,game,event,mouse,keyboard, = self.tool_box
        self.reset()
        event.reset()
        while not self._stop:
            if not self._pause:


                event.win(print,'kakka')               

                

