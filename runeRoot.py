from lib.core import *
import sys


'''
Last update = 2018.11.05
'''

def initgui():
    import lib.gui
    g = lib.gui.GUI(main, scriptMgr)
    g.root.mainloop()
    main.stop()
    
p = threading.Thread(target=initgui)
p.start()

init()





