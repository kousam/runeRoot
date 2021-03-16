from PIL import Image
import time
import datetime
import random
import pyautogui
import math
import numpy
import threading


def calcDelta(end_pos, start_pos):
    # this calculates the lenght of vector projected to x and y axis
    
    x0,y0 = start_pos
    x,y = end_pos
    delta_x = x - x0
    delta_y = y - y0
    
    return (delta_x, delta_y)


def calcDistance(end_pos, start_pos):
    # this calculates the distance between two points
    delta_x, delta_y = calcDelta(end_pos, start_pos)
    distance = (delta_x**2 + delta_y**2)**0.5
    return distance


def calcRelativePos(end_pos, start_pos):
    x1,y1 = end_pos
    x0,y0 = start_pos

    x = x1 + x0
    y = y1 + y0

    return (x,y)
    

def getPosFromIndex(i, w, h, start_x=0, start_y=0):
    y = int(i/(w))
    x = i - (y*(w))

    x += start_x
    y += start_y

    return(x,y)


def matchNumbers(haystack_image, files):
    haystack_image =  changeColor(haystack_image, (0,0,0), (255,255,255), 'keep')
    temp_dict = {}
    for i in range(10):
        name = 'hud_{}'.format(i)
        match = list(pyautogui.locateAll(files.getImage('root', name), haystack_image))
        for rect in match:
            (x,y,w,h) = rect
            temp_dict[x] = i
                
    value = int(listToString(letterSorter(temp_dict)))

    return value


def letterSorter(d):
    #this takes a dict of  x-cordinate : letter/number and returns a list of items sorted by lowes x value
    temp_list = [d[i] for i in sorted(d)]
    
    return temp_list
        

def listToString(l):
    temp_string = ''
    for i in l:
        temp_string = '{}{}'.format(temp_string, i)

    return temp_string


def timestamp(time_format='%H:%M', sec_add=0):
    # sec_add is the added seconds to the timestamp
    unix_time = time.time()
    unix_time += sec_add 
    ts = datetime.datetime.fromtimestamp(unix_time).strftime(time_format)
    return ts
    
    
def randomizer(values, integer=True):
    # this returns a random number between a and b
    # if integer = False, the function will return a number with 3 decimals
    a,b = values
    i = round(random.uniform(a,b), 4)
    
    if integer:
        i = int(round(i))

    return i

def randomPosInRegion(region):
    x,y,w,h = region
    w = randomizer(0,w)
    h = randomizer(0,h)
    x += w
    y += h

    return(x,y)

def randomMousePos(region):
    x,y,w,h = region
    l = random.random()**2
    c = random.random()
    a = 2*math.pi
    x += round(l*(w/2)*math.cos(a*c) + w/2)
    y += round(l*(h/2)*math.sin(a*c) + h/2)

    return(x,y)


def randomPos(client):
    x,y,w,h = client.window.getRect()

    rand_x = randomizer(0,w)
    rand_y = randomizer(0,h)
    
    return (rand_x,rand_y)


#============== image manipulation ==============#

def findImage(needle_image, haystack_image, search_type=None):
    # finds images in window/region
    # if region not specified searches the whole window
    # search_type = None, 'all', 'bool'
    # if search_type is not specified, this returns the first image it finds
    # 'all' returns a list of all (x,y,w,h)
    # 'bool' returns True or False
    success = False
    while not success:
        try:
            if search_type == 'all':
                match = list(pyautogui.locateAll(needle_image, haystack_image))
                
            elif search_type == 'bool':
                if pyautogui.locate(needle_image, haystack_image) == None:
                    match = False
                else:
                    match = True
            else:
                match = pyautogui.locate(needle_image, haystack_image)
            
            success  = True
                
        except:
            pass

    return match


def isSameImage(self, img1, img2):
    # this checks if two images are equal to eachother
    # pyautogui treats (0,0,0) as alfa so that is why im using this
    img1_rgb_data = getRgb(img1)
    img2_rgb_data = getRgb(img2)
    
    if img1_rgb_data == img2_rgb_data:
        match = True
    else:
        math = False

    return match


def changeColor(img, target_color, to_color=(0,0,0), action='change'):
    # this changes color of an image
    # 'change' will change all pixels == target_color into to_color
    # 'keep' will change all pixels that != target_color into to_color
    rgb_img = getRgb(img)
    size = img.size

    data = []
    for pixel in rgb_img:
        if action == 'change':
            if pixel == target_color:
                data.append(to_color)
            else:
                data.append(pixel)
                
        elif action == 'keep':
            if pixel == target_color:
                data.append(pixel)
            else:
                data.append(to_color)

    img = imageFromRgb(data, size)

    return img



def removeBackground(img, img_background, region=False):
    #this removes background color (currently only inventory)
    if region:
        x,y,w,h = region
        x2 = x + w
        y2 = y + h
        img_background = img_background.crop((x,y,x2,y2))
        
    rgb_img = getRgb(img)
    rgb_background = getRgb(img_background)
    size = img.size
    
    data = []
    for i in range(len(rgb_img)):
        pixel_img = rgb_img[i]
        pixel_background = rgb_background[i]
            
        if pixel_img == pixel_background:
            data.append((0,0,0))
        else:
            data.append(pixel_img)

    img = imageFromRgb(data, size)
            
    return img


def getRgb(img):
    data = list(img.getdata())
    
    return data

def imageFromRgb(data, size):
    data = numpy.asarray(data, dtype=numpy.uint8)
    img = Image.frombytes('RGB', size, data,'raw', 'RGB', 0, 1)

    return img

def imageFromBgrx(data, size):
    data = numpy.asarray(data, dtype=numpy.uint8)
    img = Image.frombytes('RGB', size, data,'raw', 'BGRX', 0, 1)

    return img


def sleep(t):
    if isinstance(t, tuple):
        t = randomizer(t, False)
        
    time.sleep(t)






