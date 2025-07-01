from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Patient, MedicalRecord, Profile
from .serializers import PatientSerializer, MedicalRecordSerializer, SignupSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class SignupView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(request_body=SignupSerializer)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response(serializer.errors, status=400)
    
class testingEndpoint(APIView):
    def get(self, request):
        return Response({"message": "This is a test endpoint."}, status=status.HTTP_200_OK)
    

class LoginView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(request_body=SignupSerializer)

    def post(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=400)

class PatientListCreateView(APIView):
    
    def get(self, request):
        user = request.user
        role = Profile.objects.get(user=user).role
        if role == 'admin':
            patients = Patient.objects.all()
        else:
            patients = Patient.objects.filter(created_by=user)
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(request_body=MedicalRecordSerializer)
    def post(self, request):
        
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddMedicalRecordView(APIView):
    @swagger_auto_schema(request_body=MedicalRecordSerializer)
    def post(self, request):
        data = request.data.copy()
        patient = Patient.objects.get(id=data['patient'])
        if patient.created_by != request.user and not request.user.is_superuser:
            return Response({'error': 'Forbidden'}, status=403)
        serializer = MedicalRecordSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class ViewPatientRecords(APIView):
    
    def get(self, request, id):
        patient = Patient.objects.get(id=id)
        user = request.user
        role = Profile.objects.get(user=user).role
        if role != 'admin' and patient.created_by != user:
            return Response({'error': 'Forbidden'}, status=403)
        records = MedicalRecord.objects.filter(patient=patient)
        serializer = MedicalRecordSerializer(records, many=True)
        return Response(serializer.data)
