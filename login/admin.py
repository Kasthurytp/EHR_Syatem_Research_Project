from django.contrib import admin
from .models import HospitalStaffProfile
from .models import patientAppointment
from .models import patientMedicalRecords
from .models import patientMedicalBills
from .models import patientMedications
from .models import createPatient


# Register your models here.

admin.site.register(HospitalStaffProfile)
admin.site.register(patientAppointment)
admin.site.register(patientMedicalRecords)
admin.site.register(patientMedicalBills)
admin.site.register(patientMedications)
admin.site.register(createPatient)
