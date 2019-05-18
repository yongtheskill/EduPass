from django.shortcuts import render

import random
import string
import decimal

import phonenumbers
import boto3

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Student, Event, Payment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.views.decorators.csrf import csrf_exempt

def indexPage(request):
    if (request.user.is_authenticated and request.user.student.isParent):
        childName = Student.objects.get(usrname=request.user.student.childName).displayName
        context = {'childsName': childName,}
        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html')


def financePage(request):
    if (request.user.is_authenticated):
        childName = request.user.student.displayName       
        balance = request.user.student.money
        context = {'balance': balance, 'childName': childName}
        return render(request, 'finance.html', context)
    else:
        return render(request, 'finance.html')
    
def parentsFinancePage(request):
    if (request.user.is_authenticated and request.user.student.isParent):
        childName = Student.objects.get(usrname=request.user.student.childName).displayName
        balance = Student.objects.get(usrname=request.user.student.childName).money
        context = {'childsName': childName, 'balance': balance,}
        return render(request, 'parentsFinance.html', context)
    else:
        return render(request, 'parentsFinance.html')
    
def communicationPage(request):
    if (request.user.is_authenticated and request.user.student.isParent):
        childName = Student.objects.get(usrname=request.user.student.childName).displayName
        comments = Student.objects.get(usrname=request.user.student.childName).comments
        teacher = Student.objects.get(usrname=request.user.student.childName).teacher
        context = {'childsName': childName, 'comments': comments, 'teacher': teacher}
        return render(request, 'communication.html', context)
    else:
        return render(request, 'communication.html')
    

def eventsPage(request):
    events = Event.objects.all()
    if request.method == 'POST':
        listOfApproved = []
        for i in request.POST:
            if i != "csrfmiddlewaretoken" and i != "action":
                listOfApproved.append(int(i))

        allEvents = Event.objects.all()
        for i in allEvents:
            i.isApproved = False
            i.save()

        for i in listOfApproved:
            currentEvent = Event.objects.get(pk=i)
            currentEvent.isApproved = True
            currentEvent.save()

    childName = Student.objects.get(usrname=request.user.student.childName).displayName
    context = {'childsName': childName, 'events': events}
    return render(request, 'events.html', context)





def store1(request):
    return render(request, 'store1.html')
    
def store2(request):
    return render(request, 'store2.html')
    
def store3(request):
    return render(request, 'store3.html')



    
def paymentStatus(request):
    paymentData = Payment.objects.get(index=1)

    return JsonResponse({'requestingVerification': paymentData.requestingVerification})
    

def setPaymentAmt(request, paymentAmt, storeId):
    paymentData = Payment.objects.get(index=1)
    actualAmt = 0.11
    actualAmt = paymentAmt / 100
    paymentData.payAmt = actualAmt

    paymentData.paymentFailed = False
    paymentData.isPaid = False
    paymentData.requestingVerification = True
    paymentData.save()


    actualAmtString = "{:.2f}".format(actualAmt)
    
    context = {
        'paymentAmt': actualAmtString, 'unformattedPaymentAmt': paymentAmt, 'storeId': storeId,
        }
    return render(request, 'waitForPayment.html', context)

def paymentSuccess(request, paymentAmt, storeId):
    paymentData = Payment.objects.get(index=1)
    actualAmt = 0.11
    actualAmt = paymentAmt / 100
    for i in Student.objects.all():
        i.money -= decimal.Decimal(actualAmt)
        i.save()
    paymentData.payAmt = -1
    paymentData.isPaid = False
    paymentData.save()
    
    context = {
        'storeId': storeId,
        }

    return render(request, 'paymentSuccess.html', context)
        
def paymentFailed(request, paymentAmt, storeId):
    paymentData = Payment.objects.get(index=1)
    context = {
        'storeId': storeId,
        'paymentAmt': paymentAmt,
    }

    return render(request, 'paymentFailed.html', context)
    
def paymentAuthSuccess(request):
    paymentData = Payment.objects.get(index=1)
    paymentData.isPaid = True
    paymentData.requestingVerification = False
    paymentData.save()

    return HttpResponse('isPaid: True, requestingVerification: False')
    
def paymentAuthFail(request):
    paymentData = Payment.objects.get(index=1)
    paymentData.paymentFailed = True
    paymentData.requestingVerification = False
    paymentData.save()

    return HttpResponse('paymentFailed: True, requestingVerification: False')

def checkIfPaid(request):
    paymentData = Payment.objects.get(index=1)

    data = {
        'isPaid': paymentData.isPaid,
        'isFailed': paymentData.paymentFailed
    }

    return JsonResponse(data)


def twoFactor(request):
    username = request.POST.get('username', '0')
    password = request.POST.get('password', '0')
    phoneNumber = request.POST.get('phoneNumber', '0')
    twoFactorActualKey = request.POST.get('actual2Fa', '0')
    twoFactorInput = request.POST.get('twoFactorInput', '0')
    if(twoFactorActualKey == twoFactorInput):
        user = authenticate(username=username, password=password)
        if user is not None: 
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        authMessage = "EduPass Login Two-Factor authentication code for " + username + ": \n" + twoFactorActualKey

        client = boto3.client(
            "sns",
            aws_access_key_id="AKIAQF4IUI6ABXEKSZEE",
            aws_secret_access_key="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",
            region_name="us-east-1"
        )

        client.publish(
            PhoneNumber= phonenumbers.format_number(phoneNumber, phonenumbers.PhoneNumberFormat.E164),
            Message=authMessage
        )

        print("2fK: " +  twoFactorActualKey)

        numberList = list(str(phoneNumber))
        numberList[:4] = "****"
        displayNumber = "".join(numberList)

        context = {
            'twoFactorKey': twoFactorActualKey,
            'displayNumber': displayNumber,
            'phoneNumber': phoneNumber,
            'username': username,
            'password': password,
        }


        return render(request, 'twoFactor.html', context)
    