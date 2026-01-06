from django.db import models


class CompanyInfo(models.Model):
    """회사 정보"""

    ceo_greeting = models.TextField('대표 인사말')
    vision = models.TextField('비전')
    mission = models.TextField('미션')
    ceo_name = models.CharField('대표자명', max_length=50, blank=True)
    ceo_photo = models.ImageField('대표자 사진', upload_to='company/', blank=True)

    class Meta:
        verbose_name = '회사 정보'
        verbose_name_plural = '회사 정보'

    def __str__(self):
        return '회사 정보'


class History(models.Model):
    """회사 연혁"""

    year = models.PositiveIntegerField('연도')
    month = models.PositiveIntegerField('월', null=True, blank=True)
    title = models.CharField('제목', max_length=100)
    description = models.TextField('설명', blank=True)

    class Meta:
        verbose_name = '연혁'
        verbose_name_plural = '연혁 목록'
        ordering = ['-year', '-month']

    def __str__(self):
        if self.month:
            return f'{self.year}.{self.month:02d} {self.title}'
        return f'{self.year} {self.title}'


class Expert(models.Model):
    """전문가/컨설턴트"""

    name = models.CharField('이름', max_length=50)
    position = models.CharField('직책', max_length=100)
    photo = models.ImageField('사진', upload_to='experts/')
    specialty = models.CharField('전문분야', max_length=200)
    certifications = models.TextField('자격증', blank=True)
    career = models.TextField('경력사항', blank=True)
    introduction = models.TextField('소개', blank=True)
    order = models.PositiveIntegerField('순서', default=0)
    is_active = models.BooleanField('활성화', default=True)

    class Meta:
        verbose_name = '전문가'
        verbose_name_plural = '전문가 목록'
        ordering = ['order']

    def __str__(self):
        return f'{self.name} ({self.position})'


class Achievement(models.Model):
    """사업 실적"""

    title = models.CharField('제목', max_length=100)
    value = models.CharField('수치', max_length=50)
    unit = models.CharField('단위', max_length=20, blank=True)
    icon = models.CharField('아이콘', max_length=50, blank=True)
    order = models.PositiveIntegerField('순서', default=0)

    class Meta:
        verbose_name = '사업 실적'
        verbose_name_plural = '사업 실적 목록'
        ordering = ['order']

    def __str__(self):
        return self.title


class OfficeLocation(models.Model):
    """오피스 위치"""

    name = models.CharField('지점명', max_length=50)
    address = models.CharField('주소', max_length=300)
    phone = models.CharField('전화번호', max_length=20)
    fax = models.CharField('팩스', max_length=20, blank=True)
    email = models.EmailField('이메일', blank=True)
    latitude = models.DecimalField('위도', max_digits=10, decimal_places=7)
    longitude = models.DecimalField('경도', max_digits=10, decimal_places=7)
    parking_info = models.TextField('주차안내', blank=True)
    is_main = models.BooleanField('본사', default=False)

    class Meta:
        verbose_name = '오피스 위치'
        verbose_name_plural = '오피스 위치 목록'

    def __str__(self):
        return self.name
