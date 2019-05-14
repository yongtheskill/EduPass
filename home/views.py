from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render

def indexPage(request):
    return render(request, 'home.html')