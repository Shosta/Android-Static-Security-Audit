#coding utf-8

'''
'''
import bcolors
import cmdutils
import logging

def unzip_package(package_name):
    '''
    Unzip the package and store the result in the "UnzippedPackaged" folder.

    Params: 
    package_name The package name, without the ".apk" extension, that is going to be unzipped. 
    '''
    print(bcolors.OKGREEN + "Extract package  : " + bcolors.BOLD + package_name + bcolors.ENDC + " to " + bcolors.BOLD + "/tmp/Attacks/UnzippedPackaged" + bcolors.ENDC + " folder.")
    cmd = "unzip /tmp/Attacks/SourcePackage/" + package_name + ".apk '*' -d /tmp/Attacks/UnzippedPackaged"

    output = cmdutils.launchcmdreturnoutput(cmd)
    #process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)
    #output = process.communicate()
    
    logging.display_verbose_logging(output[0])
    logging.display_logging(bcolors.BOLD + "Done" + bcolors.ENDC)

def disassemble_package(package_name):
    """
    Disassemble the application package using the apktool.
    apktool must be installed on the computer.

    Params: 
    package_name The package name, without the ".apk" extension, that is going to be unzipped. 
    """
    print(bcolors.OKGREEN + "Disassemble package " + bcolors.ENDC + bcolors.BOLD + package_name + ".apk" + bcolors.ENDC + " using " + bcolors.BOLD + "apktool" + bcolors.ENDC)
    cmd = "apktool d " + "/tmp/Attacks/SourcePackage/" +  package_name + ".apk" + " -f -o " + "/tmp/Attacks/DecodedPackage"

    output = cmdutils.launchcmdreturnoutput(cmd)
    
    logging.display_verbose_logging(output[0])
    logging.display_logging(bcolors.BOLD + "Done" + bcolors.ENDC)

def make_application_debuggable():
    '''
    Use sed command to add debuggable=true to the Application Manifest.
    '''
    #Use sed method to add debuggable=true to the application manifest.
    print(bcolors.OKGREEN + "Make app debuggable" + bcolors.ENDC +  " using " + bcolors.BOLD + "sed" + bcolors.ENDC + " command")
    cmd = "sed -i -e 's/<application /<application android:debuggable=\"true\" /' /tmp/Attacks/DecodedPackage/AndroidManifest.xml"

    output = cmdutils.launchcmdreturnoutput(cmd)
    
    logging.display_verbose_logging(output[0])
    logging.display_logging(bcolors.BOLD + "Done" + bcolors.ENDC)  

def allow_backup():
    '''
    Use grep and sed commands to allow backup on the application through the Application Manifest.
    '''
    print(bcolors.OKGREEN + "Allow backup on app" + bcolors.ENDC + " using " + bcolors.BOLD + "sed" + bcolors.ENDC + " command")
    cmd = "sed -i -e 's/android:allowBackup=\"false\" / /' /tmp/Attacks/DecodedPackage/AndroidManifest.xml"
    cmdutils.launchcmd(cmd)

    cmd = "sed -i -e 's/<application /<application android:allowBackup=\"true\" /' /tmp/Attacks/DecodedPackage/AndroidManifest.xml"
    output = cmdutils.launchcmdreturnoutput(cmd)
    
    logging.display_verbose_logging(output[0])
    logging.display_logging(bcolors.BOLD + "Done" + bcolors.ENDC)

def repackage_debuggable_application(package_name):
    '''
    
    '''
    print(bcolors.OKGREEN + "Repackage the app" + bcolors.ENDC + " using " + bcolors.BOLD + "apktool" + bcolors.ENDC)
    cmd = "apktool b /tmp/Attacks/DecodedPackage -o /tmp/Attacks/DebuggablePackage/" + package_name + ".b.apk"
    output = cmdutils.launchcmdreturnoutput(cmd)
    
    logging.display_verbose_logging(output[0])
    logging.display_logging(bcolors.BOLD + "Done" + bcolors.ENDC)

def sign_apk(package_name):
    print(bcolors.OKGREEN + "Sign the application " + bcolors.ENDC + "using " + bcolors.BOLD + "appium/signapk" + bcolors.ENDC + " tool")
    cmd = "signapk /tmp/Attacks/DebuggablePackage/" + package_name + ".b.apk"
    output = cmdutils.launchcmdaliasreturnoutput(cmd)
    
    logging.display_verbose_logging(output[0])
    logging.display_logging(bcolors.BOLD + "Done" + bcolors.ENDC)

def reinstall_app(package_name):
    print(bcolors.OKGREEN + "Uninstall the production app from the device" + bcolors.ENDC)
    cmd = "adb uninstall " + package_name
    cmdutils.launchcmd(cmd)
    logging.display_logging(bcolors.BOLD + "Done" + bcolors.ENDC)

    print(bcolors.OKGREEN + "Reinstall the debuggable app to the device" + bcolors.ENDC)
    cmd = "adb install /tmp/Attacks/DebuggablePackage/" + package_name + ".b.s.apk"
    output = cmdutils.launchcmdreturnoutput(cmd)
    
    logging.display_verbose_logging(output[0])
    logging.display_logging(bcolors.BOLD + "Done" + bcolors.ENDC)