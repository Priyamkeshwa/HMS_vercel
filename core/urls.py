from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.patient_register, name='patient_register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('patient/upload/', views.upload_prescription, name='upload_prescription'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/remark/<int:prescription_id>/', views.add_remark, name='add_remark'),
    path('doctor/remark/<int:prescription_id>/edit/', views.edit_remark, name='edit_remark'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('prescription/<int:prescription_id>/download/', views.download_prescription, name='download_prescription'),
] 