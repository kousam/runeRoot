from tkinter import *
import tkinter.font as font
from tkinter import ttk

from .tools import *

app_name = 'RuneRoot_v2'



class ClientWidget(ttk.Frame):
    def __init__(self, gui, parent, client):
        ttk.Frame.__init__(self, parent)

        self.gui = gui
        self.parent = parent
        self.client = client
        
        self.running = False
        self.paused = False

        self.client_entry = Label(self)
        self.setClientTitle()
        self.client_entry['width'] = 21
        self.client_entry['height'] = 1
        self.client_entry['anchor'] = 'w'
        self.client_entry['borderwidth'] = 2
        self.client_entry['relief'] = 'groove'

        self.highlight_buttton = ttk.Button(self)
        self.highlight_buttton['text'] = 'Highlight'
        self.highlight_buttton['command'] = self.highlightWindow

        self.variable = StringVar(self)
        self.variable.set('Select Script')
        self.script_menu = ttk.Combobox(self, textvariable=self.variable)
        self.script_menu['width'] = 22

        self.start_stop_button = ttk.Button(self)
        self.start_stop_button['text'] = 'Start'
        self.start_stop_button['command'] = self.start
        
        self.pause_resume_button = ttk.Button(self)
        self.pause_resume_button['text'] = 'Pause'
        self.pause_resume_button['command'] = self.pause
        self.pause_resume_button['state'] = 'disabled'

        self.client_entry.grid({'row':0, 'column':0, 'sticky':'nsew'})
        self.highlight_buttton.grid({'row':0, 'column':1, 'padx':(5,0),'sticky':'nsew'})
        self.script_menu.grid({'row':0, 'column':2, 'padx':(5,0),'sticky':'nsew'})
        self.start_stop_button.grid({'row':0, 'column':3, 'padx':(5,0),'sticky':'nsew'})
        self.pause_resume_button.grid({'row':0, 'column':4, 'padx':(5,0),'sticky':'nsew'})

    def setClientTitle(self):
        if self.client.title[11:] == '':
            self.account_name = self.client.title
        else:
            self.account_name = self.client.title[11:]
            
        self.client_entry['text'] = self.account_name

    def getClient(self):
        title = self.client_entry.get()
        return title

    def setScripts(self, options):
        #self.variable.set('Sele')
        self.script_menu['values'] = options

    def highlightWindow(self):
        self.client.fuckWin32()

    def start(self):
        self.start_stop_button['text'] = 'Stop'
        self.start_stop_button['command'] = self.stop
        self.pause_resume_button['text'] = 'Pause'
        self.pause_resume_button['state'] = 'normal'
        self.pause_resume_button['command'] = self.pause

        self.gui.pause_resume_all_button['text'] = 'Pause All'
        self.gui.pause_resume_all_button['command'] = self.gui.pauseAll
        self.gui.pause_resume_all_button['state'] = 'normal'
        
        self.running = True
        
        
        self.script_title = self.script_menu.get()
        self.gui.terminal('[{}] Starting Script "{}" on Client "{}"'.format(timestamp(),self.script_title,self.account_name))
        self.client.event.reset()
        self.client.setScript(self.script_title)
        self.client.runScript()

    def stop(self):
        self.start_stop_button['text'] = 'Start'
        self.start_stop_button['command'] = self.start
        self.pause_resume_button['text'] = 'Pause'
        self.pause_resume_button['state'] = 'disabled'

        self.running = False
        self.gui.terminal('[{}] Stopping Script "{}" on Client "{}"'.format(timestamp(),self.script_title,self.account_name))
        self.client.script.stop()

    def pause(self):
        if self.running:
            self.pause_resume_button['text'] = 'Resume'
            self.pause_resume_button['command'] = self.resume
            self.paused = True

        self.client.script.pause()

    def resume(self):
        if self.running:
            self.pause_resume_button['text'] = 'Pause'
            self.pause_resume_button['command'] = self.pause
            self.paused = False

        self.client.script.resume()
        
        
