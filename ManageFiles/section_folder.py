'''
Created on Oct 28, 2014

@author: abdo
'''
import os
import shutil
from Node import *
from Student_folder import *
class section_folder(Child):
    students=[]
    def add_student(self,student):
        self.students.append(student)
        
        
    def get_students(self):
        result=[]
        for x in os.listdir(self.get_path()):
            result.append(Student_folder(x,self))
           
        self.reports=result   
        return result
   