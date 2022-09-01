
import logging
import markdown

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
