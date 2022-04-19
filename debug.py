#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyBlog.settings')
import django

django.setup()


def main():
    """
    写自己的逻辑即可
    :return:
    """
    from article.models import Article
    from article.serializers import ArticleSerializer
    queryset = Article.objects.all()
    s = ArticleSerializer(queryset, many=True)
    # s.is_valid(raise_exception=True)
    print(s.data)
    # print(Article.objects.all())


if __name__ == '__main__':
    main()
