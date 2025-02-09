import random
import datetime
import pandas as pd
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, user_passes_test
from decouple import config
from django.core.management import call_command
from .forms import UploadForm, PaymentForm, DelegateForm
from .models import Delegate, Committee, Assignment, Payment


# Define role-based access control functions
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def is_finance(user):
    return user.is_authenticated and user.role == 'finance'

def is_delegates_affairs(user):
    return user.is_authenticated and user.role == 'delegates_affairs'


# Create your views here.
@login_required
def dashboard(request):
    total_delegates = Delegate.objects.count()
    assigned_delegates = Assignment.objects.count()
    paid_delegates = Payment.objects.filter(verified=True).count()
    recent_assignments = Assignment.objects.order_by('-id')[:10]
    percentage_paid = (paid_delegates / total_delegates) * 100 if total_delegates > 0 else 0

    context = {
        'total_delegates': total_delegates,
        'assigned_delegates': assigned_delegates,
        'paid_delegates': paid_delegates,
        'recent_assignments': recent_assignments,
        'current_date': datetime.datetime.now(),
        'percentage_paid': round(percentage_paid, 4)
    }

    return render(request, 'core/dashboard.html', context)

@login_required
@user_passes_test(lambda user: is_admin(user) or is_delegates_affairs(user))
def assignment_list(request):
    query = request.GET.get('q')
    if query:
        assignments = Assignment.objects.filter(delegate__name__icontains=query) | Assignment.objects.filter(delegate__email__icontains=query)
    else:
        assignments = Assignment.objects.all()
    paginator = Paginator(assignments, 10)  # Show 10 assignments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/assignment_list.html', {'page_obj': page_obj, 'query': query})

@login_required
def all_delegates_list(request):
    query = request.GET.get('q')
    if query:
        delegates = Delegate.objects.filter(name__icontains=query) | Delegate.objects.filter(email__icontains=query)
    else:
        delegates = Delegate.objects.all()
    
    # Check if the delegate has paid
    paid_delegate_ids = Payment.objects.filter(verified=True).values_list('delegate_id', flat=True)
    for delegate in delegates:
        delegate.has_paid = delegate.id in paid_delegate_ids

    paginator = Paginator(delegates, 10)  # Show 10 delegates per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'title': 'All Delegates',
        'description': 'Here is a list of all delegates',
        'query': query
    }
    return render(request, 'core/delegates_list.html', context)

@login_required
def paid_delegates(request):
    query = request.GET.get('q')
    paid_delegate_ids = Payment.objects.filter(verified=True).values_list('delegate_id', flat=True)
    if query:
        delegates = Delegate.objects.filter(id__in=paid_delegate_ids).filter(name__icontains=query) | Delegate.objects.filter(id__in=paid_delegate_ids).filter(email__icontains=query)
    else:
        delegates = Delegate.objects.filter(id__in=paid_delegate_ids)
    paginator = Paginator(delegates, 10)  # Show 10 delegates per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'title': 'Paid Delegates',
        'description': 'Here is a list of all paid delegates',
        'query': query
    }
    return render(request, 'core/delegates_list.html', context)


@login_required
def verify_payment(request, delegate_id):
    delegate = get_object_or_404(Delegate, id=delegate_id)
    payment = Payment.objects.filter(delegate=delegate).first()  # Get existing payment if it exists

    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)  # Use existing payment as instance if available
        if form.is_valid():
            payment = form.save(commit=False)
            payment.delegate = delegate
            payment.verified = True  # Mark as verified upon any update
            payment.save()
            delegate.has_paid = True
            delegate.save()
            messages.success(request, 'Payment details updated successfully.')
            return redirect(reverse('core:all_delegates'))
        else:
            messages.error(request, 'There was an error updating the payment details.')
    else:
        form = PaymentForm(instance=payment)  # Populate form with existing payment data if available

    return render(request, 'core/verify_payment.html', {'form': form, 'delegate': delegate})


