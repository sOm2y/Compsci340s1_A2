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
import re
import io

#import readline





#initialise dir
global root
path = 'A2dir' #create A2dir
if not os.path.exists(path):
    os.makedirs(path)

root=os.getcwd()+"/A2dir"
os.chdir(root)
curPath="-"

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
            


#change filepath
def cd(command):
    try:
        if len(command)>1:
            if  command[1].endswith("-"):
                _path=command[1]
                return _path
            else:
                raise OSError          
        else:
            _path="-"
            return _path
    except OSError:
        print("cd: "+command[1]+": No such file or directory")



#TODO:list the files and directories in the named ffs directory. 
#If no name is given use the current working ffs directory. 
#Uses the same rules for absolute and relative as cd. 
#In the output files are indicated with “f: ” preceding their names and directories are indicated with “d: ”.
def ls():
    #print(root)
    for the_file in os.listdir(root):
        #print(the_file)
        fd=re.split('-',the_file)
        if len(fd)>2:
            print("d: "+fd[len(fd)-1])
        else:
            print("f: "+fd[1])


#TODO: shows the output of the real “ls -l” command on the real A2dir directory
def rls(command):
    os.system('ls -l')

def genLine(path):
    line="="
    for i in range(len(path)):       
        line=line+"="
    print(line)
        

#TODO: shows all files below this directory as an indented tree structure. 
#Uses the same parameter rules as ls.
def tree():
    
    for the_file in os.listdir(root):
        pathOrFile=re.split('-',the_file)
        _path="-"
        for i in range(len(pathOrFile)):
            
            if len(pathOrFile)==2:  #in root dir                
                print(_path)

            elif i<(len(pathOrFile)-1): #not last element
                _path=_path+pathOrFile[i]+"-"
                print(_path)
                genLine(_path)

            elif i == (len(pathOrFile)-1):#last element in array
                print(pathOrFile[i])
     

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
    try:
        if  command[1].endswith("-"):
            raise OSError
        else:
            #_filename=re.split('-',command[1])
            return open(command[1], 'w+')
    except OSError:
        print("create: "+command[1]+" Invaild Filename")    



#TODO: appends text to the named file. 
#The first parameter is the filename, 
#the next parameter is the text and consists of the rest of the command line 
#starting one space after the filename. 
#The text is appended to the file. 
#This is the only way to put data into a file. File names can be absolute or relative.
def add(command):
    try:
        with open("-"+command[1], 'r', encoding='utf-8') as readFile:
            content=readFile.read()
        with open("-"+command[1], 'w', encoding='utf-8') as writeFile:
            writeFile.write(content+command[2])
    except:
        print("add: Invaild input"+sys.exc_info())
    finally:
        readFile.close()
        writeFile.close()


#TODO:displays the contents of the named file. File names can be absolute or relative.  
def cat(command):
    try:
        with open("-"+command[1], 'r', encoding='utf-8') as file:
            content=file.read()
            print (content)
    except:
        print("cat: Invaild input"+sys.exc_info()) 
    finally:
        file.close()


#TODO: deletes the named file. File names can be absolute or relative.
def delete():
    pass

#TODO: deletes selected dir
def dd(command):
    try:
        for files in os.listdir(root):
            #print(files)
            pathOrFile=re.split('-',files)
            for filename in pathOrFile:
                #print(filename);

                if command[1] == filename:
                    print(filename);
                    os.remove(files)
    except:
        print("delete directory error:", sys.exc_info())
 
   

#print current path
def pwd(_path):
    print (_path)


#quit programme
def quit():
    sys.exit(0)




#rest_command
def rest_command(command):
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
        





#execute commands            
def exec_command(command):

    try:
        global curPath
        
    
#        last_command = _command[len(_command) - 1]
        if command[0] == 'pwd':
            if (not curPath.startswith("-")):
                print("-"+curPath)
            else:
                print(curPath)
        elif command[0] == 'cd':
            curPath=cd(command)
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
        elif command[0]=='add':
            add(command)
        elif command[0]=='cat':
            cat(command)
        elif command[0]=='dd':
            dd(command)    
        else:
            rest_command(command)
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
    
    exec_command(_command)

    

