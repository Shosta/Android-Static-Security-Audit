#coding: utf-8
"""
"""
import subprocess
import logging
import bcolors

def __check_for_user_string_infile():
    string = raw_input(bcolors.BOLD + "Enter a string" + bcolors.ENDC + " that you want to check in the logfile? (or " + bcolors.BOLD + "\"enter\"" + bcolors.ENDC + " to end it)\n> ")
    if string != '':
        __check_for_string_infile(string, "log.txt")
        __check_for_user_string_infile()

def test_insecure_logging():
    #Launch logcat
    #Wait for input from the user
    print(bcolors.OKGREEN + "Test Insecure Logging" + bcolors.ENDC)

    process = __launch_logcat()

    raw_input("Use the app (login, use the application\'s features, etc...). The logs are going to be located in the " + bcolors.BOLD +  "/tmp/Attacks/InsecureLogging/" + bcolors.ENDC + " folder.\nThen press " + bcolors.BOLD + "\"enter\"" + bcolors.ENDC + " on your keyboard to analyse these logs.")
    process.terminate()

    #Check for password in log file
    __check_for_string_infile("password", "log.txt")
    #Check for key in log file
    __check_for_string_infile("key", "log.txt")
    #Check for admin in log file
    __check_for_string_infile("admin", "log.txt")

    #Check for a user entered input
    __check_for_user_string_infile()


def __check_for_string_infile(string, file_name):
    '''
    Check for the occurence of a string using the grep command

    Params: 

    string The string we want to check

    file_name The log file name from the /tmp/Attacks/InsecureLogging
    '''
    to_file_path = "/tmp/Attacks/InsecureLogging/grepresult-" + string + ".txt"
    
    logging.display_logging(bcolors.BOLD + "Check the number of occurences" + bcolors.ENDC + " of " + bcolors.OKGREEN + "\"" + string + "\"" + bcolors.ENDC + " in the log file and store it to " + bcolors.BOLD + to_file_path + bcolors.ENDC + ".")
    cmd = "grep " + string + " /tmp/Attacks/InsecureLogging/" + file_name + " > " + to_file_path
    process = subprocess.Popen(cmd, shell=True)


def __launch_logcat():
    '''
    Launch an "adb logcat" command and redirect the output to a specific file 
    '''
    #TODO Add a timestamp to the file name.
    cmd = "adb logcat > /tmp/Attacks/InsecureLogging/log.txt"
    process = subprocess.Popen(cmd, shell=True)

    return process
    