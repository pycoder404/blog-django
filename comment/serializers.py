from django.conf import settings

from rest_framework import serializers

from comment.models import Comment

DATEFMT = settings.DATETIMEFMT


class ParentCommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')
    created_time = serializers.DateTimeField(format=DATEFMT, read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'author', 'content', 'created_time', 'comment_order')


class CommentSerializer(serializers.ModelSerializer):
    article = serializers.SlugRelatedField(read_only=True, slug_field='title')
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')
    created_time = serializers.DateTimeField(format=DATEFMT, read_only=True)
    parent = ParentCommentSerializer(read_only=True)
    parent_id = serializers.IntegerField(write_only=True,required=False)

    class Meta:
        depth = 1
        model = Comment
        # fields = '__all__'
        fields = ('id', 'article', 'article_id', 'author', 'author_id', 'content', 'created_time', 'parent',
                  'parent_id', 'replied_count', 'liked_count', 'disabled', 'comment_order')

    #
    # # 自定义错误信息
    # default_error_messages = {
    #     'incorrect_avatar_id': 'Avatar with id {value} not exists.',
    #     'incorrect_category_id': 'Category with id {value} not exists.',
    #     'default': 'No more message here..'
    # }
    #
    # def check_obj_exists_or_fail(self, model, value, message='default'):
    #     if not self.default_error_messages.get(message, None):
    #         message = 'default'
    #
    #     if not model.objects.filter(id=value).exists() and value is not None:
    #         self.fail(message, value=value)
    #
    #
    # # category_id 字段的验证器
    # def validate_category_id(self, value):
    #     # 数据存在且传入值不等于None
    #     self.check_obj_exists_or_fail(
    #         model=Category,
    #         value=value,
    #         message='incorrect_category_id'
    #     )
    #     return value
    #
    # @staticmethod
    # def get_category_id(category_title):
    #     if not category_title:
    #         return None
    #     _category= Category.objects.filter(title=category_title).values('id')
    #     return _category[0]['id'] if _category else None
    #
    # # 覆写方法，如果输入的标签不存在则创建它
    # # 并将category从title转换为id
    # def to_internal_value(self, data):
    #     # tags_data = data.get('tags')
    #     # if isinstance(tags_data, list):
    #     #     for title in tags_data:
    #     #         if not Tag.objects.filter(title=title).exists():
    #     #             Tag.objects.create(title=title)
    #     data['category_id'] = self.get_category_id(data.get('category',None))
    #     return super().to_internal_value(data)
    #
