from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from core.models import Profile, Patient, MedicalRecord

class HospitalAPITests(APITestCase):
    def setUp(self):
        # register doctor1
        response = self.client.post('/api/signup/', {
            'username': 'doc1',
            'password': 'pass123',
            'role': 'doctor'
        })
        self.assertEqual(response.status_code, 200)

        # login doctor1
        response = self.client.post('/api/login/', {
            'username': 'doc1',
            'password': 'pass123'
        })
        self.assertEqual(response.status_code, 200)
        self.doctor1_token = response.data['token']

        # register doctor2
        response = self.client.post('/api/signup/', {
            'username': 'doc2',
            'password': 'pass123',
            'role': 'doctor'
        })
        self.assertEqual(response.status_code, 200)

        # login doctor2
        response = self.client.post('/api/login/', {
            'username': 'doc2',
            'password': 'pass123'
        })
        self.assertEqual(response.status_code, 200)
        self.doctor2_token = response.data['token']

    def test_patient_creation(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.doctor1_token)
        response = self.client.post('/api/patients/', {
            'name': 'john does',
            'age': 32,
            'gender': 'Male',
            'address': 'Lagos,Nigeria'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patient.objects.count(), 1)

    def test_doctor_can_view_only_own_patients(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.doctor1_token)
        self.client.post('/api/patients/', {
            'name': 'Patient 1',
            'age': 40,
            'gender': 'Male',
            'address': 'Address 1'
        })

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.doctor2_token)
        response = self.client.get('/api/patients/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_doctor_cannot_view_other_patient_records(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.doctor1_token)
        response = self.client.post('/api/patients/', {
            'name': 'Patient Protected',
            'age': 55,
            'gender': 'Male',
            'address': 'Hidden Street'
        })
        patient_id = response.data['id']

        MedicalRecord.objects.create(
            patient=Patient.objects.get(id=patient_id),
            symptoms='Headache',
            diagnosis='Migraine',
            treatment='Painkillers'
        )

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.doctor2_token)
        response = self.client.get(f'/api/patients/{patient_id}/records/')
        self.assertEqual(response.status_code, 403)

    def test_login_returns_token(self):
        response = self.client.post('/api/login/', {
            'username': 'doc1',
            'password': 'pass123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
