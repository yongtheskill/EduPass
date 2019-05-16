import requests
from tkinter import *
import tkinter.messagebox
from time import sleep


def allow():
    print("allowed")
    #requests.get(url = "http://edupass-env.jeabjjzbuw.ap-southeast-1.elasticbeanstalk.com/payment/auth/success/")
    
def deny():
    print("denied")
    #requests.get(url = "http://edupass-env.jeabjjzbuw.ap-southeast-1.elasticbeanstalk.com/payment/auth/fail/")


requestingVerification = False

while (True):
    verificationRequest = requests.get(url = "http://edupass-env.jeabjjzbuw.ap-southeast-1.elasticbeanstalk.com/payment/auth/status/")
    requestingVerification = verificationRequest.json()['requestingVerification']
    if(requestingVerification):

        #fingerprint stuff
        ans = input("Verification success? [Y/N]")
        if ans == "Y":
            requests.get(url = "http://edupass-env.jeabjjzbuw.ap-southeast-1.elasticbeanstalk.com/payment/auth/success/")
        else:
            requests.get(url = "http://edupass-env.jeabjjzbuw.ap-southeast-1.elasticbeanstalk.com/payment/auth/fail/")

    sleep(1)