@login_required
def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File is not a CSV type')
                return render(request, 'core/upload_form.html', {'form': form})

            try:
                df = pd.read_csv(csv_file)
                
                # Process delegate data (existing functionality)
                process_delegate_data(df)
                process_committee_data(df)

                # Process payment verification
                verify_payments_from_csv(df)

                messages.success(request, 'Data uploaded and action successfully carried out.')
                return redirect('core:all_delegates')

            except Exception as e:
                messages.error(request, f"Error processing file: {e}")
                return render(request, 'core/upload_form.html', {'form': form})
        else:
            messages.error(request, 'Invalid form data.')
            return render(request, 'core/upload_form.html', {'form': form})
    else:
        form = UploadForm()
        return render(request, 'core/upload_form.html', {'form': form})

def get_payment_method_value(payment_method_label):
    for value, label in Payment.PAYMENT_METHOD_CHOICES:
        if label.lower() == payment_method_label.lower():
            return value
    return 'Unknown'  # Default value if no match is found

def get_amount_value(amount_label):
    for value, label in Payment.AMOUNT_CHOICES:
        if label.lower() == amount_label.lower():
            return value
    return 'Unknown'  # Default value if no match is found

def verify_payments_from_csv(df):
    for index, row in df.iterrows():
        email = row.get('MAILS')  # Assuming 'MAILS' is the column name for email
        amount = row.get('AMOUNT')
        payment_method = row.get('PAYMENT METHOD')

        if not email:
            continue  # Skip if email is missing

        try:
            delegate = Delegate.objects.get(email=email)
            payment = Payment.objects.filter(delegate=delegate).first()

            validated_payment_method = get_payment_method_value(payment_method)
            validated_amount = get_amount_value(amount)

            if payment:
                payment.payment_method = validated_payment_method if pd.notna(validated_payment_method) else payment.payment_method
                payment.amount = validated_amount if pd.notna(validated_amount) else payment.amount
                payment.verified = True
                payment.save()
            else:
                payment = Payment.objects.create(
                    delegate=delegate,
                    payment_method=validated_payment_method if pd.notna(validated_payment_method) else 'Unknown',
                    amount=validated_amount if pd.notna(validated_amount) else 'Unknown',
                    verified=True
                )

            delegate.has_paid = True
            delegate.save()

        except Delegate.DoesNotExist:
            print(f"Delegate with email {email} not found.")
            continue  # Skip if delegate is not found


COMMITTEE_MAPPING = {
    "1": "United Nations Security Council (UNSC)",
    "2": "International Court of Justice (ICJ)",
    "3": "United Nations Economic Commission for Africa (UNECA)",
    "4": "Disarmament and International Security (DISEC)",
    "5": "Economic and Financial (ECOFIN)",
    "6": "Social, Humanitarian and Cultural Committee (SOCHUM)",
    "7": "Special, Political and Decolonization (SPECPOL)",
    "8": "United Nations Economic Commission for Europe (UNECE)",
    "9": "UN Legal",
}

def process_delegate_data(data):
    if "name" not in data.columns:
        return
    for index, row in data.iterrows():
        committee1_id = row.get('committee1', '')
        committee2_id = row.get('committee2', '')
        committee3_id = row.get('committee3', '')

        committee1_name = COMMITTEE_MAPPING.get(str(committee1_id), committee1_id)
        committee2_name = COMMITTEE_MAPPING.get(str(committee2_id), committee2_id)
        committee3_name = COMMITTEE_MAPPING.get(str(committee3_id), committee3_id)

        Enrollment_data = {
            'user_id': row.get('id'),
            'name': row.get('name'),
            'email': row.get('email'),
            'phone': row.get('phone'),
            'delegate_type': row.get('delegate_type'),
            'gender': row.get('gender'),
            'mun_experience': row.get('mun_experience'),
            'affiliation': row.get('affiliation'),
            'position': row.get('position'),
            'department': row.get('department'),
            'matric_num': row.get('matric_num'),
            'city': row.get('city'),
            'state': row.get('state'),
            'country': row.get('country'),
            'zipcode': row.get('zipcode'),
            'advert': row.get('advert'),
            'tshirt_size': row.get('tshirt_size'),
            'medical': row.get('medical'),
            'diet': row.get('diet'),
            'referral': row.get('referral'),
            'committee1': committee1_name,
            'country1': row.get('country1'),
            'committee2': committee2_name,
            'country2': row.get('country2'),
            'committee3': committee3_name,
            'country3': row.get('country3'),
            'code': row.get('code'),
            'token': row.get('token'),
            'status': 'Unassigned',  # All data are unassigned by default
            'captured': row.get('captured') if pd.notna(row.get('captured')) else '2025-02-07'  # Default if empty
        }
        Enrollment_data = {k: v for k, v in Enrollment_data.items() if pd.notna(v)}
        Delegate.objects.update_or_create(user_id=row.get('id'), defaults=Enrollment_data)
