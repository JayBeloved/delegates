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
    # Add other URL patterns here
]