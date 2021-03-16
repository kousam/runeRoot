from .tools import *


class Timer():
    def __init__(self, name, t, action, args=None, repeat=False):
        self.name = name
        self.sleep_time_init = t
        self.action = action
        self.args = args
        self.repeat = repeat

    
    def start(self):
        self.sleep_time = self.sleep_time_init
        self.kill = False
        
        tr = threading.Thread(target=self.sleep)
        tr.start()
        
        
    def stop(self):
        self.kill = True


    def doAction(self):
        self.action()

    def sleep(self):
        while self.sleep_time >= 0:
            self.sleep_time -= 0.1
            
            if self.kill:
                break
                
            sleep(0.1)

        if not self.kill:
            self.doAction()

    def getTime(self):
        return self.sleep_time
        
