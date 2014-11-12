'''
Created on Nov 12, 2014

@author: abdo
'''
import os,json 
class propertyfile:


    def __init__(self, folder):
        self.folder=folder
        if not(os.path.exists(self.get_path())):
            f=open(self.get_path(),"w")
            f.write("{\"properities\":{}}")            
            f.close()
    
    def get_path(self):
        return self.folder+os.sep+'properities.json'
    
    def read_file(self):
        f=open(self.get_path(),'r')
        self.properities=json.loads(f.read())
        f.close()

    def update_file(self):
        f=open(self.get_path(),'w')
        f.write(json.dumps(self.properities))
        f.close()
        
    def add_property(self,property,value):
        self.read_file()
        self.properities[property]=value
        self.update_file()
        
    def get_property(self,property):
        self.read_file()
        return self.properities[property]
    
    