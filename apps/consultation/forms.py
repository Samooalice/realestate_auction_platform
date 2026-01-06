from django import forms
from .models import Consultation


class ConsultationForm(forms.ModelForm):
    """상담 신청 폼"""
    privacy_agreed = forms.BooleanField(
        required=True,
        label='개인정보 수집 및 이용에 동의합니다',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Consultation
        fields = [
            'name', 'phone', 'email', 'service_type',
            'budget_range', 'preferred_region', 'message',
            'privacy_agreed', 'marketing_agreed'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '홍길동'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '010-0000-0000'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@email.com'}),
            'service_type': forms.Select(attrs={'class': 'form-select'}),
            'budget_range': forms.Select(attrs={'class': 'form-select'}),
            'preferred_region': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '서울 강남구'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': '상담받고 싶은 내용을 자유롭게 작성해주세요.'}),
            'marketing_agreed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
