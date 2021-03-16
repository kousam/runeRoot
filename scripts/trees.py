from lib.baseScript import *
from lib.tools import *
import lib.fuckOpenCV as focv


class Script(BaseScript):
    def __init__(self, files):
        super().__init__()

        self.files = files

        print('yoyoy')
        
        self.tree = focv.ContourMgr((80,30,0),15)
        self.tree.r_range = range(157,157)
        self.tree.g_range = range(137,137)
        self.tree.b_range = range(0,0)
        
##    def move(self):
##        window,game,eventMgr,gevent,wevent,mouse,keyboard, = self.tool_box
##        mouse.move((100,100),5)
##        event(self.move)

    def findTree(self):
        window,game,event,mouse,keyboard, = self.tool_box

        image = window.screenshot((8,31,512,334))
        rgb_data = getRgb(image)

        self.tree.locate(rgb_data, (512,334), (8,31))
        trees = self.tree.getCenter()

        if len(trees) > 0: 
            contour_distance_dict = {}
            for pos in trees:
                distance = calcDistance((262,192), pos)
                contour_distance_dict[distance] = pos
                
            distances = sorted(contour_distance_dict)
            value = contour_distance_dict[distances[0]]
        

        self.treePos = value


    def checkFullInvent(self):
        window,game,event,mouse,keyboard, = self.tool_box

        invent = game.inventory.get(True)
        if None not in invent:
            return True
        else:
            return False

    def flecth(self):
        window,game,event,mouse,keyboard, = self.tool_box
        
        region = game.inventory.getSlotRegion((0,0), True)
        mouse.move(region,1)
        mouse.click()
        sleep((0.5,1))
        region = game.inventory.getSlotRegion((1,0), True)
        mouse.move(region,1)
        mouse.click()

        sleep((1,2))
        mouse.move((224,422,80,61),1)
        mouse.click()

        sleep((47,52))

        for y in range(0,3):
            for x in range(0,6):
                if (x == 0 and y == 0):
                    pass

                else:
                    region = game.inventory.getSlotRegion((x,y), True)
                    mouse.move(region,1)
                    mouse.click('right')
                    
                    sleep((0.2,0.5))
                    
                    img1 = self.files.getImage('root', 'dropMaple')
                    img2 = window.screenshot((425,228,104,994))

                    region = findImage(img1,img2)
                    mouse.move(region,1)
                    mouse.click()

                    sleep(0.5,0.6)
        
        
    

    def _sleep(self):
        
        window,game,event,mouse,keyboard, = self.tool_box

        sleep(5)

        while True:
            sleep(2)

            image = window.screenshot((43,59,1,1))
            rgb_data = getRgb(image)

            if rgb_data[0] != (0,255,0):
                break;
            
            
            
            
    def clickTree(self):
        window,game,event,mouse,keyboard, = self.tool_box
        mouse.move(self.treePos,1)
        mouse.click()
        
            
    def run(self):
        window,game,event,mouse,keyboard, = self.tool_box

        self._stop = False
        self._pause = False
        while not self._stop:
            if not self._pause:

                if self.checkFullInvent():
                    event.game(self.flecth)

                else:
                    event.win(self.findTree)
                    event.game(self.clickTree)

                    self._sleep()
                             
                











