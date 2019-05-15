from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render
from .models import Student, Event

def indexPage(request):
    if (request.user.student.isParent):
        childName = Student.objects.get(usrname=request.user.student.childName).displayName
        context = {'childsName': childName,}
        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html')


def financePage(request):
    if (request.user.student.isParent):
        balance = Student.objects.get(usrname=request.user.student.childName).money
        context = {'balance': balance,}
        return render(request, 'finance.html', context)
    else:
        return render(request, 'home.html')
    
def parentsFinancePage(request):
    if (request.user.student.isParent):
        childName = Student.objects.get(usrname=request.user.student.childName).displayName
        balance = Student.objects.get(usrname=request.user.student.childName).money
        context = {'childsName': childName, 'balance': balance,}
        return render(request, 'parentsFinance.html', context)
    else:
        return render(request, 'home.html')
    
def communicationPage(request):
    if (request.user.student.isParent):
        childName = Student.objects.get(usrname=request.user.student.childName).displayName
        comments = Student.objects.get(usrname=request.user.student.childName).comments
        teacher = Student.objects.get(usrname=request.user.student.childName).teacher
        context = {'childsName': childName, 'comments': comments, 'teacher': teacher}
        return render(request, 'communication.html', context)
    else:
        return render(request, 'home.html')
    

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