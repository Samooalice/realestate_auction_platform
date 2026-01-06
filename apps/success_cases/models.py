from django.db import models
from django.urls import reverse
from apps.services.models import ServiceCategory


class SuccessCase(models.Model):
    """성공 사례"""

    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='success_cases',
        verbose_name='서비스 분야'
    )
    title = models.CharField('제목', max_length=200)
    thumbnail = models.ImageField('대표이미지', upload_to='success_cases/')

    # 물건 정보
    property_type = models.CharField('물건유형', max_length=50)
    location = models.CharField('소재지', max_length=100)
    winning_price = models.BigIntegerField('낙찰가')
    market_price = models.BigIntegerField('시세')

    # 스토리
    client_situation = models.TextField('고객 상황')
    selection_reason = models.TextField('물건 선정 이유')
    analysis_process = models.TextField('권리분석 과정')
    bidding_strategy = models.TextField('입찰 전략')
    result_summary = models.TextField('결과 및 수익')

    # 표시 설정
    is_featured = models.BooleanField('메인 노출', default=False)
    is_published = models.BooleanField('공개', default=True)
    view_count = models.PositiveIntegerField('조회수', default=0)

    created_at = models.DateTimeField('등록일', auto_now_add=True)

    class Meta:
        verbose_name = '성공사례'
        verbose_name_plural = '성공사례 목록'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('success_cases:detail', kwargs={'pk': self.pk})

    @property
    def profit_rate(self):
        """수익률 계산"""
        if self.market_price > 0:
            return round((self.market_price - self.winning_price) / self.winning_price * 100, 1)
        return 0

    @property
    def profit_amount(self):
        """수익금액"""
        return self.market_price - self.winning_price


class CustomerReview(models.Model):
    """고객 후기"""

    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='reviews',
        verbose_name='서비스 분야'
    )
    author_name = models.CharField('작성자', max_length=20, help_text='이니셜 또는 가명')
    rating = models.PositiveIntegerField('평점', choices=RATING_CHOICES, default=5)
    title = models.CharField('제목', max_length=100, blank=True)
    content = models.TextField('후기 내용')
    video_url = models.URLField('영상 URL', blank=True, help_text='유튜브 URL')

    is_approved = models.BooleanField('승인', default=False)
    is_featured = models.BooleanField('메인 노출', default=False)
    created_at = models.DateTimeField('작성일', auto_now_add=True)

    class Meta:
        verbose_name = '고객 후기'
        verbose_name_plural = '고객 후기 목록'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author_name} - {self.rating}점'
