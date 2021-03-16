

from .game import *
from .timer import *
from .tools import *
from .win32stuff import *





class Main():
    def __init__(self):
        self.windowEventQueue = []
        self.gameEventQueue = []
        self.connections = []

        self._stop = False

    def createConnections(self, title):
        for c in self.connections:
            c.kill()
        self.connections = []
        
        client_list = getClients(title)

        for c in client_list:
            self.addClient(c)

            
        
    def addClient(self, client):
        self.connections.append(client)
        
    def removeClient(self, client):
        self.connections.remove(client)
        
    def windowEventLoop(self):
        while not self._stop:
            while len(self.windowEventQueue)>0 and not self._stop:
                event = self.windowEventQueue[0]
                self.windowEventQueue.remove(event)
               
                if event.client.event._stop:
                    pass
                elif not event.client.event._pause:
                    event.priority()
                else:
                    self.windowEventQueue.append(event)
                
                sleep(0.1)

            sleep(0.1)
            
        quit()
            
    def gameEventLoop(self):
        while not self._stop:
            while len(self.gameEventQueue)>0 and not self._stop:
                event = self.gameEventQueue[0]
                self.gameEventQueue.remove(event)
                
                if event.client.event._stop:
                    pass
                elif not event.client.event._pause:
                    event.priority()
                else:
                    self.gameEventQueue.append(event)

                sleep(0.1)

            sleep(0.1)
            
        quit()
                
    def addGameEvent(self, event):
        self.gameEventQueue.append(event)
        
    def addWindowEvent(self, event):
        self.windowEventQueue.append(event)
        
    def stop(self):
        self._stop = True
        



def getClients(title):
    found_clients = clientSearch(title)
    client_list = [Client(title, hwnd) for hwnd, title in found_clients]

    return client_list  



        


# ==============client===========#


class Client():
    def __init__(self, title, hwnd):
        self.title = title
        self.hwnd = hwnd
        self.script = None
        self.build()

    def build(self):
        self.window = Window(self)
        self.game = GameMgr(self)
        self.event = EventMgr(self)
        self.mouse = MouseMgr(self.window)
        self.keyboard = KeyboardMgr(self)

    def getToolBox(self):
        return(self.window,
               self.game,
               self.event,
               self.mouse,
               self.keyboard)

    def getHandle(self):
        return self.hwnd


    def setScript(self, title):
        self.script = scriptMgr.initiateScript(title)
        self.script.connect(self)

    def runScript(self):
        tr = threading.Thread(target=self.script.run)
        
        tr.start()

    def kill(self):
        for i in self.getToolBox():
            del i
        
        del self
    
    def fuckWin32(self):
        # this activates the client window
        # pywintypes.error: (0, 'SetForegroundWindow', 'No error message is available')   ../.
        title_fg, hwnd_fg = getForegroudWindow()
        if hwnd_fg != self.hwnd:
            self.mouse.move((2,2,91,24), (4,5))
            self.mouse.click()


        

# =============Script Manager =============#


class ScriptManager():
    def __init__(self):
        self.scripts = []
    
    def load(self):
        files.loadScripts()
                
    def initiateScript(self, title):
        script_module = files.getScriptModule(title)
        s = script_module.Script(files)
        self.scripts.append(s)
        
        return s
        
    
    def getScriptLibrary(self):
        return self.script_lib

    def getScriptTitles(self):
        title_list = [title for title in files.getScriptModuleLibrary()]
        return title_list


        
           

#==============Events===========#


class Event():
    def __init__(self, client, action, arg=None, window_activation=True):
        self.client = client
        self.action = action
        self.arg = arg
        self.window_activation  = window_activation
        self._done = False
        self._priority = False

    def priority(self):
        self._priority = True
        while not self._done:
            sleep(0.01)
        
        sleep(0.01)
        self.kill()

    def wait(self):
        
        while not self._priority:
            sleep(0.1)
            
        if self.window_activation:
            self.client.fuckWin32()
        
        if self.arg == None:
            value = self.action()
        else:
            
            value = self.action(self.arg)
            
        
        self._priority = False
        self._done = True
        return value

    def kill(self):
        del self



class EventMgr():
    def __init__(self, client):
        self.main = main
        self.client = client
        self._pause = False
        self._stop = False
        
    def game(self, action, arg=None, window_activation=True):#, timer=None):
        e = Event(self.client, action, arg, window_activation)
        while not self._stop:
            if not self._pause:
                main.addGameEvent(e)
                break
            sleep(0.01)
        e.wait()
        
    def win(self, action, arg=None, window_activation=False):#, timer=None):
        e = Event(self.client, action, arg, window_activation)
        while not self._stop:
            if not self._pause:
                main.addWindowEvent(e)
                break
            sleep(0.01)
        return e.wait()
        

    def stop(self):
        self._stop = True
     
    def pause(self):
        self._pause = True

    def resume(self):
        self._pause = False
        
    def reset(self):
        self._stop = False
        self._pause = False
        
    




main = Main()
scriptMgr = ScriptManager()

def init():
    tr = threading.Thread(target=main.windowEventLoop)
    tr.start()
    main.gameEventLoop()



 

    

        
        
        
        
        
