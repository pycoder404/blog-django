import logging
import markdown
from collections import OrderedDict

from django.views import generic
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny

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
                # todo 放在前端还是后台？
                md = markdown.Markdown(
                    extensions=[
                        'markdown.extensions.extra',
                        'markdown.extensions.toc',
                    ]
                )
                for index in range(0,len(data)):
                    data[index]['content'] =  md.convert(data[index]['content'])

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
        # fixme 'markdown.extensions.codehilite',好像没用？
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
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        print("begin to save-->")
        # fixme  change to real author
        serializer.save(author_id=1)
