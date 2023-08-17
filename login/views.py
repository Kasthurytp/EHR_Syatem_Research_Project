from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import auth
from .models import HospitalStaffProfile
from .models import TeHospitalStaffProfile
from .models import patientAppointment
from .models import patientMedicalRecords
from .models import patientMedicalBills
from .models import patientMedications 
from .models import createPatient
from .models import createDoctor 
from .models import createNurse
from .models import createAppointment 
from .models import createPrescription
from .models import createNewMedicalRecord
from .models import createMedicalBill
from .models import createNewMedication
from .models import createReport
from django.contrib.auth.decorators import login_required
import datetime
from .aes import encrypt, decrypt 
from Crypto.Random import get_random_bytes 
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from django.contrib.auth.hashers import check_password


# Create your views here.

def login(request):
    if request.method== 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_type = request.POST['user_type']

        if user_type == 'doctor':
            doctors = createDoctor.objects.all()

            decrypted_data_list = []
            for doctor in doctors:
                decrypted_email = decrypt(doctor.email, doctor.encryption_key).decode('utf-8')
                decrypted_password = decrypt(doctor.password, doctor.encryption_key).decode('utf-8')
                decrypted_data_list.append((decrypted_email, decrypted_password))

            data_exists = (username, password) in decrypted_data_list

            if data_exists:
                return redirect("doctorDashboard")

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("adminDashboard")
        else:
            messages.info(request, 'Invalid Credential!')
            return redirect('login')
    else:
        return render(request, 'login.html')

#Search User and Display all details related to particular user
def searchUser(request):
    prof = HospitalStaffProfile.objects.filter(user=request.user)
    if request.method == 'POST':
        search_id = request.POST['search_id']

        doctors = createDoctor.objects.all()
        patients = createPatient.objects.all()
        nurses = createNurse.objects.all()

        decrypted_doctor_list = []
        decrypted_data = {}

        decrypted_patient_list = []
        decrypted_patient_data = {}

        decrypted_nurse_list = []
        decrypted_nurse_data = {}

        for doctor in doctors:
            decrypted_id = decrypt(doctor.id_num, doctor.encryption_key).decode('utf-8')
            decrypted_doctor_list.append(decrypted_id)

            if decrypted_id == search_id:
                decrypted_data['id_num'] = decrypt(doctor.id_num, doctor.encryption_key).decode('utf-8')
                decrypted_data['first_name'] = decrypt(doctor.first_name, doctor.encryption_key).decode('utf-8')
                decrypted_data['last_name'] = decrypt(doctor.last_name, doctor.encryption_key).decode('utf-8')
                decrypted_data['dob'] = doctor.dob
                decrypted_data['sex'] = decrypt(doctor.sex, doctor.encryption_key).decode('utf-8')
                decrypted_data['nic'] = decrypt(doctor.nic, doctor.encryption_key).decode('utf-8')
                decrypted_data['mobile_number'] = decrypt(doctor.mobile_number, doctor.encryption_key).decode('utf-8')
                decrypted_data['email'] = decrypt(doctor.email, doctor.encryption_key).decode('utf-8')
                decrypted_data['address'] = decrypt(doctor.address, doctor.encryption_key).decode('utf-8')
                decrypted_data['primary_phone'] = decrypt(doctor.primary_phone, doctor.encryption_key).decode('utf-8')
                decrypted_data['secondary_phone'] = decrypt(doctor.secondary_phone, doctor.encryption_key).decode('utf-8')
                break

        for patient in patients:
            decrypted_id = decrypt(patient.id_num, patient.encryption_key).decode('utf-8')
            decrypted_patient_list.append(decrypted_id)

            if decrypted_id == search_id:
                decrypted_patient_data['id_num'] = decrypt(patient.id_num, patient.encryption_key).decode('utf-8')
                decrypted_patient_data['first_name'] = decrypt(patient.first_name, patient.encryption_key).decode('utf-8')
                decrypted_patient_data['last_name'] = decrypt(patient.last_name, patient.encryption_key).decode('utf-8')
                decrypted_patient_data['dob'] = patient.dob
                decrypted_patient_data['sex'] = decrypt(patient.sex, patient.encryption_key).decode('utf-8')
                decrypted_patient_data['nic'] = decrypt(patient.nic, patient.encryption_key).decode('utf-8')
                decrypted_patient_data['mobile_number'] = decrypt(patient.mobile_number, patient.encryption_key).decode('utf-8')
                decrypted_patient_data['email'] = decrypt(patient.email, patient.encryption_key).decode('utf-8')
                decrypted_patient_data['address'] = decrypt(patient.address, patient.encryption_key).decode('utf-8')
                decrypted_patient_data['primary_phone'] = decrypt(patient.primary_phone, patient.encryption_key).decode('utf-8')
                decrypted_patient_data['secondary_phone'] = decrypt(patient.secondary_phone, patient.encryption_key).decode('utf-8')
                break

        for nurse in nurses:
            decrypted_id = decrypt(nurse.id_num, nurse.encryption_key).decode('utf-8')
            decrypted_nurse_list.append(decrypted_id)

            if decrypted_id == search_id:
                decrypted_nurse_data['id_num'] = decrypt(nurse.id_num, nurse.encryption_key).decode('utf-8')
                decrypted_nurse_data['first_name'] = decrypt(nurse.first_name, nurse.encryption_key).decode('utf-8')
                decrypted_nurse_data['last_name'] = decrypt(nurse.last_name, nurse.encryption_key).decode('utf-8')
                decrypted_nurse_data['dob'] = nurse.dob
                decrypted_nurse_data['sex'] = decrypt(nurse.sex, nurse.encryption_key).decode('utf-8')
                decrypted_nurse_data['nic'] = decrypt(nurse.nic, nurse.encryption_key).decode('utf-8')
                decrypted_nurse_data['mobile_number'] = decrypt(nurse.mobile_number, nurse.encryption_key).decode('utf-8')
                decrypted_nurse_data['email'] = decrypt(nurse.email, nurse.encryption_key).decode('utf-8')
                decrypted_nurse_data['address'] = decrypt(nurse.address, nurse.encryption_key).decode('utf-8')
                decrypted_nurse_data['primary_phone'] = decrypt(nurse.primary_phone, nurse.encryption_key).decode('utf-8')
                decrypted_nurse_data['secondary_phone'] = decrypt(nurse.secondary_phone, nurse.encryption_key).decode('utf-8')
                break

        if search_id in decrypted_doctor_list:
            return render(request, 'searchUser.html', {'doctor': decrypted_data, 'prof': prof})
        if search_id in decrypted_patient_list:
            return render(request, 'searchUser.html', {'patient': decrypted_patient_data, 'prof': prof})
        if search_id in decrypted_nurse_list:
            return render(request, 'searchUser.html', {'nurse': decrypted_nurse_data, 'prof': prof})
        else:
            doctors = createDoctor.objects.all()
            return render(request, 'searchUser.html', {'prof': prof, 'doctors': doctors})

    else:
        return render(request, 'searchUser.html', {'prof': prof})



