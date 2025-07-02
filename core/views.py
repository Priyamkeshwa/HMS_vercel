from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Patient, Prescription, DoctorRemark
from django import forms
from django.http import HttpResponse
from mimetypes import guess_type

# Forms
class PatientRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Patient
        fields = []

class PrescriptionUploadForm(forms.Form):
    file = forms.FileField()

class DoctorRemarkForm(forms.ModelForm):
    class Meta:
        model = DoctorRemark
        fields = ['remark']

# Views

def patient_register(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            Patient.objects.create(user=user)
            return redirect('login')
    else:
        form = PatientRegistrationForm()
    return render(request, 'core/patient_register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if hasattr(user, 'patient'):
                return redirect('patient_dashboard')
            elif user.is_staff:
                return redirect('doctor_dashboard')
        else:
            return render(request, 'core/login.html', {'error': 'Invalid credentials'})
    return render(request, 'core/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def patient_dashboard(request):
    try:
        patient = request.user.patient
    except Exception:
        return render(request, 'core/no_patient.html')
    prescriptions = patient.prescriptions.all()
    return render(request, 'core/patient_dashboard.html', {'prescriptions': prescriptions})

@login_required
def upload_prescription(request):
    if request.method == 'POST':
        form = PrescriptionUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            patient = request.user.patient
            Prescription.objects.create(
                patient=patient,
                file_name=uploaded_file.name,
                file_data=uploaded_file.read(),
            )
            return redirect('patient_dashboard')
    else:
        form = PrescriptionUploadForm()
    return render(request, 'core/upload_prescription.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def doctor_dashboard(request):
    prescriptions = Prescription.objects.all()
    pending_count = prescriptions.filter(status='pending').count()
    done_count = prescriptions.filter(status='done').count()
    return render(request, 'core/doctor_dashboard.html', {
        'prescriptions': prescriptions,
        'pending_count': pending_count,
        'done_count': done_count,
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def add_remark(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    if hasattr(prescription, 'remark'):
        return redirect('doctor_dashboard')
    if request.method == 'POST':
        form = DoctorRemarkForm(request.POST)
        if form.is_valid():
            remark = form.save(commit=False)
            remark.prescription = prescription
            remark.doctor = request.user
            remark.save()
            prescription.status = 'done'
            prescription.save()
            return redirect('doctor_dashboard')
    else:
        form = DoctorRemarkForm()
    return render(request, 'core/add_remark.html', {'form': form, 'prescription': prescription})

@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_remark(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    if not hasattr(prescription, 'remark'):
        return redirect('doctor_dashboard')
    remark = prescription.remark
    if request.method == 'POST':
        form = DoctorRemarkForm(request.POST, instance=remark)
        if form.is_valid():
            form.save()
            prescription.status = 'done'
            prescription.save()
            return redirect('doctor_dashboard')
    else:
        form = DoctorRemarkForm(instance=remark)
    # Optionally allow reverting status to 'pending'
    if request.GET.get('revert') == '1':
        prescription.status = 'pending'
        prescription.save()
        # Optionally, you could also delete the remark here if you want a full revert
        # remark.delete()
        return redirect('doctor_dashboard')
    return render(request, 'core/edit_remark.html', {'form': form, 'prescription': prescription})

def home(request):
    return redirect('login')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('doctor_dashboard')
        else:
            return render(request, 'core/admin_login.html', {'error': 'Invalid admin credentials'})
    return render(request, 'core/admin_login.html')

def download_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    # Guess content type from file name
    content_type, _ = guess_type(prescription.file_name)
    if not content_type:
        content_type = 'application/octet-stream'
    response = HttpResponse(prescription.file_data, content_type=content_type)
    # Use 'inline' to display in browser if possible
    response['Content-Disposition'] = f'inline; filename="{prescription.file_name}"'
    return response
