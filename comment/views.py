import logging
import markdown
from django.db.models import F

from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework import status

from comment.models import Comment
from comment.serializers import CommentSerializer
from utils.views import BaseListAPIView, BaseRetrieveAPIView, BaseCreateAPIView, BaseUpdateAPIView

logger = logging.getLogger('dev')


class CommentList(BaseListAPIView):
    """
    Concrete view for listing a queryset.
    """
    model = Comment
    serializer_class = CommentSerializer
    is_page = True
    default_ordering = ('id',)
    query_param_keys = ['article_id']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # 默认需要分页,防止数据过大
        if self.is_page:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                data = serializer.data
                md = markdown.Markdown(
                    extensions=[
                        'markdown.extensions.extra',
                        'markdown.extensions.toc',
                    ]
                )
                for index in range(0, len(data)):
                    data[index]['mdcontent'] = md.convert(data[index]['content'])


                return self.get_paginated_response(serializer.data)
        else:
            # fixme
            raise Exception


class CommentDetail(BaseRetrieveAPIView):
    model = Comment
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # 编辑模式下，将原始内容返回
        if self.request.GET.get('isedit', None) == 'true':
            return Response(data)

        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        md = markdown.Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.toc',
            ]
        )
        data['content'] = md.convert(data['content'])
        data['toc'] = md.toc
        return Response(data)


class CommentCreate(BaseCreateAPIView):
    model = Comment
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    # how to get replied to
    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user.id)
        replied_to = serializer.validated_data['replied_to']
        article_id = serializer.validated_data['article_id']

        if replied_to:
            self.model.objects.filter(article_id=article_id, comment_order=replied_to).update(
                replied_count=F('replied_count') + 1)
        # if serializer.valid_data:
        #     self.model.objects.get(article_id=article_id,comment_order=replied_to).update(replied_count=1)
        # todo if replied_to , replied_to's replied_count += 1
        # todo should be a mysql transaction(如果有多个评论可能存在死锁的问题)

    def get_request_data(self, request):
        logger.info("request data is:{}".format(request.data))
        post_data = request.data
        article_id = post_data['article_id']
        if not article_id:
            raise Exception

        comment_order = self.model.objects.filter(article_id=article_id).count()
        post_data['comment_order'] = comment_order + 1
        return post_data

    def create(self, request, *args, **kwargs):
        logger.info('create, get serializer -->')
        logger.info("request data is:{}".format(request.data))
        data = self.get_request_data(request)
        serializer = self.get_serializer(data=data)
        logger.info('get serializer--> done')
        logger.info('begin to call serializer is_valid function')
        serializer.is_valid(raise_exception=True)
        logger.info('serializer.errors:{}'.format(serializer.errors))
        logger.info('before create-->')
        self.perform_create(serializer)
        # logs.info('creat done')
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
