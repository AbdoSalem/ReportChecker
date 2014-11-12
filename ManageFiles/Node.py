'''
Created on Oct 30, 2014

@author: abdo
'''
import os
import shutil

class Child:
    def __init__(self, name,parent):
        self.parent=parent
        self.name=name
        self.create()
    
    def create(self):
        print 'creating %s'%self.get_path()
        if not(os.path.exists(self.get_path())):
            os.makedirs(self.get_path())
    
    def get_name(self):
        return self.name
    
    def remove(self):
        if os.path.exists(self.get_path()):
            shutil.rmtree(self.get_path())
    
    def get_path(self):
        return self.parent.get_path()+os.sep+self.name
    
class Root:
    def __init__(self, name,parent):
        self.parent=parent
        self.name=name
    
    def create(self):
        print 'creating %s'%self.get_path()
        if not(os.path.exists(self.get_path())):
            os.makedirs(self.get_path())
    
    def get_name(self):
        return self.name
    
    def remove(self):
        if os.path.exists(self.get_path()):
            shutil.rmtree(self.get_path())
    
    def get_path(self):
        return self.parent+os.sep+self.name