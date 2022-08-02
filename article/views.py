import json
import os
import datetime
import logging
import markdown

from django.views import generic
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from article.models import Article, Tag, Category
from article.serializers import ArticleSerializer, TagSerializer, CategorySerializer
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
    query_param_keys = ['category', 'tags']
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
            query_params['category__title'] = query_params.pop('category', None)

        if 'tags' in query_params.keys():
            query_params['tags__title'] = query_params.pop('tags', None)
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
    # fixme 代理中禁用put方法，所以这里直接用post，后续删除
    def post(self, request, *args, **kwargs):
        return self.put(request,*args,**kwargs)


class UploadView(generic.View):
    """ upload image file """

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(UploadView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        upload_file = request.FILES.get("upload_file", None)
        media_root = settings.MEDIA_ROOT
        media_url = settings.MEDIA_URL
        # image none check
        if not upload_file:
            return HttpResponse({'data': json.dumps({
                'code': 1,
                'message': "未检测到上传的文件信息",
                'url': ""
            })})

        # file format check
        file_name_list = upload_file.name.split('.')
        file_extension = file_name_list.pop(-1)
        file_name = '.'.join(file_name_list)
        # fixme  check file size
        # if file_extension not in MDEDITOR_CONFIGS['upload_image_formats']:
        #     return HttpResponse(json.dumps({
        #         'success': 0,
        #         'message': "上传图片格式错误，允许上传图片格式为：%s" % ','.join(
        #             MDEDITOR_CONFIGS['upload_image_formats']),
        #         'url': ""
        #     }))

        # image floder check
        file_path = os.path.join(media_root, 'img')
        if not os.path.exists(file_path):
            try:
                os.makedirs(file_path)
            except Exception as err:
                return HttpResponse(json.dumps({
                    'code': 1,
                    'message': "上传失败：%s" % str(err),
                    'url': ""
                }))

        # save image
        print("file_path is:{}".format(file_path))
        file_full_name = '%s_%s.%s' % (file_name, '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()),
                                       file_extension)
        with open(os.path.join(file_path, file_full_name), 'wb+') as file:
            for chunk in upload_file.chunks():
                file.write(chunk)

        # todo 后续这里反馈的是一个相对链接url即可，前端，后台，还有media，static全部放在nginx后面，使用不同的url匹配转发即可
        return HttpResponse(json.dumps({'data': {'code': 0, 'message': "上传成功！",
                                                 'url': '{}/img/{}'.format(media_url,file_full_name)}})
                            )
