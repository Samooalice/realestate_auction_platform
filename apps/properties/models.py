from django.db import models
from django.urls import reverse
from django.conf import settings


class PropertyCategory(models.Model):
    """물건 카테고리"""

    name = models.CharField('카테고리명', max_length=50)
    slug = models.SlugField('슬러그', unique=True, allow_unicode=True)
    description = models.CharField('설명', max_length=200, blank=True)
    order = models.PositiveIntegerField('순서', default=0)

    class Meta:
        verbose_name = '물건 카테고리'
        verbose_name_plural = '물건 카테고리 목록'
        ordering = ['order']

    def __str__(self):
        return self.name


class Property(models.Model):
    """경매 물건"""

    PROPERTY_TYPE_CHOICES = [
        ('apartment', '아파트'),
        ('villa', '빌라/다세대'),
        ('house', '단독주택'),
        ('officetel', '오피스텔'),
        ('commercial', '상가'),
        ('office', '오피스'),
        ('factory', '공장'),
        ('warehouse', '창고'),
        ('land', '토지'),
        ('other', '기타'),
    ]

    AUCTION_STATUS_CHOICES = [
        ('scheduled', '입찰예정'),
        ('ongoing', '진행중'),
        ('completed', '완료'),
        ('cancelled', '취소'),
    ]

    RISK_LEVEL_CHOICES = [
        ('A', '안전'),
        ('B', '보통'),
        ('C', '주의'),
    ]

    # 기본 정보
    case_number = models.CharField('사건번호', max_length=50)
    title = models.CharField('제목', max_length=200)
    category = models.ForeignKey(
        PropertyCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='properties',
        verbose_name='카테고리'
    )
    property_type = models.CharField(
        '물건유형',
        max_length=20,
        choices=PROPERTY_TYPE_CHOICES
    )

    # 위치 정보
    address = models.CharField('주소', max_length=300)
    sido = models.CharField('시도', max_length=20)
    sigungu = models.CharField('시군구', max_length=20)
    dong = models.CharField('읍면동', max_length=20, blank=True)
    latitude = models.DecimalField(
        '위도', max_digits=10, decimal_places=7, null=True, blank=True
    )
    longitude = models.DecimalField(
        '경도', max_digits=10, decimal_places=7, null=True, blank=True
    )

    # 면적/층수
    area_land = models.DecimalField(
        '대지면적(㎡)', max_digits=10, decimal_places=2, null=True, blank=True
    )
    area_building = models.DecimalField(
        '건물면적(㎡)', max_digits=10, decimal_places=2, null=True, blank=True
    )
    floor_info = models.CharField('층수', max_length=50, blank=True)

    # 가격 정보
    appraisal_price = models.BigIntegerField('감정가')
    minimum_price = models.BigIntegerField('최저가')
    market_price = models.BigIntegerField('시세', null=True, blank=True)

    # 경매 정보
    auction_date = models.DateField('입찰일')
    auction_status = models.CharField(
        '경매상태',
        max_length=20,
        choices=AUCTION_STATUS_CHOICES,
        default='scheduled'
    )
    bid_count = models.PositiveIntegerField('유찰횟수', default=0)
    court = models.CharField('관할법원', max_length=50, blank=True)

    # 권리분석
    rights_analysis = models.TextField('권리분석 요약')
    risk_level = models.CharField(
        '리스크등급',
        max_length=1,
        choices=RISK_LEVEL_CHOICES,
        default='B'
    )
    tenant_info = models.TextField('임차인 현황', blank=True)
    special_conditions = models.TextField('특이사항', blank=True)

    # 추천 정보
    is_recommended = models.BooleanField('추천물건', default=False)
    is_weekly_pick = models.BooleanField('금주의 추천', default=False)
    recommendation_reason = models.TextField('추천 이유', blank=True)
    tags = models.CharField('태그', max_length=200, blank=True, help_text='쉼표로 구분')

    # 이미지
    thumbnail = models.ImageField('대표이미지', upload_to='properties/thumbnails/')

    # 조회/관심
    view_count = models.PositiveIntegerField('조회수', default=0)

    # 타임스탬프
    created_at = models.DateTimeField('등록일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)

    class Meta:
        verbose_name = '경매 물건'
        verbose_name_plural = '경매 물건 목록'
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.case_number}] {self.title}'

    def get_absolute_url(self):
        return reverse('properties:detail', kwargs={'pk': self.pk})

    @property
    def discount_rate(self):
        """시세 대비 할인율"""
        if self.market_price and self.market_price > 0:
            return round((1 - self.minimum_price / self.market_price) * 100, 1)
        return 0

    @property
    def tag_list(self):
        """태그 리스트"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []


class PropertyImage(models.Model):
    """물건 이미지"""

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='물건'
    )
    image = models.ImageField('이미지', upload_to='properties/images/')
    caption = models.CharField('설명', max_length=100, blank=True)
    order = models.PositiveIntegerField('순서', default=0)

    class Meta:
        verbose_name = '물건 이미지'
        verbose_name_plural = '물건 이미지 목록'
        ordering = ['order']

    def __str__(self):
        return f'{self.property.title} - 이미지 {self.order}'


class PropertyBookmark(models.Model):
    """관심 물건"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookmarks',
        verbose_name='회원'
    )
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='bookmarks',
        verbose_name='물건'
    )
    created_at = models.DateTimeField('등록일', auto_now_add=True)

    class Meta:
        verbose_name = '관심 물건'
        verbose_name_plural = '관심 물건 목록'
        unique_together = ['user', 'property']

    def __str__(self):
        return f'{self.user.username} - {self.property.title}'
