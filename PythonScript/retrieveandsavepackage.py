#coding: utf-8
 
'''

'''
import os
import errno
import subprocess
import bcolors

def create_folder(folder_location):
    """
    Create a folder at a specific location

    Params:
    folder_location The desired location where the folder is going to be created.
    """
    try:
        os.mkdir(folder_location)
    except OSError, e:
        if e.errno == errno.EEXIST and os.path.isdir(folder_location):
            # File exists, and it's a directory,
            # another process beat us to creating this dir, that's OK.
            pass
        else:
            # Our target dir exists as a file, or different error,
            # reraise the error!
            raise

def create_attacks_folder_tree():
    '''
    Create the subfolders related to each attacks based on OWASP Top 10 Mobile where we are going to save our static analysis for each attacks.
    Create the "Attacks" folder that is going to gather all the attacks type folder.
    InsecureBackup
    InsecureLogging
    InsecureStorage
    '''
    source_package_folder_location = "/tmp/Attacks/SourcePackage"

    unzipped_package_folder_location = "/tmp/Attacks/UnzippedPackaged"
    decoded_package_folder_location = "/tmp/Attacks/DecodedPackaged"
    insecure_backup_folder_location = "/tmp/Attacks/InsecureBackup"
    insecure_logging_folder_location = "/tmp/Attacks/InsecureLogging"
    insecure_storage_folder_location = "/tmp/Attacks/InsecureStorage"
    debuggable_package_folder_location = "/tmp/Attacks/DebuggablePackage"

    create_folder("/tmp/Attacks")
    create_folder(source_package_folder_location)
    create_folder(decoded_package_folder_location)
    create_folder(unzipped_package_folder_location)
    create_folder(insecure_backup_folder_location)
    create_folder(insecure_logging_folder_location)
    create_folder(insecure_storage_folder_location)
    create_folder(debuggable_package_folder_location)

def choose_package_from_list(packages_list):
    for index in range(len(packages_list)):
    #for package in packages:
        if packages_list[index] != '':
            print(bcolors.BOLD + bcolors.OKBLUE + "[" + bcolors.FAIL +  str(index+1) + bcolors.BOLD + bcolors.OKBLUE +  "] " + bcolors.ENDC + bcolors.BOLD + packages_list[index].split(":")[1] + bcolors.ENDC)
 

    #Wait for input from user in order to choose which apk to retrive through adb
    variable = raw_input('Which package do you want to investigate (from [' + bcolors.BOLD + bcolors.FAIL + '1' + bcolors.ENDC + '] to [' + bcolors.BOLD + bcolors.FAIL + str(len(packages_list)-1) + bcolors.ENDC + ']) : ')
    return packages_list[int(variable)-1].split(":")[1]

def get_packages_list_from_string(package_name_part):
    '''
    Get all the package names that are installed on the device that contains the package_name_part parameter in their name.

    Params:
    package_name_part The part of the package name that it should look for.

    Return: A list that contains all the packages name that have the package_name_part in their package name.
    '''
    print(bcolors.OKGREEN + "Get the packages names" + bcolors.ENDC + " on the device that contains \"" + bcolors.BOLD + package_name_part + bcolors.ENDC + "\".")
    cmd = "adb shell pm list packages | grep " + package_name_part

    #from subprocess import Popen, PIPE
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)

    #Launch the shell command:
    output = process.communicate()
    packages = output[0].split("\n")
    return packages

def pull_package_from_path(package_name, package_path):
    '''
    Pull a package on the connected devices via adb.

    Params:
    
    package_name The package name, without the "apk" extension.
    package_path The package path on the connected device.
    '''
    print(bcolors.OKGREEN + "Pull package from " + bcolors.ENDC + bcolors.BOLD + package_path.split(":")[1] + bcolors.ENDC + 
    " and store it to " + bcolors.BOLD + "/tmp/Attacks/SourcePackage/" + package_name + ".apk" + bcolors.ENDC + ".")
    cmd = "adb pull " + package_path.split(":")[1] + " "  + "/tmp/Attacks/SourcePackage/" + package_name + ".apk"
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)

    #Launch the shell command:
    process.communicate()

def get_package_path_from_package_name(package_name):
    '''
    Get the package path on the connected devices via adb regarding the package name, without the "apk" extension.

    Params:
    package_name The package name, without the "apk" extension.
    '''
    print(bcolors.OKGREEN + "Get path from " + bcolors.ENDC + bcolors.BOLD + package_name + bcolors.ENDC + ".")
    cmd = "adb shell pm path " + package_name

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)

    #Launch the shell command:
    output = process.communicate()
    package_path = output[0].split("\n")[0]
    print("Path : " + bcolors.BOLD + package_path + bcolors.ENDC)

    return package_path
