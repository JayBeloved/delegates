from django import forms
from .models import Payment, Delegate

class UploadForm(forms.Form):
    file = forms.FileField()

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method', 'amount']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-control form-select'}),
            'amount': forms.Select(attrs={'class': 'form-control form-select'}),
        }


class DelegateForm(forms.ModelForm):
    class Meta:
        model = Delegate
        fields = ['name', 'email', 'phone', 'delegate_type', 'gender', 'mun_experience', 'affiliation', 'position', 'department', 'matric_num', 'city', 'state', 'country', 'zipcode', 'advert', 'tshirt_size', 'medical', 'diet', 'referral', 'status']
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-control form-select'}),
            'delegate_type': forms.Select(attrs={'class': 'form-control form-select'}),
            'mun_experience': forms.Textarea(attrs={'class': 'form-control'}),
            'affiliation': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'matric_num': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'advert': forms.TextInput(attrs={'class': 'form-control form-select'}),
            'tshirt_size': forms.Select(attrs={'class': 'form-control form-select'}),
            'medical': forms.Textarea(attrs={'class': 'form-control'}),
            'diet': forms.Textarea(attrs={'class': 'form-control'}),
            'referral': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }