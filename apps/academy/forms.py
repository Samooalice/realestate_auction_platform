from django import forms
from .models import Enrollment


class EnrollmentForm(forms.ModelForm):
    """수강 신청 폼"""
    class Meta:
        model = Enrollment
        fields = ['name', 'phone', 'email', 'payment_method']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
        }
