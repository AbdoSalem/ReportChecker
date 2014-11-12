'''
Created on Nov 1, 2014

@author: abdo
'''
import json
import os

class status_file:
    '''
    classdocs
    '''
    name="status.json"
    status=""
    def __init__(self, parent):
        self.parent=parent
        parent.add_status(self)
        if not(os.path.exists(self.get_path())):
            print "creating status file:%s"%self.get_path()
            f=open(self.get_path(),"w")
            f.write("{\"absence\":{},\"report\":{}}")            
            f.close()
            
    def get_path(self):
        return self.parent.get_path()+os.sep+self.name
    
    def read_file(self):
        f=open(self.get_path(),'r')       
        self.status=json.loads(f.read())
        
    def update_file(self):
        f=open(self.get_path(),"w")
        f.write(json.dumps(self.status))
        f.close()
    
    def get_absences(self):
        self.read_file()
        return self.status["absence"]
    
    def get_absence(self,date):
        self.read_file()
        return self.status["absence"][date]
    
    def add_absence(self,date,absence):
        self.read_file()       
        self.status["absence"][date]=absence
        self.update_file()
        
    def get_reports(self):
        self.read_file()
        return self.status["report"]
    
    def get_report(self,name):
        self.read_file()
        return self.status["report"][name]
    
    def add_report(self,name,report,date):
        self.read_file()       
        self.status["report"][name]=[report,date]
        self.update_file()
        
        
        