#Search patient and Display all details related to particular patient - doctor serach patient
def doctor_searchPatient(request):
    if request.method == 'POST':
        search_id = request.POST['search_id']

        patients = createPatient.objects.all()

        decrypted_patient_list = []
        decrypted_patient_data = {}

        for patient in patients:
            decrypted_id = decrypt(patient.id_num, patient.encryption_key).decode('utf-8')
            decrypted_patient_list.append(decrypted_id)

            if decrypted_id == search_id:
                decrypted_patient_data['id_num'] = decrypt(patient.id_num, patient.encryption_key).decode('utf-8')
                decrypted_patient_data['first_name'] = decrypt(patient.first_name, patient.encryption_key).decode('utf-8')
                decrypted_patient_data['last_name'] = decrypt(patient.last_name, patient.encryption_key).decode('utf-8')
                decrypted_patient_data['dob'] = patient.dob
                decrypted_patient_data['sex'] = decrypt(patient.sex, patient.encryption_key).decode('utf-8')
                decrypted_patient_data['nic'] = decrypt(patient.nic, patient.encryption_key).decode('utf-8')
                decrypted_patient_data['mobile_number'] = decrypt(patient.mobile_number, patient.encryption_key).decode('utf-8')
                decrypted_patient_data['email'] = decrypt(patient.email, patient.encryption_key).decode('utf-8')
                decrypted_patient_data['address'] = decrypt(patient.address, patient.encryption_key).decode('utf-8')
                decrypted_patient_data['primary_phone'] = decrypt(patient.primary_phone, patient.encryption_key).decode('utf-8')
                decrypted_patient_data['secondary_phone'] = decrypt(patient.secondary_phone, patient.encryption_key).decode('utf-8')
                break 

        if search_id in decrypted_patient_list:
            return render(request, 'doctor_searchPatient.html', {'patient': decrypted_patient_data})
        else:
            doctors = createDoctor.objects.all()
            return render(request, 'doctor_searchPatient.html', {'patients': patients})

    else:
        return render(request, 'doctor_searchPatient.html')

#
def doctorDashboard(request):
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%I:%M %p, Today, %m/%d/%Y")
    return render(request, 'doctorDashboard.html', {'formatted_datetime': formatted_datetime})

#Create new doctor
def newDoctor(request):
    prof = HospitalStaffProfile.objects.filter(user=request.user)
    if request.method=="POST":
       create_new_doctor=createDoctor() 
       photo=request.POST.get('image')
       id_num=request.POST.get('id_num')
       first_name=request.POST.get('first_name')
       last_name=request.POST.get('last_name')
       dob=request.POST.get('dateOfBirth')
       sex=request.POST.get('sex')
       nic=request.POST.get('nic')
       password=request.POST.get('password')
       mobile_number=request.POST.get('mobile_number')
       email=request.POST.get('email')
       address=request.POST.get('address')
       primary_phone=request.POST.get('primary_phone')
       secondary_phone=request.POST.get('secondary_phone')

       id_num_plaintext = id_num.encode('utf-8')
       first_name_plaintext = first_name.encode('utf-8')
       last_name_plaintext = last_name.encode('utf-8')
       sex_plaintext = sex.encode('utf-8')
       nic_plaintext = nic.encode('utf-8')
       password_plaintext = password.encode('utf-8')
       mobile_number_plaintext = mobile_number.encode('utf-8')
       email_plaintext = email.encode('utf-8')
       address_plaintext = address.encode('utf-8')
       primary_phone_plaintext = primary_phone.encode('utf-8')
       secondary_phone_plaintext = secondary_phone.encode('utf-8')

       key = get_random_bytes(16)  # AES-128 key size

       id_num_ciphertext = encrypt(id_num_plaintext, key)
       first_name_ciphertext = encrypt(first_name_plaintext, key)
       last_name_ciphertext = encrypt(last_name_plaintext, key)
       sex_ciphertext = encrypt(sex_plaintext, key)
       nic_ciphertext = encrypt(nic_plaintext, key)
       password_ciphertext = encrypt(password_plaintext, key)
       mobile_number_ciphertext = encrypt(mobile_number_plaintext, key)
       email_ciphertext = encrypt(email_plaintext, key)
       address_ciphertext = encrypt(address_plaintext, key)
       primary_phone_ciphertext = encrypt(primary_phone_plaintext, key)
       secondary_phone_ciphertext = encrypt(secondary_phone_plaintext, key)


       create_new_doctor.photo=photo
       create_new_doctor.id_num= id_num_ciphertext
       create_new_doctor.first_name= first_name_ciphertext
       create_new_doctor.last_name=last_name_ciphertext
       create_new_doctor.dob=dob
       create_new_doctor.sex=sex_ciphertext
       create_new_doctor.nic=nic_ciphertext
       create_new_doctor.password=password_ciphertext
       create_new_doctor.mobile_number=mobile_number_ciphertext
       create_new_doctor.email=email_ciphertext
       create_new_doctor.address=address_ciphertext
       create_new_doctor.primary_phone=primary_phone_ciphertext
       create_new_doctor.secondary_phone=secondary_phone_ciphertext
       create_new_doctor.encryption_key=key
       create_new_doctor.save()
       return render(request, 'newDoctor.html', {'prof': prof, 'success': True})
    return render(request, 'newDoctor.html', {'prof' : prof})

