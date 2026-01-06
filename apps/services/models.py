from django.db import models
from django.urls import reverse


class ServiceCategory(models.Model):
    """서비스 카테고리 (5대 서비스)"""

    name = models.CharField('서비스명', max_length=50)
    slug = models.SlugField('슬러그', unique=True, allow_unicode=True)
    icon = models.CharField('아이콘 클래스', max_length=50, blank=True)
    short_description = models.CharField('간단 설명', max_length=200)
    order = models.PositiveIntegerField('순서', default=0)
    is_active = models.BooleanField('활성화', default=True)

    class Meta:
        verbose_name = '서비스 카테고리'
        verbose_name_plural = '서비스 카테고리 목록'
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('services:detail', kwargs={'slug': self.slug})


class Service(models.Model):
    """서비스 상세 정보"""

    category = models.OneToOneField(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name='detail',
        verbose_name='카테고리'
    )
    hero_image = models.ImageField('대표 이미지', upload_to='services/')
    overview = models.TextField('서비스 개요')
    target_properties = models.TextField('대상 부동산')
    target_customers = models.TextField('대상 고객')
    process_steps = models.JSONField('업무 프로세스', default=list)
    checkpoints = models.TextField('핵심 체크포인트')
    benefits = models.TextField('서비스 혜택', blank=True)

    class Meta:
        verbose_name = '서비스 상세'
        verbose_name_plural = '서비스 상세 목록'

    def __str__(self):
        return f'{self.category.name} 상세'


class PricingPlan(models.Model):
    """서비스 요금제"""

    PRICE_TYPE_CHOICES = [
        ('fixed', '정액제'),
        ('rate', '정률제'),
        ('mixed', '정률+성공보수'),
        ('annual', '연간 계약제'),
    ]

    name = models.CharField('요금제명', max_length=50)
    description = models.TextField('설명')
    price_type = models.CharField(
        '요금 유형',
        max_length=20,
        choices=PRICE_TYPE_CHOICES
    )
    price_display = models.CharField('요금 표시', max_length=100)
    features = models.JSONField('서비스 내용', default=list)
    target_customers = models.CharField('대상 고객', max_length=200)
    is_popular = models.BooleanField('인기 요금제', default=False)
    order = models.PositiveIntegerField('순서', default=0)

    class Meta:
        verbose_name = '요금제'
        verbose_name_plural = '요금제 목록'
        ordering = ['order']

    def __str__(self):
        return self.name


class ProcessStep(models.Model):
    """컨설팅 프로세스 단계"""

    step_number = models.PositiveIntegerField('단계 번호')
    title = models.CharField('단계명', max_length=100)
    description = models.TextField('설명')
    icon = models.CharField('아이콘', max_length=50, blank=True)

    class Meta:
        verbose_name = '프로세스 단계'
        verbose_name_plural = '프로세스 단계 목록'
        ordering = ['step_number']

    def __str__(self):
        return f'{self.step_number}. {self.title}'
