from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    created_time = models.DateTimeField(default=timezone.now)
    last_modified_time = models.DateTimeField(auto_now=True)
    importance = models.IntegerField(default=1, null=False, blank=False)
    status = models.CharField(max_length=20, default='draft', null=False, blank=False)

    class Meta:
        db_table = 'article'
        ordering = ('-last_modified_time',)

    def __str__(self):
        return self.title