# Create New Patient
def newPatient(request):
    prof = HospitalStaffProfile.objects.filter(user=request.user)
    if request.method=="POST":
       create_new_patient=createPatient() 
       photo=request.POST.get('image')
       id_num=request.POST.get('id_num')
       first_name=request.POST.get('first_name')
       last_name=request.POST.get('last_name')
       dob=request.POST.get('dateOfBirth')
       sex=request.POST.get('sex')
       nic=request.POST.get('nic')
       mobile_number=request.POST.get('mobile_number')
       email=request.POST.get('email')
       address=request.POST.get('address')
       primary_phone=request.POST.get('primary_phone')
       secondary_phone=request.POST.get('secondary_phone')

       id_num_plaintext = id_num.encode('utf-8')
       first_name_plaintext = first_name.encode('utf-8')
       last_name_plaintext = last_name.encode('utf-8')
       sex_plaintext = sex.encode('utf-8')
       nic_plaintext = nic.encode('utf-8')
       mobile_number_plaintext = mobile_number.encode('utf-8')
       email_plaintext = email.encode('utf-8')
       address_plaintext = address.encode('utf-8')
       primary_phone_plaintext = primary_phone.encode('utf-8')
       secondary_phone_plaintext = secondary_phone.encode('utf-8')

       key = get_random_bytes(16)  # AES-128 key size

       id_num_ciphertext = encrypt(id_num_plaintext, key)
       first_name_ciphertext = encrypt(first_name_plaintext, key)
       last_name_ciphertext = encrypt(last_name_plaintext, key)
       sex_ciphertext = encrypt(sex_plaintext, key)
       nic_ciphertext = encrypt(nic_plaintext, key)
       mobile_number_ciphertext = encrypt(mobile_number_plaintext, key)
       email_ciphertext = encrypt(email_plaintext, key)
       address_ciphertext = encrypt(address_plaintext, key)
       primary_phone_ciphertext = encrypt(primary_phone_plaintext, key)
       secondary_phone_ciphertext = encrypt(secondary_phone_plaintext, key)


       create_new_patient.photo=photo
       create_new_patient.id_num= id_num_ciphertext
       create_new_patient.first_name= first_name_ciphertext
       create_new_patient.last_name=last_name_ciphertext
       create_new_patient.dob=dob
       create_new_patient.sex=sex_ciphertext
       create_new_patient.nic=nic_ciphertext
       create_new_patient.mobile_number=mobile_number_ciphertext
       create_new_patient.email=email_ciphertext
       create_new_patient.address=address_ciphertext
       create_new_patient.primary_phone=primary_phone_ciphertext
       create_new_patient.secondary_phone=secondary_phone_ciphertext
       create_new_patient.encryption_key=key
       create_new_patient.save()
       return render(request, 'newPatient.html', {'prof': prof, 'success': True})
    return render(request, 'newPatient.html', {'prof' : prof})

#create account for nurse
def newNurse(request):
    prof = HospitalStaffProfile.objects.filter(user=request.user)
    if request.method=="POST":
       create_new_Nurse=createNurse() 
       photo=request.POST.get('image')
       id_num=request.POST.get('id_num')
       first_name=request.POST.get('first_name')
       last_name=request.POST.get('last_name')
       dob=request.POST.get('dateOfBirth')
       sex=request.POST.get('sex')
       nic=request.POST.get('nic')
       mobile_number=request.POST.get('mobile_number')
       email=request.POST.get('email')
       address=request.POST.get('address')
       primary_phone=request.POST.get('primary_phone')
       secondary_phone=request.POST.get('secondary_phone')

       id_num_plaintext = id_num.encode('utf-8')
       first_name_plaintext = first_name.encode('utf-8')
       last_name_plaintext = last_name.encode('utf-8')
       sex_plaintext = sex.encode('utf-8')
       nic_plaintext = nic.encode('utf-8')
       mobile_number_plaintext = mobile_number.encode('utf-8')
       email_plaintext = email.encode('utf-8')
       address_plaintext = address.encode('utf-8')
       primary_phone_plaintext = primary_phone.encode('utf-8')
       secondary_phone_plaintext = secondary_phone.encode('utf-8')

       key = get_random_bytes(16)  # AES-128 key size

       id_num_ciphertext = encrypt(id_num_plaintext, key)
       first_name_ciphertext = encrypt(first_name_plaintext, key)
       last_name_ciphertext = encrypt(last_name_plaintext, key)
       sex_ciphertext = encrypt(sex_plaintext, key)
       nic_ciphertext = encrypt(nic_plaintext, key)
       mobile_number_ciphertext = encrypt(mobile_number_plaintext, key)
       email_ciphertext = encrypt(email_plaintext, key)
       address_ciphertext = encrypt(address_plaintext, key)
       primary_phone_ciphertext = encrypt(primary_phone_plaintext, key)
       secondary_phone_ciphertext = encrypt(secondary_phone_plaintext, key)


       create_new_Nurse.photo=photo
       create_new_Nurse.id_num= id_num_ciphertext
       create_new_Nurse.first_name= first_name_ciphertext
       create_new_Nurse.last_name=last_name_ciphertext
       create_new_Nurse.dob=dob
       create_new_Nurse.sex=sex_ciphertext
       create_new_Nurse.nic=nic_ciphertext
       create_new_Nurse.mobile_number=mobile_number_ciphertext
       create_new_Nurse.email=email_ciphertext
       create_new_Nurse.address=address_ciphertext
       create_new_Nurse.primary_phone=primary_phone_ciphertext
       create_new_Nurse.secondary_phone=secondary_phone_ciphertext
       create_new_Nurse.encryption_key=key
       create_new_Nurse.save()
       return render(request, 'newNurse.html', {'prof': prof, 'success': True})
    return render(request, 'newNurse.html', {'prof' : prof})


#create new appointment
def newAppointment(request):
    if request.method=="POST":
       create_new_Appointment= createAppointment() 
       doctor_id=request.POST.get('doctor_id_num')
       patient_id=request.POST.get('patient_id_num')
       date=request.POST.get('date')
       visit_type=request.POST.get('visit_type')
       location=request.POST.get('location')
       comments=request.POST.get('comments')

       doctor_id_plaintext = doctor_id.encode('utf-8')
       patient_id_plaintext = patient_id.encode('utf-8')
       visit_type_plaintext = visit_type.encode('utf-8')
       location_plaintext = location.encode('utf-8')
       comments_plaintext = comments.encode('utf-8')

       key = get_random_bytes(16)  # AES-128 key size

       doctor_id_ciphertext = encrypt(doctor_id_plaintext, key)
       patient_id_ciphertext = encrypt(patient_id_plaintext, key)
       visit_type_ciphertext = encrypt(visit_type_plaintext, key)
       location_ciphertext = encrypt(location_plaintext, key)
       comments_ciphertext = encrypt(comments_plaintext, key)
    
       create_new_Appointment.doctor_id= doctor_id_ciphertext
       create_new_Appointment.patient_id= patient_id_ciphertext
       create_new_Appointment.date= date
       create_new_Appointment.visit_type= visit_type_ciphertext
       create_new_Appointment.location= location_ciphertext
       create_new_Appointment.comments= comments_ciphertext
       create_new_Appointment.encryption_key=key
       create_new_Appointment.save()
       return render(request, 'newAppointment.html', {'success': True})
    return render(request, 'newAppointment.html')


#create new prescription
def newPrescription(request):
    if request.method=="POST":
       create_new_Prescription= createPrescription() 
       doctor_id_num = request.POST.get('doctor_id_num')
       patient_id_num = request.POST.get('patient_id_num')
       patientName = request.POST.get('patientName')
       date=request.POST.get('date')
       medicationName = request.POST.get('medicationName')
       dose = request.POST.get('dose')
       frequency = request.POST.get('frequency')

       doctor_id_num_plaintext = doctor_id_num.encode('utf-8')
       patient_id_num_plaintext = patient_id_num.encode('utf-8')
       patientName_plaintext = patientName.encode('utf-8')
       medicationName_plaintext = medicationName.encode('utf-8')
       dose_plaintext = dose.encode('utf-8')
       frequency_plaintext = frequency.encode('utf-8')

       key = get_random_bytes(16)  # AES-128 key size

       doctor_id_num_ciphertext = encrypt( doctor_id_num_plaintext, key)
       patient_id_num_ciphertext = encrypt(patient_id_num_plaintext, key)
       patientName_ciphertext = encrypt(patientName_plaintext, key)
       medicationName_ciphertext = encrypt(medicationName_plaintext, key)
       dose_ciphertext = encrypt(dose_plaintext, key)
       frequency_ciphertext = encrypt(frequency_plaintext, key)
    
       create_new_Prescription.doctor_id_num = doctor_id_num_ciphertext
       create_new_Prescription.patient_id_num = patient_id_num_ciphertext
       create_new_Prescription.patientName = patientName_ciphertext
       create_new_Prescription.date= date
       create_new_Prescription.medicationName = medicationName_ciphertext
       create_new_Prescription.dose = dose_ciphertext
       create_new_Prescription.frequency = frequency_ciphertext
       create_new_Prescription.encryption_key=key
       create_new_Prescription.save()
       return render(request, 'newPrescription.html', {'success': True})
    return render(request, 'newPrescription.html')


def newMedicalRecord(request):
    if request.method=="POST":
       create_new_MedicalRecord = createNewMedicalRecord() 
       doctor_id_num = request.POST.get('doctor_id_num')
       patient_id_num = request.POST.get('patient_id_num')
       patient_name = request.POST.get('patient_name')
       date = request.POST.get('date')
       location = request.POST.get('location')
       message = request.POST.get('message')

       doctor_id_num_plaintext = doctor_id_num.encode('utf-8')
       patient_id_num_plaintext = patient_id_num.encode('utf-8')
       patient_name_plaintext = patient_name.encode('utf-8')
       location_plaintext = location.encode('utf-8')
       message_plaintext = message.encode('utf-8')

       key = get_random_bytes(16)  # AES-128 key size

       doctor_id_num_ciphertext = encrypt( doctor_id_num_plaintext, key)
       patient_id_num_ciphertext = encrypt(patient_id_num_plaintext, key)
       patient_name_ciphertext = encrypt(patient_name_plaintext, key)
       location_ciphertext = encrypt(location_plaintext, key)
       message_ciphertext = encrypt(message_plaintext, key)
    
       create_new_MedicalRecord.doctor_id_num = doctor_id_num_ciphertext
       create_new_MedicalRecord.patient_id_num = patient_id_num_ciphertext
       create_new_MedicalRecord.patient_name = patient_name_ciphertext
       create_new_MedicalRecord.date= date
       create_new_MedicalRecord.location = location_ciphertext
       create_new_MedicalRecord.message = message_ciphertext
       create_new_MedicalRecord.encryption_key=key
       create_new_MedicalRecord.save()
       return render(request, 'newMedicalRecord.html', {'success': True})
    return render(request, 'newMedicalRecord.html')

#create new medical bill
def newMedicalBill(request):
    if request.method=="POST":
       create_new_MedicalBill = createMedicalBill() 
       doctor_id_num = request.POST.get('doctor_id_num')
       patient_id_num = request.POST.get('patient_id_num')
       service_detail = request.POST.get('service_detail')
       date = request.POST.get('date')
       location = request.POST.get('location')
       payment_amount = request.POST.get('payment_amount')
       payment_status = request.POST.get('payment_status')

       doctor_id_num_plaintext = doctor_id_num.encode('utf-8')
       patient_id_num_plaintext = patient_id_num.encode('utf-8')
       service_detail_plaintext = service_detail.encode('utf-8')
       location_plaintext = location.encode('utf-8')
       payment_amount_plaintext = payment_amount.encode('utf-8')
       payment_status_plaintext = payment_status.encode('utf-8')

       key = get_random_bytes(16)  # AES-128 key size

       doctor_id_num_ciphertext = encrypt( doctor_id_num_plaintext, key)
       patient_id_num_ciphertext = encrypt(patient_id_num_plaintext, key)
       service_detail_ciphertext = encrypt(service_detail_plaintext, key)
       location_ciphertext = encrypt(location_plaintext, key)
       payment_amount_ciphertext = encrypt(payment_amount_plaintext, key)
       payment_status_ciphertext = encrypt(payment_status_plaintext, key)
    
       create_new_MedicalBill.doctor_id_num = doctor_id_num_ciphertext
       create_new_MedicalBill.patient_id_num = patient_id_num_ciphertext
       create_new_MedicalBill.service_detail = service_detail_ciphertext
       create_new_MedicalBill.date= date
       create_new_MedicalBill.location = location_ciphertext
       create_new_MedicalBill.payment_amount = payment_amount_ciphertext
       create_new_MedicalBill.payment_status = payment_status_ciphertext
       create_new_MedicalBill.encryption_key=key
       create_new_MedicalBill.save()
       return render(request, 'newMedicalBill.html', {'success': True})
    return render(request, 'newMedicalBill.html')

#create new medications
def newMedication(request):
    if request.method=="POST":
       create_new_Medication = createNewMedication() 
       doctor_id_num = request.POST.get('doctor_id_num')
       patient_id_num = request.POST.get('patient_id_num')
       medicationName = request.POST.get('medicationName')
       dose = request.POST.get('dose')
       frequency = request.POST.get('frequency')
       date = request.POST.get('date')
       location = request.POST.get('location')
       message = request.POST.get('message')

       doctor_id_num_plaintext = doctor_id_num.encode('utf-8')
       patient_id_num_plaintext = patient_id_num.encode('utf-8')
       medicationName_plaintext = medicationName.encode('utf-8')
       dose_plaintext = dose.encode('utf-8')
       frequency_plaintext = frequency.encode('utf-8')
       location_plaintext = location.encode('utf-8')
       message_plaintext =  message.encode('utf-8')

       key = get_random_bytes(16)  # AES-128 key size

       doctor_id_num_ciphertext = encrypt( doctor_id_num_plaintext, key)
       patient_id_num_ciphertext = encrypt(patient_id_num_plaintext, key)
       medicationName_ciphertext = encrypt(medicationName_plaintext, key)
       dose_ciphertext = encrypt(dose_plaintext, key)
       frequency_ciphertext = encrypt(frequency_plaintext, key)
       location_ciphertext = encrypt(location_plaintext, key)
       message_ciphertext = encrypt(message_plaintext, key)
    
       create_new_Medication.doctor_id_num = doctor_id_num_ciphertext
       create_new_Medication.patient_id_num = patient_id_num_ciphertext
       create_new_Medication.medicationName = medicationName_ciphertext
       create_new_Medication.dose = dose_ciphertext
       create_new_Medication.medicationName = medicationName_ciphertext
       create_new_Medication.date= date
       create_new_Medication.frequency = frequency_ciphertext
       create_new_Medication.location = location_ciphertext
       create_new_Medication.message = message_ciphertext
       create_new_Medication.encryption_key=key
       create_new_Medication.save()
       return render(request, 'newMedication.html', {'success': True})
    return render(request, 'newMedication.html')

def newReport(request):
    if request.method=="POST":
       create_new_Report = createReport() 
       doctor_id_num = request.POST.get('doctor_id_num')
       patient_id_num = request.POST.get('patient_id_num')
       test_type = request.POST.get('test_type')
       date = request.POST.get('date')
       location = request.POST.get('location')
       message = request.POST.get('message')

       doctor_id_num_plaintext = doctor_id_num.encode('utf-8')
       patient_id_num_plaintext = patient_id_num.encode('utf-8')
       test_type_plaintext = test_type.encode('utf-8')
       location_plaintext = location.encode('utf-8')
       message_plaintext = message.encode('utf-8')

       key = get_random_bytes(16)  # AES-128 key size

       doctor_id_num_ciphertext = encrypt( doctor_id_num_plaintext, key)
       patient_id_num_ciphertext = encrypt(patient_id_num_plaintext, key)
       test_type_ciphertext = encrypt(test_type_plaintext, key)
       location_ciphertext = encrypt(location_plaintext, key)
       message_ciphertext = encrypt(message_plaintext, key)
    
       create_new_Report.doctor_id_num = doctor_id_num_ciphertext
       create_new_Report.patient_id_num = patient_id_num_ciphertext
       create_new_Report.test_type = test_type_ciphertext
       create_new_Report.date= date
       create_new_Report.location = location_ciphertext
       create_new_Report.message = message_ciphertext
       create_new_Report.encryption_key=key
       create_new_Report.save()
       return render(request, 'newReport.html', {'success': True})
    return render(request, 'newReport.html')

# Example decryption function
def decrypt_data(encrypted_data, encryption_key):
    decrypted_data = decrypt(encrypted_data, encryption_key).decode('utf-8')
    return decrypted_data

