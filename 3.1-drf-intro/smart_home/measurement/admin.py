from django.contrib import admin

from .models import Sensor, Measurement

admin.site.register(Sensor)
admin.site.register(Measurement)