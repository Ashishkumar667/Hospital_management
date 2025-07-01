from django.urls import path
from .views import *

urlpatterns = [
    path("",testingEndpoint.as_view()),
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('patients/', PatientListCreateView.as_view()), 
    path('patients/records/add', AddMedicalRecordView.as_view()),
    path('patients/<int:id>/records/', ViewPatientRecords.as_view()),
]
