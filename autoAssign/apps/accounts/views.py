# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .forms import LoginForm, CustomUserCreationForm #SignUpForm


def home_view(request):
    return HttpResponseRedirect(reverse('login'))

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("core:dashboard")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
@user_passes_test(lambda u: u.is_superuser)  # Only superusers can create users
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.role = form.cleaned_data['role']  # Save the role
            user.save()
            messages.success(request, 'User created successfully.')
            return redirect(reverse('core:dashboard'))  # Redirect to the delegates list
        else:
            messages.error(request, 'There was an error creating the user.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/create_user.html', {'form': form})