from .contours import *
from .tools import *
from .files import *




class Inventory():
    slots = []
    for y_axis in range(7):
        for x_axis in range(4):
            x = 42*x_axis
            y = 36*y_axis
            slots.append((x,y))

    region = (569, 242, 154, 244)   
    slot_size = (28, 28)
    
    
    def __init__(self, client):
        self.client = client
        self.update()

    def update(self):
        self.items = []
        for y in range(7):
            for x in range(4):
                slot = (x,y)
                item_name = self.getItemInSlot(slot)
                self.items.append(item_name)

    def getSlotRegion(self, slot, true_region=False):
        x,y = slot
        slot_index = x + 4*y
        x,y = self.slots[slot_index]
        
        if true_region:
            x_i, y_i, w_i, h_i  = self.region
            x += x_i
            y += y_i
            
        w,h = self.slot_size
        return x,y,w,h

    def getImage(self, slot=False):
        if slot:
            region = self.getSlotRegion(slot, True)
            rect = self.getSlotRegion(slot)  
        else:
            region = self.region
            rect = region
        
        image = self.client.window.screenshot(region)
        image = removeBackground(image, files.getImage('root','hud_inventbg'), rect)

        return image

    def isItemInSlot(self, item, slot):
        haystack_image = self.getImage(slot)
        needle_image = files.getImage('item', item)

        if getRgb(needle_image) == getRgb(haystack_image):
            value = True
        else:
            value = False
            
        return value

    def getItemInSlot(self, slot):
        needle_image = self.getImage(slot)
        parent_library = files.getParentLibrary('item')
        
        value = 'Unknown'
        
        for item_name in parent_library:
            if getRgb(needle_image) == getRgb(parent_library[item_name]):
                value = item_name
                break
            
        if value == 'None':
            value = None

        return value   

    def get(self, update=True):
        if update:
            self.update()
        
        return self.items


class Prayer():
    region = (558,244,176,213)
    
    slots = []
    for y_axis in range(6):
        for x_axis in range(5):
            x = 37*x_axis
            y = 37*y_axis
            slots.append((x,y))
            
  
class GameMgr():
    name = 'HUD manager'
    
    tabs = {'Combat Options': (534, 198),
            'Stats': (567, 198),
            'Quest List': (600, 198),
            'Inventory': (633, 198),
            'Worn Equipment': (666, 198),
            'Prayer': (699, 198),
            'Magic': (732, 198),
            'Clan Chat': (534, 496),
            'Friends List': (567, 496),
            'Ignore List': (600, 496),
            'Logout': (633, 496),
            'Options': (666, 496),
            'Emotes': (699, 496),
            'Music Player': (732, 496)}

    tab_size = (27,30)


    stats = {'Hitpoints': (528, 86),
             'Prayer': (528, 120),
             'Energy': (538, 152),
             'Special Attack': (560, 177),}
    
    stat_size = (16,8)
    total_xp_region = (425,46,87,8)
    character_center = (262, 192)


    def __init__(self, client):
        self.client = client

        #initiating tabs
        self.inventory = Inventory(client)
        self.prayer = Prayer()

        self.npc = ContourMgr((255,0,255))
        self.tile = ContourMgr((255,255,0),50)
        self.groundItem = ContourMgr((0,255,255),50)



    def getStat(self, stat):
        #black magic incoming
        #changeColor(img, target_color, to_color=(0,0,0), action='change')
     
        x,y = self.stats[stat]
        w,h = self.stat_size
        
        haystack_image = self.client.window.screenshot((x,y,w,h))
        value = matchNumbers(haystack_image, files)
   
        return value

        #dont worry about it. it works


    def getTotalXp(self):
        haystack_image = self.client.window.screenshot(self.total_xp_region)
        value = matchNumbers(haystack_image, files)

        return value

    def locateContour(self, contour, search_type):
        image = self.client.window.screenshot((8,31,512,334))
        rgb_data = getRgb(image)
        contour.locate(rgb_data, (512,334), (8,31))
        contour_list = contour.getCenter()
        if len(contour_list) > 0: 
            contour_distance_dict = {}
            for pos in contour_list:
                distance = calcDistance(self.character_center, pos)
                contour_distance_dict[distance] = pos
                
            distances = sorted(contour_distance_dict)
            if search_type == 'closest':
                value = contour_distance_dict[distances[0]]
                
            elif search_type == 'all':
                value = contour_list#[contour_distance_dict[i] for i in distances]

        else:
            value = None
        
        return value
    
    def locateNpc(self, search_type='closest'):
        value = self.locateContour(self.npc, search_type)
        
        return value


    def locateTile(self, search_type='closest'):
        value = self.locateContour(self.tile, search_type)
        
        return value

    def locateGroundItem(self, search_type='closest'):
        value = self.locateContour(self.groundItem, search_type)
        
        return value

    def pickGroundItem(self, search_type='closest'):
        if search_type == 'all':
            while self.locateGroundItem() != None:
                invent = self.inventory.get()
                item_pos = self.locateGroundItem()
                if item_pos != None:
                    self.client.mouse.move(item_pos,(3,4))
                    self.client.mouse.click('right')
                    sleep(0.2)
                    haystack_image = self.client.window.screenshot()
                    needle_image = files.getImage('root', 'take')
                    region = findImage(needle_image, haystack_image)
                    if region != None:
                        x,y = randomMousePos(region)
                        x += 30
                        self.client.mouse.move((x,y), (3,4))
                        self.client.mouse.click()

                    else:
                        break
                    
                    t = 0
                    while self.inventory.get() == invent:
                        t += 1
                        if t >= 25:
                            break
                        sleep(0.1)
    
                    
        elif search_type == 'closest':
            item_pos = self.locateGroundItem()
            if item_pos != None:
                invent = self.inventory.get()
                self.client.mouse.move(item_pos,(3,4))
                self.client.mouse.click('right')
                sleep(0.2)
                haystack_image = self.client.window.screenshot()
                needle_image = files.getImage('root', 'take')
                region = findImage(needle_image, haystack_image)
                if region != None:
                    x,y = randomMousePos(region)
                    x += 30
                    self.client.mouse.move((x,y), (3,4))
                    self.client.mouse.click()
                
                t = 0
                while self.inventory.get() == invent:
                    t += 1
                    if t >= 25:
                        break
                    sleep(0.1)
    


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        


