from django.conf import settings

from rest_framework import serializers

from article.models import Article
from django.contrib.auth.models import User

DATEFMT = settings.DATEFMT


class DjangoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        fields = ('username', 'email')


class ArticleSerializer(serializers.ModelSerializer):
    author = DjangoUserSerializer(read_only=True)

    # created_time = serializers.DateTimeField(format=DATEFMT)
    # last_modified_time = serializers.DateTimeField(format=DATEFMT)

    class Meta:
        model = Article
        fields = '__all__'

