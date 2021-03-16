




# ======== script stuff ==========#

class BaseScript():
    def __init__(self):
        self._stop = False
        self._pause = False


    def connect(self, client):
        self.client = client
        self.tool_box = client.getToolBox()
        
        (self.window,
        self.game,
        self.event,
        self.mouse,
        self.keyboard) = self.tool_box


    def pause(self):
        self._pause = True
        self.event.pause()

    def resume(self):
        self._pause = False
        self.event.resume()

    def stop(self):
        self._stop = True
        self.event.stop()
        del self
        
    def reset(self):
        self._stop = False
        self._pause = False






















