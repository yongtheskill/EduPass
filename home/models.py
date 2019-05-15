from django.db import models

from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usrname = models.CharField(max_length=100, default='')
    isParent = models.BooleanField(default=False)
    displayName = models.CharField(max_length=100, default='')
    childName = models.CharField(max_length=100, default='')
    money = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    isPaid = models.BooleanField(default=False)
    phoneNumber = models.IntegerField(default=-1)
    teacher = models.CharField(max_length=100, default='')
    comments = models.TextField(default="none")
    parentsFeedback = models.TextField(default="none")

class Event(models.Model):
    eventName = models.CharField(max_length=200, default='')
    description = models.TextField(default="")
    date = models.DateField(default="2019-05-19")
    isApproved = models.BooleanField(default=False)

    def __str__(self):
        return self.eventName