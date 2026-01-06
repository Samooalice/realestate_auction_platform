from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Consultation
from .forms import ConsultationForm


def consultation_form(request):
    """상담 신청 폼"""
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save()
            messages.success(request, '상담 신청이 접수되었습니다. 빠른 시일 내에 연락드리겠습니다.')
            return redirect('consultation:complete')
    else:
        form = ConsultationForm()

    context = {
        'form': form,
    }
    return render(request, 'consultation/form.html', context)


def consultation_complete(request):
    """상담 신청 완료"""
    return render(request, 'consultation/complete.html')
