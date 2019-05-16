from django.shortcuts import render

import decimal

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Student, Event, Payment

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
