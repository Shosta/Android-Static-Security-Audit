# Android-Static-Security-Audit
Some commands to test the security of an Android App

Check for some key that are available in the application package.

Get it from adb
> adb pull packageName

Change the file name from ".apk" to ".zip".
Unzip the file.

Run the following commands :
* > find . -name "*key"
* > find . -name "*cer*"
* > find . -name "*pass*"'''

If you find some file twhose name is key try these commands :
> hexdump ./path/to/.appkey  -vC
> more ./path/to/.appkey 


Check the application signature.

Get the package name of the application if you don't have it.
> adb pm list packages -f

Verify the signature : 
> apksigner verify --verbose Application.apk

and

Move to the META.INF folder and check the signature with openssl : 
> openssl pkcs7 -inform DER -in CERT.RSA -noout -print_certs -text

You can then check the type of encryption used (hint, sha1 is no more secure).
