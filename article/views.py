from django.shortcuts import render
from django.shortcuts import HttpResponse
from article.models import Article
from article.serializers import ArticleSerializer
# Create your views here.
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.mixins import ListModelMixin


def index(request):
    return HttpResponse('article index page')


def article_list(request):
    return HttpResponse('article list page')


class ArticleList(ListModelMixin, GenericAPIView):
    """
    Concrete view for listing a queryset.
    """
    serializer_class = ArticleSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        # return Article.objects.all()
        # todo 详细看下这里  https://www.django-rest-framework.org/api-guide/relations/
        # https://docs.djangoproject.com/en/4.0/ref/models/querysets/
        # 对于这种嵌套的多层的模型，如果使用正常的filter会导致在序列化过程中，每一条记录都去查询一次数据库，从后台执行的sql语句看
        # 使用了prefetch_related会使用sql的 key in (values)来筛选出来所有关联的数据
        return Article.objects.prefetch_related('author')


class ArticalDetail(RetrieveAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.all()
