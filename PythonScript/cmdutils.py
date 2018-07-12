import subprocess
from subprocess import Popen, PIPE

def launchcmdreturnoutput(cmd):
    '''
    '''
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)

    #Launch the shell command:
    output = process.communicate()
    return output

def launchcmd(cmd):
    '''
    '''
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)

    #Launch the shell command:
    process.communicate()