#Retrieve doctor data from databse and decrypt 
def doctors(request):
    prof = HospitalStaffProfile.objects.filter(user=request.user)
    doctors = createDoctor.objects.all()

    # Decrypt the encrypted fields in each patient object
    for doctor in doctors:
        doctor.id_num = decrypt_data(doctor.id_num, doctor.encryption_key)
        doctor.first_name = decrypt_data(doctor.first_name, doctor.encryption_key)
        doctor.last_name = decrypt_data(doctor.last_name, doctor.encryption_key)
        doctor.sex = decrypt_data(doctor.sex, doctor.encryption_key)
        doctor.nic = decrypt_data(doctor.nic, doctor.encryption_key)
        doctor.mobile_number = decrypt_data(doctor.mobile_number, doctor.encryption_key)
        doctor.email = decrypt_data(doctor.email, doctor.encryption_key)
        doctor.address = decrypt_data(doctor.address, doctor.encryption_key)

    return render(request, 'doctors.html', {'prof' : prof, 'doctors': doctors})

def patients(request):
    prof = HospitalStaffProfile.objects.filter(user=request.user)
    patients = createPatient.objects.all()

    # Decrypt the encrypted fields in each patient object
    for patient in patients:
        patient.id_num = decrypt_data(patient.id_num, patient.encryption_key)
        patient.first_name = decrypt_data(patient.first_name, patient.encryption_key)
        patient.last_name = decrypt_data(patient.last_name, patient.encryption_key)
        patient.sex = decrypt_data(patient.sex, patient.encryption_key)
        patient.nic = decrypt_data(patient.nic, patient.encryption_key)
        patient.mobile_number = decrypt_data(patient.mobile_number, patient.encryption_key)
        patient.email = decrypt_data(patient.email, patient.encryption_key)
        patient.address = decrypt_data(patient.address, patient.encryption_key)

    return render(request, 'patients.html', {'prof' : prof, 'patients': patients})

#fetch and disply nurse data
def nurses(request):
    prof = HospitalStaffProfile.objects.filter(user=request.user)
    nurses = createNurse.objects.all()

    # Decrypt the encrypted fields in each patient object
    for nurse in nurses:
        nurse.id_num = decrypt_data(nurse.id_num, nurse.encryption_key)
        nurse.first_name = decrypt_data(nurse.first_name, nurse.encryption_key)
        nurse.last_name = decrypt_data(nurse.last_name, nurse.encryption_key)
        nurse.sex = decrypt_data(nurse.sex, nurse.encryption_key)
        nurse.nic = decrypt_data(nurse.nic, nurse.encryption_key)
        nurse.mobile_number = decrypt_data(nurse.mobile_number, nurse.encryption_key)
        nurse.email = decrypt_data(nurse.email, nurse.encryption_key)
        nurse.address = decrypt_data(nurse.address, nurse.encryption_key)

    return render(request, 'nurse.html', {'prof' : prof, 'nurses': nurses})

def users(request):
    prof = HospitalStaffProfile.objects.filter(user=request.user)
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%I:%M %p, Today, %m/%d/%Y")
    return render(request, 'users.html', {'prof' : prof, 'formatted_datetime': formatted_datetime})

def ePriscribing(request):
    prof = HospitalStaffProfile.objects.filter(user=request.user)
    return render(request, 'newEPrescription.html')

def yourPractice(request):
    prof = HospitalStaffProfile.objects.filter(user=request.user)
    return render(request, 'yourPractice.html')

def laps(request):
    prof = HospitalStaffProfile.objects.filter(user=request.user)
    return render(request, 'laps.html')


def encrypt_decrypt_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Retrieve email from the form input
        plaintext = email.encode('utf-8')
        key = get_random_bytes(16)  # AES-128 key size
        ciphertext = encrypt(plaintext, key)

        # Save the encrypted data to the database
        TeHospitalStaffProfile.objects.create(encrypted_email=ciphertext, encryption_key=key)
        
        decrypted_plaintext = decrypt(ciphertext, key).decode('utf-8')
        
        context = {
            'ciphertext': ciphertext,
            'decrypted_plaintext': decrypted_plaintext,
        }
        return render(request, 'your_template.html', context)
    else:
        return render(request, 'your_template.html')

def display_encrypted_data(request):
    # Retrieve the encrypted data from the database based on some criteria
    en_hospital_staff_profile = createDoctor.objects.get(id=3)  # Fetch the record with id=1, modify as needed
    ciphertext = en_hospital_staff_profile.email
    encryption_key = en_hospital_staff_profile.encryption_key

    decrypted_plaintext = decrypt(ciphertext, encryption_key).decode('utf-8')

    context = {
            'ciphertext': ciphertext,
            'decrypted_plaintext': decrypted_plaintext,
        }


    return render(request, 'your_template.html', context)


