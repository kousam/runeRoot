from PIL import Image
import os
import importlib.util
from importlib import reload




def getFiles(path):
    files = os.listdir(path)
    return files

    

class Files():
    def __init__(self):
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.parent_path = os.path.abspath(os.path.join(self.path, os.pardir))
        self.image_lib = {}
        self.root_image_dir = '{}\\images\\root\\'.format(self.path)
        self.item_image_dir = '{}\\images\\item\\'.format(self.path)
        self.script_module_lib = {}
        self.script_dir = '{}\\scripts\\'.format(self.parent_path)
        self.loadImages('root', self.root_image_dir)
        self.loadImages('item', self.item_image_dir)
        

    def loadImages(self, title, dir):
        #loads images in PIL format
        
        if title not in self.image_lib:
            self.image_lib[title] = {}
        
        for file in getFiles(dir):
            image_name = file.split('.')[0] #this just takes the extension away
            
            path = '{}{}'.format(dir, file) 
            
            img = Image.open(path)
            self.image_lib[title][image_name] = img

            
    
    def loadScriptImages(self, script_title):
        dir = '.\\{}\\images'.format(script_title)
        self.loadImages(script_title, dir)

    def loadScripts(self):
        garbage_collection = [self.script_module_lib[script_name]for script_name in self.script_module_lib]
        for i in garbage_collection:
            del i
            
        self.script_module_lib = {}
        
        
        for file in getFiles(self.script_dir):
            script_name = file.split('.')[0] #this just takes the extension away
            try:
                if script_name not in self.script_module_lib and file.split('.')[1] == 'py':
                    path = '{}{}'.format(self.script_dir, file)
                    
                    spec = importlib.util.spec_from_file_location(file, path)
                    script_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(script_module)
                    
                    self.script_module_lib[script_name] = script_module
            except Exception as e:
                pass
                
            
    def getImageLibrary(self):
        return self.image_lib

    def getParentLibrary(self, parent):
        return self.image_lib[parent]

        
    def getImage(self, parent, image_name):
        return self.image_lib[parent][image_name]

    def getScriptModuleLibrary(self):
        return self.script_module_lib
    
    def getScriptModule(self, title):
        return self.script_module_lib[title]

files = Files()





