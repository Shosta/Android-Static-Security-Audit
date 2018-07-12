#coding: utf-8
"""
The main class of the Script
"""

import os
import errno
import sys
import getopt
import bcolors
import retrieveandsavepackage


def usage():
    print("AndroidStaticSecurity v0 - a tool to accelerate your Android application security\nassessments and take care of the boring setup.")
    print("Copyright 2018 Rémi Lavedrine " + bcolors.OKBLUE + "<remi.lavedrine@outlook.com>" + bcolors.ENDC)

    print("\nusage : python AndroidStaticSecurity.py [option] ")
    print("-a, --app-name <apk_name>\tThe name, or a part of it, of the apk you want to analyse")
    print("-v, --verbose\t\t\tDisplay more information during the security analysis")
    print("example : " + bcolors.OKBLUE + "python AndroidStaticSecurity -a facebook" + bcolors.ENDC)
    print("\nFor additional info, see https://github.com/shosta")




def test_insecure_logging():
    #Launch logcat
    #Wait for input from the user
    print(bcolors.OKGREEN + "Test Insecure Logging" + bcolors.ENDC)

    #from datetime import date
    cmd = "adb logcat > /tmp/Attacks/InsecureLogging/log-" + str(1)  + ".txt"
    cmdutils.launchcmd(cmd)
    
    raw_input("Use the app (login, use the application\'s features). The logs are going to be located in the " + bcolors.BOLD +  "/tmp/Attacks/InsecureLogging/" + bcolors.ENDC + " folder.")
    process.kill()
    
def main(argv):

    retrieveandsavepackage.create_attacks_folder_tree()
    
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
        #Wait for input from user in order to choose which apk to retreive through adb
            app_name = raw_input('Which package do you want to investigate (you can give just the name of it)?')
            
    
    packages_list = retrieveandsavepackage.get_packages_list_from_string(app_name)

    package_name = retrieveandsavepackage.choose_package_from_list(packages_list)
    
    package_path = retrieveandsavepackage.get_package_path_from_package_name(package_name)
    
    retrieveandsavepackage.pull_package_from_path(package_name, package_path)
    
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