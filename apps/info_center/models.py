from django.db import models
from django.urls import reverse
from django.conf import settings


class PostCategory(models.Model):
    """게시물 카테고리"""

    name = models.CharField('카테고리명', max_length=50)
    slug = models.SlugField('슬러그', unique=True, allow_unicode=True)
    description = models.CharField('설명', max_length=200, blank=True)
    order = models.PositiveIntegerField('순서', default=0)

    class Meta:
        verbose_name = '게시물 카테고리'
        verbose_name_plural = '게시물 카테고리 목록'
        ordering = ['order']

    def __str__(self):
        return self.name


class Post(models.Model):
    """게시물"""

    category = models.ForeignKey(
        PostCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        verbose_name='카테고리'
    )
    title = models.CharField('제목', max_length=200)
    slug = models.SlugField('슬러그', allow_unicode=True)
    thumbnail = models.ImageField('썸네일', upload_to='posts/', blank=True)

    content = models.TextField('내용')
    summary = models.CharField('요약', max_length=300, blank=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='작성자'
    )
    author_name = models.CharField('작성자명', max_length=50, blank=True)

    tags = models.CharField('태그', max_length=200, blank=True, help_text='쉼표로 구분')
    view_count = models.PositiveIntegerField('조회수', default=0)

    is_published = models.BooleanField('공개', default=False)
    is_featured = models.BooleanField('메인 노출', default=False)
    published_at = models.DateTimeField('발행일', null=True, blank=True)
    created_at = models.DateTimeField('작성일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)

    class Meta:
        verbose_name = '게시물'
        verbose_name_plural = '게시물 목록'
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('info_center:post_detail', kwargs={'slug': self.slug})

    @property
    def tag_list(self):
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []


class GlossaryTerm(models.Model):
    """경매 용어사전"""

    CATEGORY_CHOICES = [
        ('rights', '권리분석'),
        ('procedure', '경매절차'),
        ('tax', '세금/비용'),
        ('legal', '법률용어'),
        ('general', '일반'),
    ]

    term = models.CharField('용어', max_length=100)
    definition = models.TextField('정의')
    category = models.CharField(
        '카테고리',
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='general'
    )
    related_terms = models.ManyToManyField(
        'self',
        blank=True,
        verbose_name='관련 용어'
    )
    order = models.PositiveIntegerField('순서', default=0)

    class Meta:
        verbose_name = '용어'
        verbose_name_plural = '용어사전'
        ordering = ['category', 'order', 'term']

    def __str__(self):
        return self.term


class Notice(models.Model):
    """공지사항"""

    NOTICE_TYPE_CHOICES = [
        ('notice', '공지'),
        ('event', '이벤트'),
        ('update', '업데이트'),
    ]

    notice_type = models.CharField(
        '유형',
        max_length=20,
        choices=NOTICE_TYPE_CHOICES,
        default='notice'
    )
    title = models.CharField('제목', max_length=200)
    content = models.TextField('내용')
    is_pinned = models.BooleanField('상단고정', default=False)
    is_published = models.BooleanField('공개', default=True)
    view_count = models.PositiveIntegerField('조회수', default=0)
    created_at = models.DateTimeField('작성일', auto_now_add=True)

    class Meta:
        verbose_name = '공지사항'
        verbose_name_plural = '공지사항 목록'
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title
