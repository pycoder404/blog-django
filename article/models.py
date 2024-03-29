from django.db import models
from django.utils import timezone
from user.models import User

class Tag(models.Model):
    """文章标签"""
    title = models.CharField(max_length=30,unique=True)
    # fixme add is_public?
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title


class Category(models.Model):
    """文章分类"""
    title = models.CharField(max_length=100,unique=True)
    created = models.DateTimeField(default=timezone.now)
    # fixme add is_public?

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Avatar(models.Model):
    content = models.ImageField(upload_to='avatar/%Y%m%d')


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    created_time = models.DateTimeField(default=timezone.now)
    last_modified_time = models.DateTimeField(auto_now=True)
    importance = models.IntegerField(default=1, null=False, blank=False)
    status = models.CharField(max_length=20, default='public', null=False, blank=False)
    views_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    # 分类
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='articles'
    )
    # 标签
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='articles'
    )


    class Meta:
        db_table = 'article'
        ordering = ('-last_modified_time',)

    def __str__(self):
        return self.title
