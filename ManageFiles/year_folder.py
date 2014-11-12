import os
import shutil
from Node import *
from section_folder import section_folder
from status_file import *
from Student_folder import *

from ReportsManager import ReportsManager
import json
class year_folder(Root):   
    sections=[]
    def add_section(self,section):
        self.sections.append(section)
            
    def get_sections(self):
        result=[]
        for x in os.listdir(self.get_path()):
            result.append(section_folder(x,self))
           
        self.reports=result   
        return result
    
    def get_status(self):
        return status_file(self)
    
    def add_status(self,status):
        self.status=status
    
    def add_report(self,reportname,name,hashed_file):
        status=status_file(self)
        status.read_file()
        if 'reports' in status.status:
            status.status['reports'][reportname].append([name,hashed_file])
        else:
            print 'new one'
            status.status=json.loads('{"reports":{}}')
            status.status['reports'][reportname]=[[name,hashed_file]]            
        status.update_file()
    def get_reports(self,report):
        status=status_file(self)
        status.read_file()
        return  status.status['reports'][report]
            
        
r=ReportsManager(4)        
year=year_folder("4","/media/abdo/Abdo/faculty work/DB/Reports")        
section=section_folder("section1",year )
student=Student_folder("ahmed",section)
report=report_folder("report1",student)

year.add_report(report.get_name(),student.get_name(),r.get_file_hash('/media/abdo/Abdo/faculty work/DB/Reports/2year/section2/test/test/db_report.sql'))
list= year.get_reports('report1')

