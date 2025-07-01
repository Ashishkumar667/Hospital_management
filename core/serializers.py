from rest_framework import serializers
from .models import Patient, MedicalRecord
from django.contrib.auth.models import User

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=[('doctor', 'Doctor'), ('admin', 'Admin')])

    class Meta:
        model = User
        fields = ['username', 'password', 'role']

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(**validated_data)
        from .models import Profile
        Profile.objects.create(user=user, role=role)
        return user

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['created_by']

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = '__all__'
