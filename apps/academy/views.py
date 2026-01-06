from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import CourseCategory, Course, Instructor, Enrollment, FreeLecture
from .forms import EnrollmentForm


def course_list(request):
    """교육 과정 목록"""
    courses = Course.objects.filter(is_active=True)

    # 필터링
    category = request.GET.get('category')
    if category:
        courses = courses.filter(category__slug=category)

    enrolling_only = request.GET.get('enrolling')
    if enrolling_only:
        courses = courses.filter(is_enrolling=True)

    context = {
        'courses': courses,
        'categories': CourseCategory.objects.all(),
    }
    return render(request, 'academy/list.html', context)


def course_detail(request, pk):
    """교육 과정 상세"""
    course = get_object_or_404(Course, pk=pk, is_active=True)

    already_enrolled = False
    if request.user.is_authenticated:
        already_enrolled = Enrollment.objects.filter(
            user=request.user, course=course
        ).exists()

    reviews = course.enrollments.filter(
        review__is_approved=True
    ).select_related('review')[:5]

    context = {
        'course': course,
        'already_enrolled': already_enrolled,
        'reviews': reviews,
        'instructors': Instructor.objects.filter(is_active=True)[:3],
    }
    return render(request, 'academy/detail.html', context)


@login_required
def enroll(request, pk):
    """수강 신청"""
    course = get_object_or_404(Course, pk=pk, is_active=True, is_enrolling=True)

    if course.is_full:
        messages.error(request, '정원이 마감되었습니다.')
        return redirect('academy:course_detail', pk=pk)

    if Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.warning(request, '이미 신청한 과정입니다.')
        return redirect('academy:course_detail', pk=pk)

    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.user = request.user
            enrollment.course = course
            enrollment.payment_amount = course.display_price
            enrollment.save()

            course.current_students += 1
            course.save(update_fields=['current_students'])

            messages.success(request, '수강 신청이 완료되었습니다.')
            return redirect('academy:my_courses')
    else:
        form = EnrollmentForm(initial={
            'name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
            'phone': getattr(request.user, 'phone', ''),
        })

    context = {
        'course': course,
        'form': form,
    }
    return render(request, 'academy/enroll.html', context)


def instructor_list(request):
    """강사 소개"""
    context = {
        'instructors': Instructor.objects.filter(is_active=True),
    }
    return render(request, 'academy/instructors.html', context)


def free_lecture_list(request):
    """무료 강좌 목록"""
    lectures = FreeLecture.objects.filter(is_active=True)

    paginator = Paginator(lectures, 9)
    page = request.GET.get('page', 1)
    lectures = paginator.get_page(page)

    context = {
        'lectures': lectures,
    }
    return render(request, 'academy/free_lectures.html', context)


@login_required
def my_courses(request):
    """내 수강 목록"""
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course')

    context = {
        'enrollments': enrollments,
    }
    return render(request, 'academy/my_courses.html', context)
