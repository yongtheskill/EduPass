from django.urls import path

from . import views
from django.urls import path, include
from django.views.generic.base import TemplateView


urlpatterns = [
    path('', views.indexPage, name='home'),
    path('finance/', views.financePage, name='Finance'),
    path('finance/parent/', views.parentsFinancePage, name='Finance'),
    path('communication/', views.communicationPage, name='Communication'),
    path('events/', views.eventsPage, name='Events'),

    path('store1/', views.store1, name='Store1'),
    path('store2/', views.store2, name='Store2'),
    path('store3/', views.store3, name='Store3'),

    path('payment/auth/status/', views.paymentStatus, name='paymentStatus'),
    path('payment/auth/success/', views.paymentAuthSuccess, name='paymentAuthSuccess'),
    path('payment/auth/fail/', views.paymentAuthFail, name='paymentAuthFail'),
    path('<path:storeId>/payment/setAmt/<int:paymentAmt>/', views.setPaymentAmt, name='viewPayment'),
    path('ajax/checkIfPaid/', views.checkIfPaid, name='checkIfPaid'),
    path('<path:storeId>/paid/<int:paymentAmt>/', views.paymentSuccess, name='paymentSuccess'),
    path('<path:storeId>/failed/<int:paymentAmt>/', views.paymentFailed, name='paymentFailed'),

    
    path('auth/twoFactor/', views.twoFactor, name='twoFactor'),
]
