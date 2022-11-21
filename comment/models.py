from django.db import models
from user.models import User
from article.models import Article


# 博文的评论
class Comment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    disabled = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    replied_to = models.IntegerField(default=0)
    # todo replied count and comment order ? how ???
    replied_count = models.IntegerField(default=0)
    liked_count = models.IntegerField(default=0)
    comment_order = models.IntegerField(default=1)

    class Meta:
        ordering = ('created_time',)
        unique_together = (('article_id', 'comment_order'),)

    def __str__(self):
        return self.content[:20]
