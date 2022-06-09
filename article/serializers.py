from django.conf import settings

from rest_framework import serializers

from article.models import Article
from article.models import Tag
from article.models import Category
from django.contrib.auth.models import User

DATEFMT = settings.DATEFMT


class DjangoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        fields = ('username', 'email')

class TagSerializer(serializers.HyperlinkedModelSerializer):
    """标签序列化器"""

    def check_tag_obj_exists(self, validated_data):
        text = validated_data.get('text')
        if Tag.objects.filter(text=text).exists():
            raise serializers.ValidationError('Tag with text {} exists.'.format(text))

    def create(self, validated_data):
        self.check_tag_obj_exists(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self.check_tag_obj_exists(validated_data)
        return super().update(instance, validated_data)

    class Meta:
        model = Tag
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """分类的序列化器"""
    # url = serializers.HyperlinkedIdentityField(view_name='category-detail')

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created']


class ArticleCategoryDetailSerializer(serializers.ModelSerializer):
    """给分类详情的嵌套序列化器"""
    url = serializers.HyperlinkedIdentityField(view_name='article-detail')

    class Meta:
        model = Article
        fields = [
            'url',
            'title',
        ]


class CategoryDetailSerializer(serializers.ModelSerializer):
    """分类详情"""
    articles = ArticleCategoryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'created',
            'articles',
        ]



class ArticleSerializer(serializers.ModelSerializer):
    author = DjangoUserSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True)
    # fixme 这里如果使用了格式后，就会导致创建过程中异常,传上的数据中是不包含这两个字段的
    # 问题已经解决，使用read_only属性即可，在提供数据用于显示过程中可以显示，在update或者create阶段由model 的auto_now属性来完成更新
    created_time = serializers.DateTimeField(format=DATEFMT,read_only=True)
    last_modified_time = serializers.DateTimeField(format=DATEFMT,read_only=True)

    # category 的嵌套序列化字段
    category = CategorySerializer(read_only=True)
    # category 的 id 字段，用于创建/更新 category 外键
    category_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)
    # tag 字段
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False,
        slug_field='text'
    )
    class Meta:
        model = Article
        # fields = '__all__'
        fields = ('id','author','author_id','title','content','created_time','last_modified_time','importance','status','tags',
                  'category','category_id')


    # 自定义错误信息
    default_error_messages = {
        'incorrect_avatar_id': 'Avatar with id {value} not exists.',
        'incorrect_category_id': 'Category with id {value} not exists.',
        'default': 'No more message here..'
    }

    def check_obj_exists_or_fail(self, model, value, message='default'):
        if not self.default_error_messages.get(message, None):
            message = 'default'

        if not model.objects.filter(id=value).exists() and value is not None:
            self.fail(message, value=value)


    # category_id 字段的验证器
    def validate_category_id(self, value):
        # 数据存在且传入值不等于None
        self.check_obj_exists_or_fail(
            model=Category,
            value=value,
            message='incorrect_category_id'
        )
        return value

    # 覆写方法，如果输入的标签不存在则创建它
    def to_internal_value(self, data):
        tags_data = data.get('tags')
        if isinstance(tags_data, list):
            for text in tags_data:
                if not Tag.objects.filter(text=text).exists():
                    Tag.objects.create(text=text)
        data['category_id'] = data.get('category',None)
        return super().to_internal_value(data)
