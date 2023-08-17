"""
URL configuration for EHR project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('login.urls')),
    path('login', include('login.urls')),
    path('searchUser', include('login.urls')),
    path('newDoctor', include('login.urls')),
    path('newPatient', include('login.urls')),
    path('admin/', admin.site.urls),
    path('userProfile', include('login.urls')),
    path('medicalBills', include('login.urls')),
    path('medicalRecords', include('login.urls')),
    path('medications', include('login.urls')),
    path('adminDashboard', include('login.urls')),
    path('doctorDashboard', include('login.urls')),
    path('newDoctor', include('login.urls')),
    path('newPatient', include('login.urls')),
    path('newPrescription', include('login.urls')),
    path('newAppointment', include('login.urls')),
    path('newMedicalRecord', include('login.urls')),
    path('newMedicalBill', include('login.urls')),
    path('newMedication', include('login.urls')),
    path('newReport', include('login.urls')),
    path('doctor_searchPatient', include('login.urls')),
    path('doctorAppointment', include('login.urls')),
    path('doctorMedicalBill', include('login.urls')),
    path('doctorBillPayment', include('login.urls'))
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


