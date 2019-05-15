from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render
from .models import Student

def indexPage(request):
    childName = Student.objects.get(usrname=request.user.student.childName).displayName
    context = {'childsName': childName,}
    return render(request, 'home.html', context)

def financePage(request):
    balance = Student.objects.get(usrname=request.user.student.childName).money
    context = {'balance': balance,}
    return render(request, 'finance.html', context)
    
def parentsFinancePage(request):
    childName = Student.objects.get(usrname=request.user.student.childName).displayName
    balance = Student.objects.get(usrname=request.user.student.childName).money
    context = {'childsName': childName, 'balance': balance,}
    return render(request, 'parentsFinance.html', context)
    
def store1(request):
    return render(request, 'store1.html')
    
def store2(request):
    return render(request, 'store2.html')
    
def store3(request):
    return render(request, 'store3.html')