#coding: utf-8
"""
The main class of the Script
"""

import os
import errno
import sys
import getopt
import bcolors
import cmdutils
import retrieveandsavepackage
import repackageapp
import variables

import subprocess

def usage():
    print("AndroidStaticSecurity v0 - a tool to accelerate your Android application security\nassessments and take care of the boring setup.")
    print("Copyright 2018 Rémi Lavedrine " + bcolors.OKBLUE + "<remi.lavedrine@outlook.com>" + bcolors.ENDC)

    print("\nusage : python AndroidStaticSecurity.py [option] ")
    print("-a, --app-name <apk_name>\tThe name, or a part of it, of the apk you want to analyse")
    print("-v, --verbose\t\t\tDisplay more information during the security analysis")
    print("example : " + bcolors.OKBLUE + "python AndroidStaticSecurity -a facebook" + bcolors.ENDC)
    print("\nFor additional info, see https://github.com/shosta")


def main(argv):

    retrieveandsavepackage.create_attacks_folder_tree()
    
    try:
        opts, args = getopt.getopt(argv, "hav:i", ["help", "app-name", "verbose", "insecure-logging="])
    except getopt.GetoptError:
        print('Type \'AndroidStaticSecurity.py -h\' for help.')
        sys.exit(2)

    app_name = '' 

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(2)
            #raise Exception('Usage displayed, stop application')
        elif opt in ("-a", "--app-name"):
            app_name = arg
        elif opt in ("-v", "--verbose"):
            print("il y a bien v")
            variables.DISPLAY_VERBOSE = True
        elif opt == "--insecure-logging":
            print("Faire uniquement les attaques Insecure Logging.")


    if app_name == '':
        #Wait for input from user in order to choose which apk to retreive through adb
            app_name = raw_input('Which package do you want to investigate (you can give just the name of it)?\n')
    '''        
    # Retrieve the application
    packages_list = retrieveandsavepackage.get_packages_list_from_string(app_name)

    package_name = retrieveandsavepackage.choose_package_from_list(packages_list)
    
    package_path = retrieveandsavepackage.get_package_path_from_package_name(package_name)
    
    retrieveandsavepackage.pull_package_from_path(package_name, package_path)
    
    # Depackage the app to wider the attack surface and then Repackage the app
    repackageapp.unzip_package(package_name)
    
    repackageapp.disassemble_package(package_name)

    repackageapp.make_application_debuggable()

    repackageapp.allow_backup()

    repackageapp.repackage_debuggable_application(package_name)

    repackageapp.sign_apk(package_name)

    repackageapp.reinstall_app(package_name)
    '''
    #Attacks
    from attacks import insecurelogging
    insecurelogging.test_insecure_logging()

if __name__ == '__main__':   
    main(sys.argv[1:])