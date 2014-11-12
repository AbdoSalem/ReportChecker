import os
import shutil
from Node import *
class subject_folder(Child):
  
        
    def addReport(self,report):
        self.reports.append(report)
        
    def getreports(self):
        return self.reports
    
 