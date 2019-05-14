from django.db import models

from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    StudentName = models.CharField(max_length=100)
    ParentName = models.CharField(max_length=100)
    Money = models.DecimalField(decimal_places=2, max_digits=10)
    IsPaid = models.BooleanField()

