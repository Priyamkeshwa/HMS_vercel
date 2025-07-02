from django.contrib import admin
from .models import Patient, Prescription, DoctorRemark

# Register your models here.
admin.site.register(Patient)
admin.site.register(Prescription)
admin.site.register(DoctorRemark)
