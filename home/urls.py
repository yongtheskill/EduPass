from django.urls import path

from . import views
from django.urls import path, include
from django.views.generic.base import TemplateView


urlpatterns = [
    path('', views.indexPage, name='home'),
]
