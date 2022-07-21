import logging
import markdown
from django.shortcuts import HttpResponse

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser,IsAuthenticated,AllowAny

from article.models import Article,Tag,Category
from article.serializers import ArticleSerializer,TagSerializer,CategorySerializer
from utils.views import BaseListAPIView, BaseRetrieveAPIView, BaseCreateAPIView, BaseUpdateAPIView

logger = logging.getLogger('dev')


def index(request):
    return HttpResponse('article index page')

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class ArticleList(BaseListAPIView):
    """
    Concrete view for listing a queryset.
    """
    model = Article
    serializer_class = ArticleSerializer
    is_page = False
    query_param_keys = ['category','tags']
    # 这里的权限管理分两个部分进行的，首先在authentication中进行用户的信息确认
    # 然后再permission中对用户权限进行判断，
    # 如果用户权限管理算的话，就分为三部分了
    # authentication_classes = ()
    permission_classes = [IsAdminUser]
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

    def query_params_transform(self, query_params):
        if 'category' in query_params.keys():
            query_params['category__title'] = query_params.pop('category',None)

        if 'tags' in query_params.keys():
            query_params['tags__title'] = query_params.pop('tags',None)
        return query_params

class ArticleDetail(BaseRetrieveAPIView):
    model = Article
    serializer_class = ArticleSerializer
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


class CreateArticle(BaseCreateAPIView):
    model = Article
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        print("begin to save-->")
        # fixme  change to real author
        serializer.save(author_id=1)


class UpdateArticle(BaseUpdateAPIView):
    model = Article
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminUser]