def admin_searchUserDashboard(request, doctor_id):
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%I:%M %p, Today, %m/%d/%Y")
    prof = HospitalStaffProfile.objects.filter(user=request.user)

    doctors = createDoctor.objects.all()
    patients = createPatient.objects.all()
    nurses = createNurse.objects.all()
    

    decrypted_list = []
    decrypted_data = {}
    personal_data = {}

    for doctor in doctors:
        decrypted_id = decrypt(doctor.id_num, doctor.encryption_key).decode('utf-8')
        decrypted_list.append(decrypted_id)

        if decrypted_id == doctor_id:
            personal_data['photo'] = doctor.photo
            personal_data['id_num'] = decrypt(doctor.id_num, doctor.encryption_key).decode('utf-8')
            personal_data['first_name'] = decrypt(doctor.first_name, doctor.encryption_key).decode('utf-8')
            personal_data['last_name'] = decrypt(doctor.last_name, doctor.encryption_key).decode('utf-8')
            personal_data['dob'] = doctor.dob
            personal_data['sex'] = decrypt(doctor.sex, doctor.encryption_key).decode('utf-8')
            personal_data['nic'] = decrypt(doctor.nic, doctor.encryption_key).decode('utf-8')
            personal_data['mobile_number'] = decrypt(doctor.mobile_number, doctor.encryption_key).decode('utf-8')
            personal_data['email'] = decrypt(doctor.email, doctor.encryption_key).decode('utf-8')
            personal_data['address'] = decrypt(doctor.address, doctor.encryption_key).decode('utf-8')
            personal_data['primary_phone'] = decrypt(doctor.primary_phone, doctor.encryption_key).decode('utf-8')
            personal_data['secondary_phone'] = decrypt(doctor.secondary_phone, doctor.encryption_key).decode('utf-8')
            break

    for patient in patients:
        decrypted_id = decrypt(patient.id_num, patient.encryption_key).decode('utf-8')
        decrypted_list.append(decrypted_id)

        if decrypted_id == doctor_id:
            decrypted_data['photo'] = patient.photo
            decrypted_data['id_num'] = decrypt(patient.id_num, patient.encryption_key).decode('utf-8')
            decrypted_data['first_name'] = decrypt(patient.first_name, patient.encryption_key).decode('utf-8')
            decrypted_data['last_name'] = decrypt(patient.last_name, patient.encryption_key).decode('utf-8')
            decrypted_data['dob'] = patient.dob
            decrypted_data['sex'] = decrypt(patient.sex, patient.encryption_key).decode('utf-8')
            decrypted_data['nic'] = decrypt(patient.nic, patient.encryption_key).decode('utf-8')
            decrypted_data['mobile_number'] = decrypt(patient.mobile_number, patient.encryption_key).decode('utf-8')
            decrypted_data['email'] = decrypt(patient.email, patient.encryption_key).decode('utf-8')
            decrypted_data['address'] = decrypt(patient.address, patient.encryption_key).decode('utf-8')
            decrypted_data['primary_phone'] = decrypt(patient.primary_phone, patient.encryption_key).decode('utf-8')
            decrypted_data['secondary_phone'] = decrypt(patient.secondary_phone, patient.encryption_key).decode('utf-8')
            break
    
    for nurse in nurses:
        decrypted_id = decrypt(nurse.id_num, nurse.encryption_key).decode('utf-8')
        decrypted_list.append(decrypted_id)

        if decrypted_id == doctor_id:
            decrypted_data['photo'] = nurse.photo
            decrypted_data['id_num'] = decrypt(nurse.id_num, nurse.encryption_key).decode('utf-8')
            decrypted_data['first_name'] = decrypt(nurse.first_name, nurse.encryption_key).decode('utf-8')
            decrypted_data['last_name'] = decrypt(nurse.last_name, nurse.encryption_key).decode('utf-8')
            decrypted_data['dob'] = nurse.dob
            decrypted_data['sex'] = decrypt(nurse.sex, nurse.encryption_key).decode('utf-8')
            decrypted_data['nic'] = decrypt(nurse.nic, nurse.encryption_key).decode('utf-8')
            decrypted_data['mobile_number'] = decrypt(nurse.mobile_number, nurse.encryption_key).decode('utf-8')
            decrypted_data['email'] = decrypt(nurse.email, nurse.encryption_key).decode('utf-8')
            decrypted_data['address'] = decrypt(nurse.address, nurse.encryption_key).decode('utf-8')
            decrypted_data['primary_phone'] = decrypt(nurse.primary_phone, nurse.encryption_key).decode('utf-8')
            decrypted_data['secondary_phone'] = decrypt(nurse.secondary_phone, nurse.encryption_key).decode('utf-8')
            break

    appointments = createAppointment.objects.all()
    decrypted_appointments = []
    for appointment in appointments:
        decrypted_id = decrypt(appointment.doctor_id, appointment.encryption_key).decode('utf-8')

        if decrypted_id == doctor_id:
            decrypted_data = {
            'patient_id': decrypt(appointment.patient_id, appointment.encryption_key).decode('utf-8'),
            'date': appointment.date,
            'visit_type': decrypt(appointment.visit_type, appointment.encryption_key).decode('utf-8'),
            'location': decrypt(appointment.location, appointment.encryption_key).decode('utf-8'),
            'comments': decrypt(appointment.comments, appointment.encryption_key).decode('utf-8')
        }
        decrypted_appointments.append(decrypted_data)


    medicalBills = createMedicalBill.objects.all()
    decrypted_medicalBills = []
    for medicalBill in medicalBills:
        decrypted_id = decrypt(medicalBill.doctor_id_num, medicalBill.encryption_key).decode('utf-8')

        if decrypted_id == doctor_id:
            decrypted_data = {
            'patient_id_num': decrypt(medicalBill.patient_id_num, medicalBill.encryption_key).decode('utf-8'),
            'date': appointment.date,
            'service_detail': decrypt(medicalBill.service_detail, medicalBill.encryption_key).decode('utf-8'),
            'location': decrypt(medicalBill.location, medicalBill.encryption_key).decode('utf-8'),
            'payment_amount': decrypt(medicalBill.payment_amount, medicalBill.encryption_key).decode('utf-8'),
            'payment_status': decrypt(medicalBill.payment_status, medicalBill.encryption_key).decode('utf-8')
        }
        decrypted_medicalBills.append(decrypted_data)

    medications = createNewMedication.objects.all()
    decrypted_medications = []
    for medication in medications:
        decrypted_id = decrypt(medication.doctor_id_num, medication.encryption_key).decode('utf-8')

        if decrypted_id == doctor_id:
            decrypted_data = {
            'patient_id_num': decrypt(medication.patient_id_num, medication.encryption_key).decode('utf-8'),
            'medicationName': decrypt(medication.medicationName, medication.encryption_key).decode('utf-8'),
            'dose': decrypt(medication.dose, medication.encryption_key).decode('utf-8'),
            'frequency': decrypt(medication.frequency, medication.encryption_key).decode('utf-8')
        }
        decrypted_medications.append(decrypted_data)

    medicalRecords = createNewMedicalRecord.objects.all()
    decrypted_medicalRecords = []
    for medicalRecord in medicalRecords:
        decrypted_id = decrypt(medicalRecord.doctor_id_num, medicalRecord.encryption_key).decode('utf-8')

        if decrypted_id == doctor_id:
            decrypted_data = {
            'patient_id_num': decrypt(medicalRecord.patient_id_num, medicalRecord.encryption_key).decode('utf-8'),
            'patient_name': decrypt(medicalRecord.patient_name, medicalRecord.encryption_key).decode('utf-8'),
            'date': medicalRecord.date,
            'message': decrypt(medicalRecord.message, medicalRecord.encryption_key).decode('utf-8')
        }
        decrypted_medicalRecords.append(decrypted_data)

    

    context = {
        'doctor': personal_data,
        'prof': prof,
        'formatted_datetime': formatted_datetime,
        'appointments': decrypted_appointments,
        'medicalBills':  decrypted_medicalBills,
        'medications' : decrypted_medications,
        'medicalRecords' : decrypted_medicalRecords
    }
        
            
  
    if doctor_id in decrypted_list:
        return render(request, 'admin_searchUserDashboard.html',context )
    else:
        doctors = createDoctor.objects.all()
        return render(request, 'admin_searchUserDashboard.html', {'prof': prof, 'doctors': doctors, 'formatted_datetime': formatted_datetime})


