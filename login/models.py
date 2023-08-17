from django.db import models
from django.contrib.auth.models import User
from Crypto.Cipher import AES

# Create your models here.

class HospitalStaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    workfor = models.CharField(max_length=100)
    Address = models.CharField(max_length=100)
    age = models.IntegerField()
    dob = models. DateField(auto_now=False, auto_now_add=False)
    status = models.CharField(max_length=10)
    image = models.ImageField(upload_to='pics')
    medicalInsutance = models.CharField(max_length=100)
    VisionInsurance = models.CharField(max_length=100)
    DentalInsurance = models.CharField(max_length=100)

class createDoctor(models.Model):
    photo = models.ImageField(upload_to='pics')
    id_num = models.BinaryField() 
    first_name = models.BinaryField() 
    last_name = models.BinaryField()
    dob = models.DateField()
    sex = models.BinaryField()
    nic = models.BinaryField()
    password = models.BinaryField()
    mobile_number = models.BinaryField()
    email = models.BinaryField()
    address = models.BinaryField()
    primary_phone = models.BinaryField()
    secondary_phone = models.BinaryField()
    encryption_key = models.BinaryField()

class createPatient(models.Model):
    photo = models.ImageField(upload_to='pics')
    id_num = models.BinaryField() 
    first_name = models.BinaryField() 
    last_name = models.BinaryField()
    dob = models.DateField()
    sex = models.BinaryField()
    nic = models.BinaryField()
    mobile_number = models.BinaryField()
    email = models.BinaryField()
    address = models.BinaryField()
    primary_phone = models.BinaryField()
    secondary_phone = models.BinaryField()
    encryption_key = models.BinaryField()

class createNurse(models.Model):
    photo = models.ImageField(upload_to='pics')
    id_num = models.BinaryField() 
    first_name = models.BinaryField() 
    last_name = models.BinaryField()
    dob = models.DateField()
    sex = models.BinaryField()
    nic = models.BinaryField()
    mobile_number = models.BinaryField()
    email = models.BinaryField()
    address = models.BinaryField()
    primary_phone = models.BinaryField()
    secondary_phone = models.BinaryField()
    encryption_key = models.BinaryField()

class createAppointment(models.Model):
    doctor_id = models.BinaryField()
    patient_id = models.BinaryField()
    date = models.DateField()
    visit_type = models.BinaryField()
    location = models.BinaryField()
    comments = models.BinaryField()
    encryption_key = models.BinaryField()

class createPrescription(models.Model):
    doctor_id_num = models.BinaryField()
    patient_id_num = models.BinaryField()
    patientName = models.BinaryField()
    date = models.DateField()
    medicationName = models.BinaryField()
    dose = models.BinaryField()
    frequency = models.BinaryField()
    encryption_key = models.BinaryField()

class createNewMedicalRecord(models.Model):
    doctor_id_num = models.BinaryField()
    patient_id_num = models.BinaryField()
    patient_name = models.BinaryField()
    date = models.DateField()
    location = models.BinaryField()
    message = models.BinaryField()
    encryption_key = models.BinaryField()

class createMedicalBill(models.Model):
    doctor_id_num = models.BinaryField()
    patient_id_num = models.BinaryField()
    service_detail = models.BinaryField()
    date = models.DateField()
    location = models.BinaryField()
    payment_amount = models.BinaryField()
    payment_status = models.BinaryField()
    encryption_key = models.BinaryField()

class createNewMedication(models.Model):
    doctor_id_num = models.BinaryField()
    patient_id_num = models.BinaryField()
    medicationName = models.BinaryField()
    dose = models.BinaryField()
    frequency = models.BinaryField()
    date = models.DateField()
    location = models.BinaryField()
    message = models.BinaryField()
    encryption_key = models.BinaryField()

class createReport(models.Model):
    doctor_id_num = models.BinaryField()
    patient_id_num = models.BinaryField()
    test_type = models.BinaryField()
    date = models.DateField()
    location = models.BinaryField()
    message = models.BinaryField()

class TeHospitalStaffProfile(models.Model):
    encrypted_email = models.BinaryField() 
    encryption_key = models.BinaryField()

class patientAppointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    VisitType = models.CharField(max_length=50)
    Date = models. DateField(auto_now=False, auto_now_add=False)
    Provider = models.CharField(max_length=30)
    AppointmentDate = models. DateField(auto_now=False, auto_now_add=False)

class patientMedicalRecords(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Date = models. DateField(auto_now=False, auto_now_add=False)
    Name = models.CharField(max_length=100)
    Result = models.CharField(max_length=1000)

class patientMedicalBills(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Date = models. DateField(auto_now=False, auto_now_add=False)
    Amount = models.IntegerField()
    Status = models.BooleanField(default=False)

class patientMedications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    MedicationName = models.CharField(max_length=100)
    Dose = models.CharField(max_length=100)
    Frequency = models.CharField(max_length=100)
    Condition = models.CharField(max_length=100)
