#coding: utf-8
 
import subprocess
from subprocess import Popen, PIPE

def launchcmdreturnoutput(cmd):
    '''
    '''
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)
    
    #Launch the shell command:
    output = process.communicate()
    return output

def launchcmdaliasreturnoutput(cmd):
    '''
    '''
    process = subprocess.Popen(["/bin/bash", "-i", "-c", cmd]) 
 
    #Launch the shell command:
    output = process.communicate()
    return output

def launchcmd(cmd):
    '''
    '''
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)
    
    #Launch the shell command:
    process.communicate()

def launchcmdalias(cmd):
    '''
    '''
    process = subprocess.Popen(["/bin/bash", "-i", "-c", cmd]) 
 
    #Launch the shell command:
    process.communicate()