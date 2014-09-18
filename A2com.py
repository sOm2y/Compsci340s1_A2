#Author: Yue Yin
#UPI: yyin888
#ID: 5398177


#!/usr/bin/python
# -*- coding: utf-8 -*-

# Non class version
# This can be used to break a line into words suitable for this assignment.

import shlex
import os
import sys
import subprocess

#import readline

#global variable
global dictCounter
dictCounter=1
global job_counter
job_counter=1
global _vaildCommand
_vaildCommand=True
dict={}
jobList={}
state=[]

#initialization

path = 'A2dir' #create A2dir
if not os.path.exists(path):
    os.makedirs(path)

global root
root=os.getcwd()+"/A2dir"

os.chdir(root)


#read input
def word_list(line):
    """Break the line into shell words.
    """

    lexer = shlex.shlex(line, posix=True)
    lexer.whitespace_split = False
    lexer.wordchars += '#$+-,./?@^='
    args = list(lexer)
    return args


def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))
            

#TODO:list the files and directories in the named ffs directory. 
#If no name is given use the current working ffs directory. 
#Uses the same rules for absolute and relative as cd. 
#In the output files are indicated with “f: ” preceding their names and directories are indicated with “d: ”.
def ls():

#TODO: shows the output of the real “ls -l” command on the real A2dir directory
def rls(command):
    os.system('ls -l')


#TODO: shows all files below this directory as an indented tree structure. 
#Uses the same parameter rules as ls.
def tree():
    list_files(root)

     

#TODO: removes all files in the ffs root directory. 
#This is like “rm -rf /” in Unix (not a good idea).
def clear():
    for the_file in os.listdir(root):
        file_path = os.path.join(root, the_file)
        try:    
            os.unlink(file_path)
        except:
            print("clear EOFError:", sys.exc_info())

#TODO: creates a file with the specified name. 
#The name must not end with a “-” otherwise it would be a directory and we don’t create directories directly. 
#The name can be either absolute, starting with a “-”, or relative to the working ffs directory.
def create(command):
    return open(command[1], 'w+')
    



#TODO: appends text to the named file. 
#The first parameter is the filename, 
#the next parameter is the text and consists of the rest of the command line 
#starting one space after the filename. 
#The text is appended to the file. 
#This is the only way to put data into a file. File names can be absolute or relative.
def add():
    pass


#TODO: deletes the named file. File names can be absolute or relative.
def delete():
    pass


#print current path
def pwd():
    print (os.getcwd())


#quit programme
def quit():
    sys.exit(0)

#change filepath
def cd(command):
    try:
        _curPath = os.getcwd()
        if len(command)>1:
            os.chdir(_curPath + "/" + command[1])
        else:
            print("cd: "+command[0]+": No such file or directory")
    except OSError:
        print("cd: "+command[1]+": No such file or directory")

#add job 
def add_job(command,child,job_counter):
    try:
        idCommand=[]
        idCommand[0]=child
        idCommand[1]=command
        jobList.update({job_counter : " ".join(idCommand)})
        print("["+str(job_counter)+"] "+str(child))  
    except:
         print("Unexpected error2:", sys.exc_info())

#rest_command
def rest_command(command,job_counter,_vaildCommand):
    try:
        ampersand='&' in command
        if ampersand:
            del command[len(command)-1]
        child = os.fork()#make a child process
        if child==0:#if it is a child
            os.execvp(command[0], command)#execute command
        else:
            if ampersand:
                add_job(command,child,job_counter)
            else:    
                os.waitpid(child,0)#wait util finished
    except:
#        _vaildCommand=False
#        print(_vaildCommand)
        print("Command doesn't exsit!")
        



# # history command
# #def hist(command):
# def history(command,dict):
#     new_command=[]
#     if(len(command)>1):
#         #print(dict)
#         print(dict.get(int(command[1])))
        
#         new_command=str(dict.get(int(command[1]))).split()
#         print(new_command)
#         exec_command(new_command,dict,job_counter)
#     else:     
#         if(len(dict)>10):
#             for i in range((len(dict)-10),len(dict)):
#                 dict_list=str(i+1)+": "+str(dict.get(i+1))
#                 print(dict_list)
#         else:
#             for i in range(len(dict)):
#                 dict_list=str(i+1)+": "+str(dict.get(i+1))
#                 print(dict_list)
    


# #check "|" in right position
# def checkPipe(command):
#     if command[0] == '|' or command[len(command)-1]=='|':
#         print("Invalid use of pipe '|'. ")
#         #print(command)
#         return False
#     else:
#         for i in range( 1,len(command)-1):
#             if command[i]=='|' and command[i+1]=='|':
#                 print("Invalid use of pipe '|'.")
#                 return False
#     #print("correct pipeline input")
#     return True
            
            
# #pipeline
# def pipeline(command):
    
#         try:      
#             if '&' in command:
#                 amper=1
#             else:
#                 amper=0
                
#             #child process
#             child=os.fork()
#             if child==0 :
#                 while '|' in command:
#                     #get '|' index position    
#                     pipe_index=command.index('|')
#                     r,w=os.pipe()
#                     grand_child=os.fork()
#                     if grand_child==0:
#                         os.dup2(w,1)#replace to w in index 1
#                         os.close(w)#close w
#                         os.close(r)# close stand in 
#                         os.execvp(command[0],command[0:pipe_index])# execute command before '|'
#                     os.dup2(r,0)
#                     os.close(r)
#                     os.close(w)
#                     del command[:pipe_index+1]
#                 os.execvp(command[0],command)
#             else:
#                 if amper==0:
#                     os.waitpid(child,0)
#         except:
#             print("Unexpected error2:", sys.exc_info()[0])


# #jobs
# def jobs(jobList):
#     for jobKey in jobList.keys():
#         pid=jobList[jobKey]
#         ps=subprocess.Popen(['ps','-p',str(pid),'-o','state='],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
#         result,error=ps.communicate()
#         if result.decode()!='':
#             print('[{}] <{}> {}'.format(jobKey,result.decode()[0],str(pid)))
#             #print("jobs")
  



#execute commands            
def exec_command(command,dict,job_counter):
    try:
#        last_command = _command[len(_command) - 1]
        if command[0] == 'history' or command[0] == 'h':
            history(command,dict)
        elif command[0] == 'pwd':
            pwd()
        elif command[0] == 'cd':
            cd(command)
        elif '|' in command:
            if checkPipe(command):
                pipeline(command)
                #print("pipe")
        elif command[0]=='jobs':
            jobs(jobList)
        elif command[0]=='rls':
            rls(command) 
        elif command[0]=='create':
            create(command)
        elif command[0]=='tree':
            tree()
        elif command[0]=='clear':
            clear()
        elif command[0]=='ls':
            ls()
        else:
            rest_command(command,job_counter,_vaildCommand)
    except:
        print("Unexpected error1:", sys.exc_info())
        

    
    
        
while True:
    try:
        line = input('ffs> ')
    except EOFError:
        break
    _command = word_list(line)
    if _command[0]=='quit':
        quit()
    
    exec_command(_command,dict,job_counter)

    

    if _vaildCommand:
        dict.update({dictCounter : " ".join(_command)})
    #print(dict)
    #print(len(dict))
    dictCounter+=1
    job_counter+=1
   
