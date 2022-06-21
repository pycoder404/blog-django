import logging
from collections import OrderedDict
import markdown
from django.contrib.auth.models import User
from rest_framework.response import Response

from django.shortcuts import HttpResponse
from article.models import Article
from article.serializers import ArticleSerializer
# Create your views here.

from utils.views import BaseListAPIView, BaseRetrieveAPIView, BaseCreateAPIView, BaseUpdateAPIView

logger = logging.getLogger('dev')


def index(request):
    return HttpResponse('article index page')


class ArticleList(BaseListAPIView):
    """
    Concrete view for listing a queryset.
    """
    model = Article
    serializer_class = ArticleSerializer
    def get_queryset_data(self):
        """
        从数据库获取数据，各个子类可以根据情况重写
        :return: queryset form db;
        """
        if self.model is not None:
            query_params = self.get_query_params()
            # todo 详细看下这里  https://www.django-rest-framework.org/api-guide/relations/  prefetch_related
            # todo 这里两种方案的性能如何选择,如果使用当前这种不带prefetch的，那这个方法也没有必要重写，直接使用即可
            # queryset = self.model.objects.filter(**query_params).prefetch_related('author','category','tags').order_by(*self.ordering)
            queryset = self.model.objects.filter(**query_params).order_by(*self.ordering)
            if not queryset:
                logger.warning('Get empty data from db by query:{}'.format(self.request.get_full_path()))
        else:
            raise Exception(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )
        return queryset


class ArticleDetail(BaseRetrieveAPIView):
    model = Article
    serializer_class = ArticleSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        # 编辑模式下，将原始内容返回
        if self.request.GET.get('isedit', None) == 'true':
            return Response(data)

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


class CreateArticle(BaseCreateAPIView):
    model = Article
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        print("begin to save-->")
        # fixme  change to real author
        serializer.save(author_id=1)


class UpdateArticle(BaseUpdateAPIView):
    model = Article
    serializer_class = ArticleSerializer
