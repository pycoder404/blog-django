from django.contrib import admin

# Register your models here.
from article.models import Article,Category,Tag
admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Tag)