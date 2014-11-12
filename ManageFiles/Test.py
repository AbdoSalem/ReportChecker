from report_folder import *
from section_folder import *
from Student_folder import *
from status_file import *

section=section_folder("section2","/home/abdo/test" )
student=Student_folder("abdo",section)
student2=Student_folder("7mada",section)
report=report_folder("report1",student)
print student.parent.get_path()
section.create()
student.create()
student2.create()
report.create()
section.add_student(student)
section.add_student(student2)

status=status_file(student)

s=student.get_status()
s.add_absence("2014-12-10","true")
s.add_report("report1",report.get_path(),"2014-12-10")

print section.get_students()