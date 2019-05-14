from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render

def indexPage(request):
    return render(request, 'home.html')

def financePage(request):
    return render(request, 'finance.html')
    
def store1(request):
    return render(request, 'store1.html')
    
def store2(request):
    return render(request, 'store2.html')
    
def store3(request):
    return render(request, 'store3.html')