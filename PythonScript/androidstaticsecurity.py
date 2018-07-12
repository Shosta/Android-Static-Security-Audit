#coding: utf-8
"""
The main class of the Script
"""

import os
import errno
import sys
import getopt


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def usage():
    print("AndroidStaticSecurity v0 - a tool to accelerate your Android application security\nassessments and take care of the boring setup.")
    print("Copyright 2018 Rémi Lavedrine " + bcolors.OKBLUE + "<remi.lavedrine@outlook.com>" + bcolors.ENDC)

    print("\nusage : python AndroidStaticSecurity.py [option] ")
    print("-a, --app-name <apk_name>\tThe name, or a part of it, of the apk you want to analyse")
    print("-v, --verbose\t\t\tDisplay more information during the security analysis")
    print("example : " + bcolors.OKBLUE + "python AndroidStaticSecurity -a facebook" + bcolors.ENDC)
    print("\nFor additional info, see https://github.com/shosta")


def unzip_package(package_name):
    print(bcolors.OKGREEN + "Extract package  : " + bcolors.BOLD + package_name + bcolors.ENDC + " to " + bcolors.BOLD + "/tmp/Attacks/UnzippedPackaged" + bcolors.ENDC + " folder.")
    cmd = "unzip /tmp/Attacks/SourcePackage/" + package_name + ".apk '*' -d /tmp/Attacks/UnzippedPackaged"

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)
    output = process.communicate()
    print(output[0]) # Verbose

def disassemble_package(package_name):
    """
    Disassemble the application package using the apktool.
    apktool must be installed on the computer.
    """
    print(bcolors.OKGREEN + "Disassemble package " + bcolors.ENDC + bcolors.BOLD + package_name + ".apk" + bcolors.ENDC + " using " + bcolors.BOLD + "apktool" + bcolors.ENDC)
    cmd = "apktool d " + "/tmp/Attacks/SourcePackage/" +  package_name + ".apk" + " -f -o " + "/tmp/Attacks/DecodedPackage"

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)

    #Launch the shell command:
    output = process.communicate()
    print(output)

def make_application_debuggable():
    #Use sed method to add debuggable=true to the application manifest.
    print(bcolors.OKGREEN + "Make app debuggable" + bcolors.ENDC +  " using " + bcolors.BOLD + "sed" + bcolors.ENDC + " command")
    cmd = "sed -i -e 's/<application /<application android:debuggable=\"true\" /' /tmp/Attacks/DecodedPackage/AndroidManifest.xml"

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)

    #Launch the shell command:
    output = process.communicate()
    print(output)    

def allow_backup():
    #Use grep and sed to allow backup on the application.
    print(bcolors.OKGREEN + "Allow backup on app" + bcolors.ENDC + " using " + bcolors.BOLD + "sed" + bcolors.ENDC + " command")
    cmd = "sed -i -e 's/android:allowBackup=\"false\" / /' /tmp/Attacks/DecodedPackage/AndroidManifest.xml"

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)

    #Launch the shell command:
    output = process.communicate()

    cmd = "sed -i -e 's/<application /<application android:allowBackup=\"true\" /' /tmp/Attacks/DecodedPackage/AndroidManifest.xml"

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)

    #Launch the shell command:
    output = process.communicate()
    print(output[0])

def repackage_debuggable_application(package_name):
    print(bcolors.OKGREEN + "Repackage the app" + bcolors.ENDC + " using " + bcolors.BOLD + "apktool" + bcolors.ENDC)
    cmd = "apktool b /tmp/Attacks/DecodedPackage -o /tmp/Attacks/DebuggablePackage/" + package_name + ".b.apk"
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)

    #Launch the shell command:
    output = process.communicate()
    print(output[0])

def sign_apk(package_name):
    print(bcolors.OKGREEN + "Sign the application " + bcolors.ENDC + "using " + bcolors.BOLD + "appium/signapk" + bcolors.ENDC + " tool")
    cmd = "signapk /tmp/Attacks/DebuggablePackage/" + package_name + ".b.apk"
    process = subprocess.Popen(["/bin/bash", "-i", "-c", cmd])

    #Launch the shell command:
    output = process.communicate()
    print(output[0])

def reinstall_app(package_name):
    print(bcolors.OKGREEN + "Uninstall the production app from the device" + bcolors.ENDC)
    cmd = "adb uninstall " + package_name
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)
    process.communicate()


    print(bcolors.OKGREEN + "Reinstall the debuggable app to the device" + bcolors.ENDC)
    cmd = "adb install /tmp/Attacks/DebuggablePackage/" + package_name + ".b.s.apk"
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)
    output = process.communicate()
    print(output[0])


def test_insecure_logging():
    #Launch logcat
    #Wait for input from the user
    print(bcolors.OKGREEN + "Test Insecure Logging" + bcolors.ENDC)

    #from datetime import date
    cmd = "adb logcat > /tmp/Attacks/InsecureLogging/log-" + str(1)  + ".txt"
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)
    process.communicate()

    raw_input("Use the app (login, use the application\'s features). The logs are going to be located in the " + bcolors.BOLD +  "/tmp/Attacks/InsecureLogging/" + bcolors.ENDC + " folder.")
    process.kill()
    
def main(argv):

    create_attacks_folder_tree()
    
    try:
        opts, args = getopt.getopt(argv, "ha:", ["help", "app-name="])
    except getopt.GetoptError:
        print('Type \'AndroidStaticSecurity.py -h\' for help.')
        sys.exit(2)

    app_name = '' 

    for opt, arg in opts:
        if opt in ["-h", "--help"]:
            usage()
            sys.exit(2)
            #raise Exception('Usage displayed, stop application')
        elif opt in ("-a", "--app-name"):
            app_name = arg

    if app_name == '':
        #Wait for input from user in order to choose which apk to retrive through adb
        app_name = raw_input('Which package do you want to investigate (you can give just the name of it)?')
        
    
    packages_list = get_packages_list_from_string(app_name)

    package_name = choose_package_from_list(packages_list)
    
    package_path = get_package_path_from_package_name(package_name)
    
    pull_package_from_path(package_name, package_path)
    
    unzip_package(package_name)
    
    disassemble_package(package_name)

    make_application_debuggable()

    allow_backup()

    repackage_debuggable_application(package_name)

    sign_apk(package_name)

    reinstall_app(package_name)
    
    #Attacks
    #test_insecure_logging()

if __name__ == '__main__':   
    main(sys.argv[1:])