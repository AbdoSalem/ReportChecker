f'''
Created on Nov 8, 2014

@author: abdo
'''
from report_folder import *
from section_folder import *
from Student_folder import *
from status_file import *
from properities import *
#from year_folder import *
import MySQLdb as mdb 
import datetime, time
import json
# Import smtplib for the actual sending function
import smtplib
import thread
import sys
import imaplib
import getpass
import email
import datetime
import re
import hashlib
import filecmp

# Import the email modules we'll need
from email.mime.text import MIMEText

class ReportsManager:
    def __init__(self, year):
        self.year = year
        
    def handle_report_mail(self, message, mailHandler):
        mailsubject = json.loads(message["Subject"])
        self.mailHandler = mailHandler
        self.year = year_folder("year" + self.year, "/media/abdo/Abdo/faculty work/DB/Reports")        
        self.section = section_folder("section" + str(mailsubject["section"]), self.year)
        self.student = Student_folder(mailsubject["student"], self.section)    
        if not (self.student in self.section.get_students()):
                self.section.add_student(self.student)
                
        report = report_folder(mailsubject["report"], self.student)
                
        #check if report exists     
        if not mailsubject["report"] in self.student.get_status().get_reports():             
            
            #check if report exists            
            self.student.add_report(report, self.mailHandler.get_message_date(message).strftime("%a, %d %b %Y %H:%M:%S"))
                
            part=self.mailHandler.get_attachment(message)
            filename = report.get_path()+os.sep+part.get_filename()
            payload=  part.get_payload(decode=True)
               
            #write the report to its folder
            fp = open(filename, 'wb')
            fp.write(payload)
            fp.close()
            
            #check for similar reports
            if 'reports' in self.year.get_status():
                for x in self.year.get_reports(mailsubject["report"]):
                    if self.get_file_hash(filename) == x[1]:
                        self.send_message(message["From"], "Your report will not be considered as it is the same as the one delivered by" + x[0])
                        os.remove(filename)
                        self.student.add_report(report, 'similar to the report delivered by' + x[0])                       
                        return
                    
            print '%s saved!' % filename
            self.year.add_report(report.get_name(),self.student.get_name(),self.get_file_hash(payload))            
            
            self.execute_sql(filename, message)
        else:
            print 'report already exists'
    
    def exec_sql_file(self, connection, sql_file):
        print "\n[INFO] Executing SQL script file: '%s'" % (sql_file)
        statement = ""
        cursor = connection.cursor()
        for line in open(sql_file):
            if re.match(r'--', line) or len(line.strip()) == 0:  # ignore sql comment lines
                continue
            if not re.search(r'[^-;]+;', line):  # keep appending lines that don't end in ';'
                statement = statement + line
            else:  # when you get a line ending in ';' then exec statement and reset for next statement
                statement = statement + line
                # print "\n\n[DEBUG] Executing SQL statement:\n%s" % (statement)
                cursor.execute(statement)   
                statement = ""
    
    def send_message(self, to, body):
        try:
            msg = email.mime.multipart.MIMEMultipart()
            msg['To'] = to
            msg['From'] = 'mail@company.com'
            msg['Subject'] = self.report.get_name() + ' result.'
            msg.add_header('reply-to', to)
            smtpObj = smtplib.SMTP('localhost')
            part1 = MIMEText(body, 'plain')
            msg.attach(part1)
            smtpObj.sendmail('mail@company.com', to, msg.as_string())         
            print "Successfully sent email"
        except SMTPException:
            print "Error: unable to send email"
        print 'sending%s' % body
    
    def execute_sql(self, file, message):
        connection = mdb.connect('127.0.0.1', 'root', 'password', 'test')
        try:
            self.exec_sql_file(connection, file)
            self.send_message(message["From"], "Thanks, your report is correct.")
        except mdb.Error, e:
            try:
                self.send_message(message["From"], "The execution of your report encountred a problem :\nMySQL Error" + str(e.args[0]) + ":" + e.args[1])
            except IndexError:
                self.send_message(message["From"], "The execution of your report encountred a problem :\nMySQL Error:" + e.args[1])            
        connection.close()
    
       
    def get_file_hash(self, file):
        statement = ""
        for line in open(file):
            if re.match(r'--', line) or len(line.strip()) == 0:  # ignore sql comment lines
                continue
            if not re.search(r'[^-;]+;', line):  # keep appending lines that don't end in ';'
                statement = statement + line
            else:  # when you get a line ending in ';' then exec statement and reset for next statement
                statement = statement + line
        print statement
        return self.get_hash(statement)
        
            
    def get_hash(self, commands):
        m = hashlib.sha224()
        m.update(commands)
        return m.hexdigest()



  

class MailHandler:
    def __init__(self, mail, password):
        self.mail = mail
        self.password = password
        
    def login(self):
        self.M = imaplib.IMAP4_SSL('imap.gmail.com')
        try:
                     
            self.M.login(self.mail,self.password)
            self.loggedin = True
            rv, mailboxes = self.M.list()
            if rv == 'OK':
                print "Mailboxes:"
                for x in  mailboxes:
                    print x
        except imaplib.IMAP4.error:
            print "LOGIN FAILED!!! "
    
    
    def get_first_text_block(self, email_message_instance):
        maintype = email_message_instance.get_content_maintype()
        if maintype == 'multipart':
            for part in email_message_instance.get_payload():
                if part.get_content_maintype() == 'text':
                    return part.get_payload()
        elif maintype == 'text':
            return email_message_instance.get_payload()
        
    def get_attachment(self, message):
        if message.get_content_maintype() == 'multipart':  # multipart messages only
            for part in message.walk():
                # find the attachment part
                if part.get_content_maintype() == 'multipart': continue
                if part.get('Content-Disposition') is None: continue
                return part
    
    def get_message_date(self, message):
        date_tuple = email.utils.parsedate_tz(message['Date'])
            
        if date_tuple:
            return datetime.datetime.fromtimestamp(
                        email.utils.mktime_tz(date_tuple))
            
            
            
    def get_reportmails(self):
        self.login()
        if not self.loggedin:
            return
        
        self.rv, self.data = self.M.select('[Gmail]/Important')
        if self.rv == 'OK':
            print "Processing mailbox...\n"
        rv, data = self.M.search(None, "ALL")
        result = [] 
        if rv != 'OK':
            print "No messages found!"
            return
        
        for self.num in data[0].split()[::-1]:
            rv, data = self.M.fetch(self.num, '(RFC822)')
            if rv != 'OK':
                print "ERROR getting message", self.num
                return
            msg = email.message_from_string(data[0][1])
            a = re.compile('^{"student"(=|:)"-?[A-z]+","section"(=|:)-?[0-9],"report"(=|:)"-?[A-z]+"}$')
            
            if self.get_message_date(msg).year == 2014 and self.get_message_date(msg).month > 9:
                if(a.match(msg['Subject'])): 
                    result.append(msg)
                    r = ReportsManager("2")    
                    r.handle_report_mail(msg, self)
                    print "message %s:is formatted" % self.num
                else:
                    print "message %s:not formatted" % self.num
            else:
                break
        return result  


prop=propertyfile("/media/abdo/Abdo/faculty work/DB/Reports")  
MailHandler(prop.get_property('mail'),prop.get_property('password')).get_reportmails()
  
