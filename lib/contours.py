


class Family:
    def __init__(self, manager):
        self.pixel_list = []
        self.manager = manager
        self.center = None

    def add(self, pos):
        if pos in self.manager.pixel_list:
            self.manager.pixel_list.remove(pos)
        if pos not in self.pixel_list:
            self.pixel_list.append(pos)
            self.find(pos)  

    def find(self, pos):
        neighbors = self.manager.neighbor_dict[pos]
        for p in neighbors:
            x,y = p
            self.add(p)
        self.setCenter()

    def setCenter(self):
        n = len(self.pixel_list)
        x_sum = 0
        y_sum = 0
        for pos in self.pixel_list:
            x,y = pos
            x_sum += x
            y_sum += y

        x = int(round(x_sum/n))
        y = int(round(y_sum/n))
        self.center = (x,y)

    def kill(self):
        del self

    

def getIndex(data, color_range):
    r_range, g_range, b_range = color_range
    index_list = []
    for i, (r,g,b) in enumerate(data):
        if r in r_range and g in g_range and b in b_range:
            index_list.append(i)
            
    return index_list

def getPosFromIndex(i, w, h, start_x=0, start_y=0):
    y = int(i/(w))
    x = i - (y*(w))

    x += start_x
    y += start_y

    return(x,y)

def checkNeighbors(pos, pixel_list):
    x_start ,y_start = pos
    size = 2 # this should be 2 for contours
    x_range = range(x_start - size, x_start + size)
    y_range = range(y_start - size, y_start + size)
    neighbors = []
    for x in x_range:
        for y in y_range:
            if (x,y) in pixel_list:
                neighbors.append((x,y))
                
    return neighbors
    

class ContourMgr():
    def __init__(self, color, offset=10):
        self.pixel_list = []
        self.families = []
        self.neighbor_dict = {}
        self.setColor(color, offset)

    def setColor(self, color, offset=10):
        r,g,b = color
        r_range = range(r - offset, r + offset + 1)
        g_range = range(g - offset, g + offset + 1)
        b_range = range(b - offset, b + offset + 1)
        self.color_range = (r_range, g_range, b_range)

    def deleteFamilies(self):
        for f in self.families:
            f.kill()
        self.families = []

    def locate(self, rgb_data, size, start_pos=(0,0)):
        self.deleteFamilies()
        x,y = start_pos
        w,h = size
        index_list = getIndex(rgb_data, self.color_range)
        self.pixel_list = [getPosFromIndex(i,w,h,x,y) for i in index_list]

        self.neighbor_dict = {}
        for i in self.pixel_list:
            neighbors = checkNeighbors(i, self.pixel_list)
            self.neighbor_dict[i] = neighbors
            
        families = []
        while len(self.pixel_list) > 0:
            f = Family(self)
            f.add(self.pixel_list[0])
            self.families.append(f)

    def getCenter(self):
        center_list = [f.center for f in self.families]
        return center_list




