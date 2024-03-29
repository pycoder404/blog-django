#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import requests
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyBlog.settings')
import django

django.setup()

def article_serializer():
    from django.contrib.auth.models import User
    from article.models import Article
    from article.serializers import ArticleSerializer
    from comment.models import Comment
    from comment.serializers import CommentSerializer
    art = Article.objects.get(id=2)
    c = art.comments.all()
    c0 = c[0]
    print(c0)
    print(c0.article)
    print(dir(c0))
    # exit(0)
    ser = CommentSerializer(c,many=True)
    print('------------------')
    # print(ser.data)
    data = ser.data
    print(data[5])
    print(data[5]['parent'])
    # data = {'status': 'published', 'title': 'title', 'content': '大师傅阿斯蒂芬', 'importance': 1}
    # data['author'] = {'username':'root','email':'root@example.com'}
    # s = ArticleSerializer(data=data)
    # s.is_valid(raise_exception=True)

def main():
    """
    写自己的逻辑即可
    :return:
    """
    from article.models import Article
    article_serializer()
    # from article.serializers import ArticleSerializer
    # print(repr(ArticleSerializer()))
    # queryset = Article.objects.filter().prefetch_related('author').order_by(*('id',))
    # print(queryset)
    # s = ArticleSerializer(queryset, many=True)
    # s.is_valid(raise_exception=True)
    # print(s.data)
    # print(Article.objects.all())
    # article_serializer()

if __name__ == '__main__':
    main()
