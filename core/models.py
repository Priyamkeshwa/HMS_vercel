from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add more patient-specific fields if needed

    def __str__(self):
        return self.user.username

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    file_name = models.CharField(max_length=255)
    file_data = models.BinaryField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('done', 'Done'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Prescription {self.id} for {self.patient.user.username}"

class DoctorRemark(models.Model):
    prescription = models.OneToOneField(Prescription, on_delete=models.CASCADE, related_name='remark')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    remark = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Remark by {self.doctor.username} on Prescription {self.prescription.id}"
