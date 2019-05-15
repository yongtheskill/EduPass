from django.urls import path

from . import views
from django.urls import path, include
from django.views.generic.base import TemplateView


urlpatterns = [
    path('', views.indexPage, name='home'),
    path('finance/', views.financePage, name='Finance'),
    path('finance/parent/', views.parentsFinancePage, name='Finance'),
    path('communication/', views.communicationPage, name='Finance'),
    path('store1/', views.store1, name='Store1'),
    path('store2/', views.store2, name='Store2'),
    path('store3/', views.store3, name='Store3'),
]
