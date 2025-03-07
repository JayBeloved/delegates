from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('assignments/', views.assignment_list, name='assignment_list'),
    path('upload/', views.upload, name='upload'),
    path('all_delegates/', views.all_delegates_list, name='all_delegates'),
    path('unverified_delegates/', views.unverified_delegates, name='unverified_delegates'),
    path('paid_unassigned_delegates/', views.paid_unassigned_delegates, name='paid_unassigned_delegates'),
    path('paid_assigned_delegates/', views.paid_assigned_delegates, name='paid_assigned_delegates'),
    # path('paid-delegates/', views.paid_delegates, name='paid_delegates'),
    path('verify_payment/<int:delegate_id>/', views.verify_payment, name='verify_payment'),
    path('assign_delegate/<int:delegate_id>/', views.assign_delegate, name='assign_delegate'),
    path('update_delegate/<int:delegate_id>/', views.update_delegate, name='update_delegate'), 
    path('test_email/', views.test_email, name='test_email'),  # Add this line
    path('register_delegate/', views.register_delegate, name='register_delegate'),
    path('registration_success/', views.registration_success, name='registration_success'),
   path('assignment_report_form/', views.assignment_report_form, name='assignment_report_form'),
    path('generate_assignment_pdf/', views.generate_assignment_pdf, name='generate_assignment_pdf'),
    # Add other URL patterns here
]