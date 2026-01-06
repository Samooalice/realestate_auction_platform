from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, UserProfile


class SignUpForm(UserCreationForm):
    """회원가입 폼"""
    email = forms.EmailField(required=True, label='이메일')
    phone = forms.CharField(max_length=20, required=True, label='연락처')
    marketing_agreed = forms.BooleanField(required=False, label='마케팅 수신 동의')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'password1', 'password2', 'marketing_agreed']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class LoginForm(forms.Form):
    """로그인 폼"""
    username = forms.CharField(label='아이디', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ProfileForm(forms.ModelForm):
    """사용자 정보 수정 폼"""
    class Meta:
        model = CustomUser
        fields = ['email', 'phone']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserProfileForm(forms.ModelForm):
    """사용자 프로필 폼"""
    class Meta:
        model = UserProfile
        fields = ['preferred_region', 'budget_range', 'interest_type']
        widgets = {
            'preferred_region': forms.TextInput(attrs={'class': 'form-control'}),
            'budget_range': forms.Select(attrs={'class': 'form-select'}),
            'interest_type': forms.Select(attrs={'class': 'form-select'}),
        }
