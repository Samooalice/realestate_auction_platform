from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """커스텀 사용자 모델"""

    USER_TYPE_CHOICES = [
        ('individual', '개인'),
        ('corporate', '기업'),
    ]

    phone = models.CharField('연락처', max_length=20, blank=True)
    user_type = models.CharField(
        '회원유형',
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='individual'
    )
    marketing_agreed = models.BooleanField('마케팅 수신동의', default=False)
    created_at = models.DateTimeField('가입일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)

    class Meta:
        verbose_name = '회원'
        verbose_name_plural = '회원 목록'

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    """사용자 프로필 확장"""

    BUDGET_CHOICES = [
        ('under_1', '1억 이하'),
        ('1_to_3', '1~3억'),
        ('3_to_5', '3~5억'),
        ('5_to_10', '5~10억'),
        ('over_10', '10억 이상'),
    ]

    INTEREST_CHOICES = [
        ('home_buying', '내집마련'),
        ('redevelopment', '재개발/재건축'),
        ('rental_income', '임대수익'),
        ('company_building', '사옥마련'),
        ('senior_facility', '노유자시설'),
    ]

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='회원'
    )
    preferred_region = models.CharField('관심지역', max_length=100, blank=True)
    budget_range = models.CharField(
        '예산범위',
        max_length=20,
        choices=BUDGET_CHOICES,
        blank=True
    )
    interest_type = models.CharField(
        '관심분야',
        max_length=30,
        choices=INTEREST_CHOICES,
        blank=True
    )
    memo = models.TextField('메모', blank=True)

    class Meta:
        verbose_name = '회원 프로필'
        verbose_name_plural = '회원 프로필 목록'

    def __str__(self):
        return f'{self.user.username}의 프로필'
