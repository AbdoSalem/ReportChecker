import os
import shutil
from Node import *
from report_folder import *
from status_file import *
class Student_folder(Child):
    reports=[]
    def add_report(self,report,date):
        self.reports.append(report)
        self.get_status().add_report(report.get_name(),report.get_path(),date)
        
    def get_reports(self):
        result=[]
        for x in  os.listdir(self.get_path()):
            if os.path.isdir(os.path.join(self.get_path(),x)):
                result.append(report_folder(x,self))
           
        self.reports=result   
        return result
    
    def get_status(self):
        return status_file(self)
    
    def add_status(self,status):
        self.status=status
        