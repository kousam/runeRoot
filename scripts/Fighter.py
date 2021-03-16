from lib.baseScript import *
from lib.tools import *




class Script(BaseScript):
    def __init__(self, files):
        super().__init__()
        self.files = files

    def checkFullInvent(self):
        window,game,event,mouse,keyboard, = self.tool_box

        invent = game.inventory.get(True)
        if None not in invent:
            self.tp()
        

    def bury(self):
        window,game,event,mouse,keyboard, = self.tool_box

        invent = game.inventory.get(True)
        found = False
        for i, item in enumerate(invent):
            if item == 'Big bones':
                slot = getPosFromIndex(i,4,7)
                region = game.inventory.getSlotRegion(slot, True)
                mouse.move(region,(4,5))
                mouse.click()
                sleep((1,1.2))

        
    def eat(self):
        window,game,event,mouse,keyboard, = self.tool_box
    
        invent = game.inventory.get(True)
        found = False
        for i, item in enumerate(invent):
            if item == 'Monkfish':
                slot = getPosFromIndex(i,4,7)
                region = game.inventory.getSlotRegion(slot, True)
                found = True
                break
        if found:
            mouse.move(region,(1,2))
            mouse.click()
        else:
            self.stop()
            #self.tp()

    def findMob(self):
        window,game,event,mouse,keyboard, = self.tool_box
       
        pos = game.locateNpc('all')
        if pos != None and pos != []:
            mob_pos = pos[0]
            mouse.move(mob_pos,(4,5),False,True)

    def getMobDead(self):
        window,game,event,mouse,keyboard, = self.tool_box
        r_range = range(90,110)
        g_range = range(10,30)
        b_range = range(10,30)
        img = event.win(window.screenshot,(15,71,1,1))
        r,g,b = getRgb(img)[0]
        if r in r_range and g in g_range and b in b_range:
            value = True
        else:
            value = False

        return value

    def getFighting(self):
        window,game,event,mouse,keyboard, = self.tool_box
        r_range = range(0,20)
        g_range = range(120,145)
        b_range = range(40,60)
        img = window.screenshot((15,71,1,1))
        r,g,b = getRgb(img)[0]
        if r in r_range and g in g_range and b in b_range:
            value = True
        else:
            value = False

        return value

    def attack(self):
        window,game,event,mouse,keyboard, = self.tool_box
        found = False
        while not found:
            
            x,y = mouse.getPos()
            x_w, y_w, w_w, h_w = window.getRect()   
            x2 = x - x_w
            y2 = y+24 - y_w
            img1 = self.files.getImage('root', 'attack')
            img2 = window.screenshot((x2,y2,50,18))
            img2 = changeColor(img2, (255,255,255), (0,0,0), action='keep')

            if findImage(img1, img2, 'bool'):
                found = True
                break
            self.findMob()
            
            
            
            
            
        mouse.click()
        
        
    def resetSleep(self):
        window,game,event,mouse,keyboard, = self.tool_box
        while not self.stopResetSleep:
            self.previous_xp = game.getTotalXp()
            sleep(10)
            if self.previous_xp == game.getTotalXp():
                self.stopSleep = True

    def _sleep(self):
        sleep((2,3))

        
        while True:
            if self.getMobDead():
                self.stopResetSleep = True
                break
            
            if not self.getFighting():
                break
                   
        sleep((4,5))

            

    def tp(self):
        window,game,event,mouse,keyboard, = self.tool_box
        region = game.inventory.getSlotRegion((0,0), True)
        mouse.move(region,(4,5))
        mouse.click()
        self.stop()
            
        
    def run(self):
        window,game,event,mouse,keyboard, = self.tool_box

##        self.timer = Timer('stop_script', 14400, self.stop)
##        self.timer.start()
        self._stop = False
        self._pause = False
        while not self._stop:
            if not self._pause:
                
                
                hp = event.win(game.getStat,'Hitpoints',False)
                if hp < 50:
                    event.game(self.eat)

                

                if game.locateGroundItem('all') != None:
                    event.win(self.checkFullInvent)
                    event.game(game.pickGroundItem, 'all')
                    sleep(0.2)
                    
                if 'Big bones' in game.inventory.get(True):
                    event.game(self.bury)
                    
                if game.locateNpc('all') != None:
                    
                    event.game(self.attack)
                    self._sleep()
                















