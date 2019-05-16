from django.contrib import admin

from .models import Event, Payment

# Register your models here.
admin.site.register(Event)
admin.site.register(Payment)