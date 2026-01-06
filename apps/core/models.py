from django.db import models


class HeroBanner(models.Model):
    """메인 히어로 배너"""

    title = models.CharField('제목', max_length=100)
    subtitle = models.CharField('부제목', max_length=200, blank=True)
    description = models.TextField('설명', blank=True)
    image = models.ImageField('배너 이미지', upload_to='banners/')
    link_url = models.URLField('링크 URL', blank=True)
    link_text = models.CharField('버튼 텍스트', max_length=50, default='자세히 보기')
    order = models.PositiveIntegerField('순서', default=0)
    is_active = models.BooleanField('활성화', default=True)
    created_at = models.DateTimeField('생성일', auto_now_add=True)

    class Meta:
        verbose_name = '히어로 배너'
        verbose_name_plural = '히어로 배너 목록'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


class SiteStatistics(models.Model):
    """사이트 통계 (메인페이지 핵심 수치)"""

    total_consultations = models.PositiveIntegerField('총 컨설팅 건수', default=0)
    total_winning_amount = models.BigIntegerField('누적 낙찰액', default=0)
    total_customers = models.PositiveIntegerField('총 고객 수', default=0)
    success_rate = models.DecimalField('성공률', max_digits=5, decimal_places=2, default=0)
    updated_at = models.DateTimeField('업데이트일', auto_now=True)

    class Meta:
        verbose_name = '사이트 통계'
        verbose_name_plural = '사이트 통계'

    def __str__(self):
        return f'사이트 통계 (최종 업데이트: {self.updated_at})'

    @property
    def winning_amount_display(self):
        """억원 단위로 표시"""
        return f'{self.total_winning_amount / 100000000:.0f}억'


class Partner(models.Model):
    """협력사/제휴사 로고"""

    name = models.CharField('협력사명', max_length=100)
    logo = models.ImageField('로고', upload_to='partners/')
    website = models.URLField('웹사이트', blank=True)
    order = models.PositiveIntegerField('순서', default=0)
    is_active = models.BooleanField('활성화', default=True)

    class Meta:
        verbose_name = '협력사'
        verbose_name_plural = '협력사 목록'
        ordering = ['order']

    def __str__(self):
        return self.name


class FAQ(models.Model):
    """자주 묻는 질문"""

    CATEGORY_CHOICES = [
        ('general', '일반'),
        ('service', '서비스'),
        ('payment', '결제'),
        ('consulting', '컨설팅'),
        ('academy', '아카데미'),
    ]

    category = models.CharField(
        '카테고리',
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='general'
    )
    question = models.CharField('질문', max_length=300)
    answer = models.TextField('답변')
    order = models.PositiveIntegerField('순서', default=0)
    is_active = models.BooleanField('활성화', default=True)
    created_at = models.DateTimeField('생성일', auto_now_add=True)

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ 목록'
        ordering = ['category', 'order']

    def __str__(self):
        return self.question[:50]
