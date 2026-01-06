from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, UserProfile
from .forms import SignUpForm, LoginForm, ProfileForm, UserProfileForm


def signup(request):
    """회원가입"""
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, '회원가입이 완료되었습니다.')
            return redirect('core:home')
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    """로그인"""
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                next_url = request.GET.get('next', 'core:home')
                return redirect(next_url)
            else:
                messages.error(request, '아이디 또는 비밀번호가 올바르지 않습니다.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """로그아웃"""
    logout(request)
    messages.info(request, '로그아웃되었습니다.')
    return redirect('core:home')


@login_required
def profile(request):
    """마이페이지"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    context = {
        'profile': profile,
        'enrollments': request.user.enrollments.all()[:5],
        'bookmarks': request.user.bookmarks.all()[:5],
        'consultations': request.user.assigned_consultations.all()[:5] if hasattr(request.user, 'assigned_consultations') else [],
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_edit(request):
    """프로필 수정"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = ProfileForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '프로필이 수정되었습니다.')
            return redirect('accounts:profile')
    else:
        user_form = ProfileForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/profile_edit.html', context)
