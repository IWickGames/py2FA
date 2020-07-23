py2FA How to
=============================

py2FA is a easy to use python library that will host a server that one user can create a token that they can then use
to request the 2FA keys, this URL can be shared with anyone you would like to also have access as well.

#Step 1
To get started paste the TwoFA folder into the root of you project(or where your main python file is located)

#Step 2
Go into the TwoFA folder and edit the 'osfa_settings.json' and change the settings to your likeing

#Step 3
In your program add this import statement
'import TwoFA.py2FA'

#Step 4
Your now ready to use the py2FA library in your program, here is how to use it


Here is how to use the library once it is imported

#Simple example

import TwoFA.py2FA #Import the library
twoFAInstance = TwoFa.py2FA.OsTwoFa() #Sets up the 2FA instance
twoFAInstance.start2FA() #Starts the webserver

if twoFAInstance.checkKey(input("Enter 2FA Token: ")):
	print("Your Authorized!")
else:
	print("Invalid 2FA token!")