def testing(request):
    prof = HospitalStaffProfile.objects.filter(user=request.user)
    return render(request, 'testing.html', {'prof' : prof})

def appointment(request):
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%I:%M %p, Today, %m/%d/%Y")
    prof = HospitalStaffProfile.objects.filter(user=request.user)
    appointments = createAppointment.objects.all()

    # Decrypt the encrypted fields in each patient object
    for appointment in appointments:
        appointment.doctor_id = decrypt_data(appointment.doctor_id, appointment.encryption_key)
        appointment.patient_id = decrypt_data(appointment.patient_id, appointment.encryption_key)
        appointment.date = appointment.date
        appointment.visit_type = decrypt_data(appointment.visit_type, appointment.encryption_key)
        appointment.location = decrypt_data(appointment.location, appointment.encryption_key)
        appointment.comments = decrypt_data(appointment.comments, appointment.encryption_key)

    return render(request, 'appointment.html', {'prof' : prof, 'appointments': appointments, 'formatted_datetime': formatted_datetime})


def doctorMedicalBill(request):
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%I:%M %p, Today, %m/%d/%Y")
    medicalBills = createMedicalBill.objects.all()

    # Decrypt the encrypted fields in each patient object
    for medicalBill in medicalBills:
        medicalBill.patient_id_num = decrypt_data(medicalBill.patient_id_num, medicalBill.encryption_key)
        medicalBill.service_detail = decrypt_data(medicalBill.service_detail, medicalBill.encryption_key)
        medicalBill.date = medicalBill.date
        medicalBill.location = decrypt_data(medicalBill.location, medicalBill.encryption_key)
        medicalBill.payment_amount = decrypt_data(medicalBill.payment_amount, medicalBill.encryption_key)
        medicalBill.payment_status = decrypt_data(medicalBill.payment_status, medicalBill.encryption_key)

    return render(request, 'doctorMedicalBill.html', {'medicalBills': medicalBills, 'formatted_datetime': formatted_datetime})


def doctorAppointment(request):
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%I:%M %p, Today, %m/%d/%Y")
    appointments = createAppointment.objects.all()

    # Decrypt the encrypted fields in each patient object
    for appointment in appointments:
        appointment.doctor_id = decrypt_data(appointment.doctor_id, appointment.encryption_key)
        appointment.patient_id = decrypt_data(appointment.patient_id, appointment.encryption_key)
        appointment.date = appointment.date
        appointment.visit_type = decrypt_data(appointment.visit_type, appointment.encryption_key)
        appointment.location = decrypt_data(appointment.location, appointment.encryption_key)
        appointment.comments = decrypt_data(appointment.comments, appointment.encryption_key)

    return render(request, 'doctorAppointment.html', {'appointments': appointments, 'formatted_datetime': formatted_datetime})


def doctorBillPayment(request):
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%I:%M %p, Today, %m/%d/%Y")

    return render(request, 'billPayment.html', {'formatted_datetime': formatted_datetime})
   

def medicalBills(request):
    prof = HospitalStaffProfile.objects.filter(user=request.user)
    appointment = patientAppointment.objects.all()
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%I:%M %p, Today, %m/%d/%Y")
    return render(request, 'medicalBills.html', {'prof' : prof, 'appointment' : appointment, 'formatted_datetime': formatted_datetime})

def medicalRecords(request):
    prof = HospitalStaffProfile.objects.filter(user=request.user)
    appointment = patientAppointment.objects.all()
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%I:%M %p, Today, %m/%d/%Y")
    return render(request, 'medicalRecords.html', {'prof' : prof, 'appointment' : appointment, 'formatted_datetime': formatted_datetime})

def medications(request):
    prof = HospitalStaffProfile.objects.filter(user=request.user)
    appointment = patientAppointment.objects.all()
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%I:%M %p, Today, %m/%d/%Y")
    return render(request, 'medications.html', {'prof' : prof, 'appointment' : appointment, 'formatted_datetime': formatted_datetime})

def adminDashboard(request):
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%I:%M %p, Today, %m/%d/%Y")
    prof = HospitalStaffProfile.objects.filter(user=request.user)
    appointment = patientAppointment.objects.order_by('-id')[:5]
    medicalRecords = patientMedicalRecords.objects.order_by('-id')[:2]
    medicalBills = patientMedicalBills.objects.order_by('-id')[:2]
    medications = patientMedications.objects.order_by('-id')[:2]
    return render(request, 'adminDashboard.html', {'prof' : prof, 'appointment' : appointment, 'medicalRecords' : medicalRecords, 'medicalBills' : medicalBills, 'medications' : medications, 'formatted_datetime': formatted_datetime})