class GUI():
    def __init__(self, main, scriptMgr):
        self.main = main
        self.scriptMgr = scriptMgr

        self.root = Tk()
        self.root.title(app_name)

        self.root.iconbitmap('tkicon.ico')
        
        self.w_init = 575
        self.h_init = 465
        self.w = self.w_init
        self.h = self.h_init
        self.x_init = 600
        self.y_init = 400
        self.rect = '{}x{}+{}+{}'.format(self.w, self.h, self.x_init, self.y_init)
        self.root.geometry(self.rect)
        self.root.resizable(width = False, height = False)
        
        self.script_list = []
        self.client_widgets = []
        self.createWidgets()

        self.terminal('Welcome to RuneRoot (v2.0 Last update 05.11.2018)')
        self.terminal('----------------------------------------------------------------------------------------------------')

        self.searchClients()
        self.searchScripts()
        
        
        
    def resize(self):
        elements = len(self.client_widgets)

        if elements > 8:
            n = elements - 8
            self.h = self.h_init + n*30
            self.rect = '{}x{}'.format(self.w, self.h)
            self.root.geometry(self.rect)

        else:
            self.w = self.w_init
            self.h = self.h_init
            self.rect = '{}x{}'.format(self.w, self.h)
            self.root.geometry(self.rect)


    def addClient(self, client):
        widget = ClientWidget(self, self.f3, client)
        widget.pack({'anchor': 'center', 'pady':(0,5)})
        self.client_widgets.append(widget)
        self.resize()

    def setScripts(self, scripts):
        for client in self.client_widgets:
            client.setScripts(scripts)


    def terminal(self, text):
        self.terminal_box['state'] = 'normal'
        self.terminal_box.insert(END, text + '\n')
        self.terminal_box['state'] = 'disabled'
        self.terminal_box.see("end")

    def startAll(self):
        self.start_stop_all_button['text'] = 'Stop All'
        self.start_stop_all_button['command'] = self.stopAll
        self.pause_resume_all_button['text'] = 'Pause All'
        self.pause_resume_all_button['state'] = 'normal'
        self.pause_resume_all_button['command'] = self.pauseAll

        for client in self.client_widgets:
            client.start()

    def stopAll(self):
        self.start_stop_all_button['text'] = 'Start All'
        self.start_stop_all_button['command'] = self.startAll
        self.pause_resume_all_button['text'] = 'Pause All'
        self.pause_resume_all_button['state'] = 'disabled'
        self.pause_resume_all_button['command'] = self.pauseAll

        for client in self.client_widgets:
            client.stop()

    def pauseAll(self):
        self.pause_resume_all_button['text'] = 'Resume All'
        self.pause_resume_all_button['command'] = self.resumeAll

        for client in self.client_widgets:
            client.pause()
                

    def resumeAll(self):
        self.pause_resume_all_button['text'] = 'Pause All'
        self.pause_resume_all_button['command'] = self.pauseAll

        for client in self.client_widgets:
            client.resume()

    def searchClients(self):
        for i in self.client_widgets:
            i.destroy()
        self.client_widgets = []
    
        self.main.createConnections('RuneLite')
        client_list = self.main.connections
        elements = len(client_list)

        self.terminal('[{}] Found {} Client(s)'.format(timestamp(), elements))
        for c in client_list:
            self.addClient(c)
            
        self.setScripts(self.script_list)
            

    def searchScripts(self):
        self.scriptMgr.load()
        self.script_list = self.scriptMgr.getScriptTitles()
        self.setScripts(self.script_list)

        elements = len(self.script_list)
        self.terminal('[{}] Found {} Script(s)'.format(timestamp(), elements))
        for i in range(elements):
            self.terminal('        {}. {}'.format(i+1, self.script_list[i]))

    def createWidgets(self):
        # this frame contains the terminal box
        self.f1 = ttk.Frame(self.root)
        self.f1.pack({'anchor': 'w', 'padx': 10, 'pady': 5})

        # this contains the utility buttons
        self.f2 = ttk.Frame(self.root)
        self.f2.pack({'anchor': 'e', 'padx': 10, 'pady': 5})

        #this contains the clients
        self.f3 = ttk.Frame(self.root)
        self.f3.pack({'anchor': 'w', 'padx': 10, 'pady': 5})


        # frame 1
        self.terminal_label = ttk.Label(self.f1)
        self.terminal_label['text'] = 'Terminal'

        self.queue_label = ttk.Label(self.f1)
        self.queue_label['text'] = 'Queue'
        
        self.terminal_scrollbar = ttk.Scrollbar(self.f1)

        self.terminal_box = Text(self.f1)
        self.terminal_box['state'] = 'disabled'
        self.terminal_box['width'] = 100
        self.terminal_box['height'] = 10
        self.terminal_box['font'] = font.Font(family='Consolas', size=8)

        self.terminal_box['yscrollcommand'] = self.terminal_scrollbar.set

        self.terminal_box.config(yscrollcommand=self.terminal_scrollbar.set)
        self.terminal_scrollbar.config(command=self.terminal_box.yview)

##        self.queue_box = Text(self.f1)
##        self.queue_box['state'] = 'disabled'
##        self.queue_box['width'] = 30
##        self.queue_box['height'] = 10
##        self.queue_box['font'] = font.Font(family='Consolas', size=10)


        # frame 2
        self.start_stop_all_button = ttk.Button(self.f2)
        self.start_stop_all_button['text'] = 'Start All'
        self.start_stop_all_button['command'] = self.startAll

        self.pause_resume_all_button = ttk.Button(self.f2)
        self.pause_resume_all_button['text'] = 'Pause All'
        self.pause_resume_all_button['command'] = self.pauseAll
        self.pause_resume_all_button['state'] = 'disabled'

        self.search_clients_button = ttk.Button(self.f2)
        self.search_clients_button['text'] = 'Search Clients'
        self.search_clients_button['command'] = self.searchClients

        self.search_scripts_button = ttk.Button(self.f2)
        self.search_scripts_button['text'] = 'Search Scripts'
        self.search_scripts_button['command'] = self.searchScripts
        

        # grid frame 1 widgets
        self.terminal_label.grid({'row':0, 'column':0, 'sticky': 'w'})
        self.terminal_box.grid({'row':1, 'column':0, 'sticky': 'nsew'})
        self.terminal_scrollbar.grid({'row': 1, 'column': 1, 'sticky': 'nsew'})

        # grid frame 2 widgets
        self.start_stop_all_button.grid({'row':0, 'column':2,'padx':(5,0),'sticky':'nsew'})
        self.pause_resume_all_button.grid({'row':0, 'column':3, 'padx':(5,0),'sticky':'nsew'})
        self.search_clients_button.grid({'row':0, 'column':0, 'padx':(5,0),'sticky':'nsew'})
        self.search_scripts_button.grid({'row':0, 'column':1, 'padx':(5,0),'sticky':'nsew'})


    



        



