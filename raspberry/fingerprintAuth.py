import requests
from time import sleep

import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint

## Tries to initialize the sensor
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

## Gets some sensor information
print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))


requestingVerification = False

tryNumber = 1

while (True):
    verificationRequest = requests.get(url = "http://edupass-env.jeabjjzbuw.ap-southeast-1.elasticbeanstalk.com/payment/auth/status/")
    requestingVerification = verificationRequest.json()['requestingVerification']
    if(requestingVerification):
        while (tryNumber <=5):
            try:
                print('Waiting for finger...')

                ## Wait that finger is read
                while ( f.readImage() == False ):
                    pass

                ## Converts read image to characteristics and stores it in charbuffer 1
                f.convertImage(0x01)

                ## Searchs template
                result = f.searchTemplate()

                positionNumber = result[0]
                accuracyScore = result[1]

                if ( positionNumber == -1 ):
                    print('No match found!')
                    tryNumber += 1
                else:
                    requests.get(url = "http://edupass-env.jeabjjzbuw.ap-southeast-1.elasticbeanstalk.com/payment/auth/success/")
                    tryNumber = 100
                print ("try number: " + tryNumber)
            except Exception as e:
                print("ono :( " + e)

        tryNumber = 1


        #fingerprint stuff
        #ans = input("Verification success? [Y/N]")
        #if ans == "Y":
        #    requests.get(url = "http://edupass-env.jeabjjzbuw.ap-southeast-1.elasticbeanstalk.com/payment/auth/success/")
        #else:
        #    requests.get(url = "http://edupass-env.jeabjjzbuw.ap-southeast-1.elasticbeanstalk.com/payment/auth/fail/")

    sleep(1)