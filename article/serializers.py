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
    # fixme 这里如果使用了格式后，就会导致创建过程中异常,传上的数据中是不包含这两个字段的
    # created_time = serializers.DateTimeField(format=DATEFMT)
    # last_modified_time = serializers.DateTimeField(format=DATEFMT)

    class Meta:
        model = Article
        # fields = '__all__'
        fields = ('id','author','title','content','created_time','last_modified_time','importance','status')
