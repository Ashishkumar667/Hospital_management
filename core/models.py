from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (('doctor', 'Doctor'), ('admin', 'Admin'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Patient(models.Model):
    GENDER_CHOICES = (('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    symptoms = models.TextField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
