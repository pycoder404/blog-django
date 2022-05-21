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
            queryset = self.model.objects.filter(**query_params).prefetch_related('author').order_by(*self.ordering)
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

    # def get_queryset(self):
    #     # return Article.objects.all()
    #     # todo 详细看下这里  https://www.django-rest-framework.org/api-guide/relations/
    #     # https://docs.djangoproject.com/en/4.0/ref/models/querysets/
    #     # 对于这种嵌套的多层的模型，如果使用正常的filter会导致在序列化过程中，每一条记录都去查询一次数据库，从后台执行的sql语句看
    #     # 使用了prefetch_related会使用sql的 key in (values)来筛选出来所有关联的数据
    #     return Article.objects.prefetch_related('author')


class ArticleDetail(BaseRetrieveAPIView):
    model = Article
    serializer_class = ArticleSerializer



    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        if self.request.GET.get('isedit', None):
            return Response(OrderedDict([('code', 0), ('data', data), ('message', 'ok')]))
        md = markdown.Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )

        # print("--------------------------------------------")
        md_content = md.convert(data['content'])
        data['content'] = md_content
        print(data['content'])
        data['toc'] = md.toc
        # print('---------------------------')
        # print(md.toc)
        # print('==========================')
        # 新增了md.toc对象
        # context = {'article': article, 'toc': md.toc}
        return Response(data)



class CreateArticle(BaseCreateAPIView):
    model = Article
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        print("begin to save-->")
        # fixme  change to real author
        serializer.save(author_id=2)


class UpdateArticle(BaseUpdateAPIView):
    model = Article
    serializer_class = ArticleSerializer