def process_committee_data(data):
    if "committee" not in data.columns or "country" not in data.columns:
        return

    for index, row in data.iterrows():
        committee_data = {
            "committee": row.get('committee'),
            "countries": row.get('country')
        }
        Committee.objects.update_or_create(committee=row.get('committee'), defaults=committee_data)


@login_required
def assign_delegate(request, delegate_id):
    delegate = get_object_or_404(Delegate, id=delegate_id)
    committees = Committee.objects.all()

    if request.method == 'POST':
        committee_name = request.POST.get('committee')
        country = request.POST.get('country')
        preference = request.POST.get('preference')

        # Check if the committee and country combination is already assigned to another delegate
        if Assignment.objects.filter(committee=committee_name, country=country).exclude(delegate=delegate).exists():
            messages.error(request, 'This committee and country combination is already assigned to another delegate.')
        else:
            # Get or create the assignment for the delegate
            assignment, created = Assignment.objects.update_or_create(
                delegate=delegate,
                defaults={'committee': committee_name, 'country': country, 'preference': preference}
            )
            delegate.status = 'Assigned'
            delegate.save()
            messages.success(request, 'Delegate assigned successfully.')
            
            # Send email to the delegate
            subject = 'RUIMUN 2025 - Assignment Details'
            context = {
                'delegate': delegate,
                'committee': committee_name,
                'country': country,
                'whatsapp_group_link': 'https://chat.whatsapp.com/IvIaqagrsxb956nFIRko7F',  # Replace with your actual WhatsApp group link
            }
            html_message = render_to_string('core/assignment_email.html', context)

            email = EmailMessage(
                subject=subject,
                body=html_message,
                from_email='contact.johnjlawal@gmail.com',  # Replace with your sending email address
                to=[delegate.email],
            )
            email.content_subtype = "html"  # Set content type to HTML
            email.send(fail_silently=True)

            return HttpResponseRedirect(reverse('core:paid_delegates'))

    context = {
        'delegate': delegate,
        'committees': committees,
    }
    return render(request, 'core/assign_delegate.html', context)


@login_required
def update_delegate(request, delegate_id):
    delegate = get_object_or_404(Delegate, id=delegate_id)
    if request.method == 'POST':
        form = DelegateForm(request.POST, instance=delegate)
        if form.is_valid():
            form.save()
            messages.success(request, 'Delegate details updated successfully.')
            return redirect(reverse('core:all_delegates'))  # Redirect to the delegates list
        else:
            messages.error(request, 'There was an error updating the delegate details.')
    else:
        form = DelegateForm(instance=delegate)
    return render(request, 'core/update_delegate.html', {'form': form, 'delegate': delegate})


def test_email(request):
    subject = 'Test Email'
    message = 'This is a test email.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['info.jaybeloved@gmail.com']  # Replace with your email address

    try:
        send_mail(subject, message, from_email, recipient_list)
        return HttpResponse('Email sent successfully.')
    except Exception as e:
        return HttpResponse(f'Error sending email: {e}')