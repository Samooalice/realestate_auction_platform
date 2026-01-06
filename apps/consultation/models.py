from django.db import models
from django.conf import settings


class Consultation(models.Model):
    """상담 신청"""

    SERVICE_TYPE_CHOICES = [
        ('home_buying', '내집마련 컨설팅'),
        ('redevelopment', '재개발/재건축 투자'),
        ('rental_income', '임대수익형 투자'),
        ('company_building', '사옥마련 컨설팅'),
        ('senior_facility', '노유자시설 컨설팅'),
    ]

    BUDGET_CHOICES = [
        ('under_1', '1억 이하'),
        ('1_to_3', '1~3억'),
        ('3_to_5', '3~5억'),
        ('5_to_10', '5~10억'),
        ('over_10', '10억 이상'),
    ]

    STATUS_CHOICES = [
        ('pending', '접수대기'),
        ('contacted', '연락완료'),
        ('in_progress', '상담중'),
        ('completed', '상담완료'),
        ('contracted', '계약완료'),
        ('cancelled', '취소'),
    ]

    # 신청자 정보
    name = models.CharField('이름', max_length=50)
    phone = models.CharField('연락처', max_length=20)
    email = models.EmailField('이메일', blank=True)

    # 상담 내용
    service_type = models.CharField(
        '상담분야',
        max_length=30,
        choices=SERVICE_TYPE_CHOICES
    )
    budget_range = models.CharField(
        '예산범위',
        max_length=20,
        choices=BUDGET_CHOICES,
        blank=True
    )
    preferred_region = models.CharField('희망지역', max_length=100, blank=True)
    message = models.TextField('문의내용', blank=True)

    # 동의
    privacy_agreed = models.BooleanField('개인정보 수집동의', default=True)
    marketing_agreed = models.BooleanField('마케팅 수신동의', default=False)

    # 처리 상태
    status = models.CharField(
        '상태',
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_consultations',
        verbose_name='담당자'
    )
    admin_memo = models.TextField('관리자 메모', blank=True)

    # 타임스탬프
    created_at = models.DateTimeField('신청일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)
    contacted_at = models.DateTimeField('연락일', null=True, blank=True)

    class Meta:
        verbose_name = '상담신청'
        verbose_name_plural = '상담신청 목록'
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.get_status_display()}] {self.name} - {self.get_service_type_display()}'
