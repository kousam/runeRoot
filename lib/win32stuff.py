import win32gui
import win32ui
import win32api
import win32con
import win32com.client as comclt
from .vector import *
from .tools import *


class Window:
    def __init__(self, client):
        self.client = client
        self.hwnd = self.client.getHandle()

    def setHandleFromTitle(self, title):
        self.hwnd = win32gui.FindWindow(None, title)
        
        
    def getHandle(self):
        return self.hwnd

    def getRect(self):
        # this return window x,y,w,h
        rect = win32gui.GetWindowRect(self.hwnd)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y
        
        return (x,y,w,h)

    def activate(self):
        title, hwnd = getForegroudWindow()
        if hwnd != self.hwnd:
            success = False
            while not success:
                try:
                    win32gui.SetForegroundWindow(self.hwnd)
                    success = True
                except Exception as e:
                    pass
                    
                sleep(0.1)

                
        
    def screenshot(self, region=False, return_bm=False):

        if region == False:
            region_x, region_y, region_w, region_h = self.getRect()
            region_x = 0
            region_y = 0
        
        else:
            region_x, region_y, region_w, region_h = region
            
        x = region_x
        y = region_y
        x2 = region_x + region_w
        y2 = region_y + region_h

        success = False
        while not success:
            try:
                # following is copypasta code. read at own risk
                # this creates a bitmap of a region in window
                wDC = win32gui.GetWindowDC(self.hwnd)
                dcObj = win32ui.CreateDCFromHandle(wDC)
                cDC = dcObj.CreateCompatibleDC()
                dataBitMap = win32ui.CreateBitmap()
                dataBitMap.CreateCompatibleBitmap(dcObj, region_w, region_h)
                cDC.SelectObject(dataBitMap)
                cDC.BitBlt((-x,-y),(x2, y2) , dcObj, (0,0), win32con.SRCCOPY)

                bitmap = dataBitMap.GetBitmapBits()

                dcObj.DeleteDC()
                cDC.DeleteDC()
                win32gui.ReleaseDC(self.hwnd, wDC)
                win32gui.DeleteObject(dataBitMap.GetHandle())
                
                success = True
                
            except:
                pass

        if return_bm:
            return bitmap
            
        else:
            img = imageFromBgrx(bitmap, (region_w, region_h))
            
            return img 
             
            
            
 
def getForegroudWindow():
    #returns the name of the foreground window
    hwnd = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(hwnd)
    return (title, hwnd)
 
        
        
def clientSearch(title):
    found_clients = []
    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            text = win32gui.GetWindowText(hwnd)
            if title in text:
                found_clients.append((hwnd,text))
            
    win32gui.EnumWindows(callback, None)

    return found_clients  





class KeyboardMgr:
    wsh = comclt.Dispatch("WScript.Shell")

    keys = {'shift': win32con.VK_SHIFT,
            'ctrl': win32con.VK_CONTROL}
    
    def __init__(self, client):
        self.client = client

    def sendKey(self, key):
        self.wsh.SendKeys(key)

    def sendString(self, s):
        pass

    def keystate(self, key):
        if key in self.keys:
            key = self.keys[keys]
        else:
            key = ord(key)
            
        if win32api.GetKeyState(key) < 0:
            value = True
        else:
            value = False
        return value
    
    def detect(self):
        if self.keystate('shift') and self.keystate('1'):
            pass
    






class MouseMgr():

    def __init__(self, window):
        self.real_vector = Vector()
        self.path_vector = Vector()
        self.force_vector = Vector()
        
        self.x = None
        self.y = None
        self.x_prev = None
        self.y_prev = None

        self.window = window

    def vectorUpdate(self, end_pos, start_pos):
        #path vector
        # path vector always points towards the end_pos
        p_distance = calcDistance(end_pos, start_pos)
        p_delta_x, p_delta_y = calcDelta(end_pos, start_pos)

        # the speed is the squareroot of the whole distance from start_pos to end_pos
        # to create easy code for acceleration
        p_speed = p_distance**0.5
        if p_speed < 1:
            p_speed = 1

        # creates a unit vector for the whole distance and multiplies it with the speed
        p_i = round(p_delta_x/p_distance*p_speed)
        p_j = round(p_delta_y/p_distance*p_speed)
        
        self.path_vector.set(p_i, p_j)


        #force vector
        #this makes inconsistent movement of mouse
        f_speed = int(abs(p_speed/8))
        f_i = -f_speed
        f_j = -f_speed




        
        if randomizer((0,3)) == 0:
            f_i *= -2
        else:
            f_i = 0
            
        if randomizer((0,3)) == 0:
            f_j *= -1

            
        self.force_vector.set(f_i,f_j)


        # real vector is the vector that moves the mouse
        # path_vector + force_vector
        r_i = int(round(p_i + f_i))
        r_j = int(round(p_j + f_j))
        
    ##    r_i,r_j = addVectors(p,f)
        self.real_vector.set(r_i,r_j)
        


    def getPos(self):
        flags, hcursor, (x,y) = win32gui.GetCursorInfo()
        return (x,y)


    def getInRegion(self, reg):
        self.update()
        
        value = False
        x,y,w,h = reg
        
        if x <= self.x <= x + w and y <= self.y <= y + h:
            value = True

        return value
    

    
    def click(self, key='left'):
        # pass string 'left', 'right' or 'middle'
        # if no argument in mouse.click(), defaults to leftclick
        
        x,y = self.getPos()
        
        if key == 'left':
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y)
                
        elif key == 'middle':
            win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN,x,y)
            win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP,x,y)
                
        elif key == 'right':
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y)


    def hold(self, state, key='left'):
        x,y = self.getPos()
        
        if state == True:
            if key == 'left':
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y)
                    
            elif key == 'middle':
                win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN,x,y)
                    
            elif key == 'right':
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y)

        if state == False:
            if key == 'left':
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y)
                    
            elif key == 'middle':
                win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP,x,y)
                    
            elif key == 'right':
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y) 

                                     
    def move(self, region, speed, relative=False, sleep=True):
        # human like movement
        if not isinstance(speed, int):
            speed_min, speed_max = speed
            speed = randomizer(speed,False)
        move_sleep = 0.01/speed

        region_elements = len(region)
        if region_elements == 2:
            end_x, end_y = region
        else:
            end_x, end_y = randomMousePos(region)

        if not relative:
            win_x, win_y, win_w, win_h = self.window.getRect()
            end_x += win_x
            end_y += win_y

        if relative:
            end_x,end_y = calcRelativePos((end_x,end_y),self.getPos())
               

        while self.getPos() != (end_x,end_y):
            self.vectorUpdate((end_x,end_y), self.getPos())
            i,j = self.real_vector.get()
        
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, i, j)

            time.sleep(move_sleep)
            
        if sleep:     
            t = randomizer((0.15, 0.25), False)
            time.sleep(t)        
        


    def ellipseTurn(self,d=(40,80)):
        #experimental stuff
        start_x, start_y = self.getPos()
        
        w = randomizer(60,100)
        h = randomizer(30,50)

        start = math.pi/4
        alpha = 0
 
        for i in range(randomizer(d)):
            x = round(w/2*math.cos(alpha + start))
            y = round(h/2*math.sin(alpha + start))
            
            mouse_event(win32con.MOUSEEVENTF_MOVE, x, y)
            
            alpha += math.pi/10#*direction

            time.sleep(0.01)





    




    
