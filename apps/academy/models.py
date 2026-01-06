from django.db import models
from django.urls import reverse
from django.conf import settings


class CourseCategory(models.Model):
    """교육 과정 카테고리"""

    name = models.CharField('카테고리명', max_length=50)
    slug = models.SlugField('슬러그', unique=True, allow_unicode=True)
    description = models.CharField('설명', max_length=200, blank=True)
    order = models.PositiveIntegerField('순서', default=0)

    class Meta:
        verbose_name = '과정 카테고리'
        verbose_name_plural = '과정 카테고리 목록'
        ordering = ['order']

    def __str__(self):
        return self.name


class Course(models.Model):
    """교육 과정"""

    category = models.ForeignKey(
        CourseCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='courses',
        verbose_name='카테고리'
    )
    title = models.CharField('과정명', max_length=100)
    subtitle = models.CharField('부제목', max_length=200, blank=True)
    thumbnail = models.ImageField('대표이미지', upload_to='academy/courses/')

    # 과정 정보
    duration = models.CharField('기간', max_length=50)
    schedule = models.CharField('일정', max_length=100)
    start_date = models.DateField('개강일')
    end_date = models.DateField('종강일', null=True, blank=True)
    location = models.CharField('장소', max_length=100, blank=True)
    max_students = models.PositiveIntegerField('정원')
    current_students = models.PositiveIntegerField('현재 신청인원', default=0)

    # 가격
    price = models.PositiveIntegerField('정가')
    discount_price = models.PositiveIntegerField('할인가', null=True, blank=True)

    # 상세 내용
    description = models.TextField('과정 소개')
    curriculum = models.JSONField('커리큘럼', default=list)
    target_audience = models.TextField('대상 수강생')
    benefits = models.TextField('수강 혜택', blank=True)

    # 상태
    is_active = models.BooleanField('활성화', default=True)
    is_enrolling = models.BooleanField('모집중', default=True)

    created_at = models.DateTimeField('등록일', auto_now_add=True)

    class Meta:
        verbose_name = '교육 과정'
        verbose_name_plural = '교육 과정 목록'
        ordering = ['-start_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('academy:course_detail', kwargs={'pk': self.pk})

    @property
    def display_price(self):
        """표시 가격"""
        return self.discount_price if self.discount_price else self.price

    @property
    def is_full(self):
        """정원 초과 여부"""
        return self.current_students >= self.max_students

    @property
    def remaining_seats(self):
        """잔여석"""
        return max(0, self.max_students - self.current_students)


class Instructor(models.Model):
    """강사"""

    name = models.CharField('이름', max_length=50)
    photo = models.ImageField('사진', upload_to='academy/instructors/')
    title = models.CharField('직함', max_length=100)
    bio = models.TextField('소개')
    specialties = models.CharField('전문분야', max_length=200)
    teaching_history = models.TextField('강의 이력', blank=True)
    order = models.PositiveIntegerField('순서', default=0)
    is_active = models.BooleanField('활성화', default=True)

    class Meta:
        verbose_name = '강사'
        verbose_name_plural = '강사 목록'
        ordering = ['order']

    def __str__(self):
        return f'{self.name} ({self.title})'


class Enrollment(models.Model):
    """수강 신청"""

    PAYMENT_METHOD_CHOICES = [
        ('card', '신용카드'),
        ('bank', '계좌이체'),
        ('installment', '분할결제'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', '결제대기'),
        ('completed', '결제완료'),
        ('cancelled', '결제취소'),
        ('refunded', '환불완료'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='회원'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='과정'
    )

    # 신청자 정보
    name = models.CharField('이름', max_length=50)
    phone = models.CharField('연락처', max_length=20)
    email = models.EmailField('이메일')

    # 결제 정보
    payment_method = models.CharField(
        '결제방법',
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES
    )
    payment_status = models.CharField(
        '결제상태',
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )
    payment_amount = models.PositiveIntegerField('결제금액')
    paid_at = models.DateTimeField('결제일', null=True, blank=True)

    created_at = models.DateTimeField('신청일', auto_now_add=True)

    class Meta:
        verbose_name = '수강신청'
        verbose_name_plural = '수강신청 목록'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.course.title}'


class FreeLecture(models.Model):
    """무료 강좌"""

    title = models.CharField('제목', max_length=100)
    description = models.TextField('설명')
    video_url = models.URLField('영상 URL', help_text='유튜브 URL')
    thumbnail = models.ImageField('썸네일', upload_to='academy/free/')
    duration = models.CharField('영상길이', max_length=20)
    order = models.PositiveIntegerField('순서', default=0)
    view_count = models.PositiveIntegerField('조회수', default=0)
    is_active = models.BooleanField('활성화', default=True)

    class Meta:
        verbose_name = '무료 강좌'
        verbose_name_plural = '무료 강좌 목록'
        ordering = ['order']

    def __str__(self):
        return self.title


class CourseReview(models.Model):
    """수강 후기"""

    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    enrollment = models.OneToOneField(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='수강정보'
    )
    rating = models.PositiveIntegerField('평점', choices=RATING_CHOICES, default=5)
    content = models.TextField('후기 내용')
    is_approved = models.BooleanField('승인', default=False)
    created_at = models.DateTimeField('작성일', auto_now_add=True)

    class Meta:
        verbose_name = '수강 후기'
        verbose_name_plural = '수강 후기 목록'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.enrollment.user.username} - {self.enrollment.course.title}'
