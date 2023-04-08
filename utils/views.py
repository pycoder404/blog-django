import logging
from collections import OrderedDict
from django.core.cache import cache
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from rest_framework.response import Response



logger = logging.getLogger('prod.utils')


class BaseGenericAPIView(GenericAPIView):
    # todo 需要一个更优雅的传参方式
    # 前端参数需要修改为 item=xx ，item[]__in=[],item__icontains='xxx'
    query_param_keys = []
    query_param_list_keys = []
    model = None

    serializer_class = None
    queryset = None

    # If you want to use object lookups other than pk, set 'lookup_field'.
    # For more complex lookup requirements override `get_object()`.
    lookup_field = 'id'
    lookup_url_kwarg = None

    # fixme default_ordering 是否需要参考default_query_params更换为函数
    default_ordering = ('-id',)
    is_cache = False  # 如果设置了缓存，则子类必须重写get_cache_key方法，防止一些和请求用户有关的请求出现问题

    # todo filed alias 对于一些查询为了方便前端显示，需要在查询过程中对字段做别名
    def get_queryset(self):
        """
        重写DRF原有的方法，从缓存获取数据,或者从数据库获取数据并更新cache
        如果获取数据这块有其他逻辑需要处理，业务模块可以重写get_queryset_data方法
        :return: queryset
        """
        if self.is_cache:
            cache_key = self.get_cache_key()
            queryset = self.get_queryset_data_from_cache(cache_key)
        else:
            queryset = self.get_queryset_data()
        return queryset

    def get_cache_key(self):
        """
        如果配置了缓存is_cache，则子类重写该方法,返回cache key值
        特别有些和用户相关的请求,需要慎重配置cache key
        """
        # 子类建议重写该方法,返回cache key值
        raise NotImplementedError('You must redefine get_queryset_cache_key or set is_cache=False')
        # return self.request.get_full_path()

    def get_queryset_data_from_cache(self, cache_key=None):
        """
        返回缓存数据,或者从数据库获取数据并更新cache
        :param cache_key: 缓存key
        :return:
        """
        value = cache.get(cache_key)
        if value:
            logger.info('Get value from cache, and key is : {key}'.format(key=cache_key))
            return value
        else:
            data_in_db = self.get_queryset_data()
            if data_in_db:
                logger.info('Insert value into cache, and key is: {key}'.format(key=cache_key))
                cache.set(cache_key, data_in_db)
            return data_in_db

    def get_queryset_data(self):
        """
        从数据库获取数据，各个子类可以根据情况重写
        :return: queryset form db;
        """
        if self.model is not None:
            query_params = self.get_query_params()
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

    @property
    def default_query_params(self):
        """
        :return:
        """
        return {}

    def get_query_params(self):
        # 这里default_query_params使用方法保证每次请求使用的query_params是新创建的，
        # 如果default_query_params直接赋值为 {} 则会导致不同请求query_params相互影响.
        # page和page_size 参数 不需要这里处理，统一由pagination处理了
        # 前端参数需要修改为 item=xx ，item[]__in=[],item__icontains='xxx'
        query_params = self.default_query_params

        if not hasattr(self, 'request'):
            # fixme 这里需要raise 正确的异常
            raise Exception('The instance must have a request attr')

        for item in self.query_param_keys:
            value = self.request.GET.get(item, None)
            if value:
                query_params[item] = value

        for item in self.query_param_list_keys:
            value = self.request.GET.getlist(item, None)
            if value:
                key = item[:-2] if '[]' in item else item
                query_params[key] = value
        # todo 这里传递的其实是引用(指针),多个请求之间是否隔离
        _query_params = self.query_params_transform(query_params)
        logger.info("Query parameters is:{}".format(_query_params))
        return _query_params

    def query_params_transform(self, query_params):
        """
        有些场景下需要对查询参数的值进行一个转换，返回转换后的请求参数
        例如datetime格式到bigint，各个子类根据情况重写
        :param query_params:
        :return:transformed_query_params
        """
        return query_params

    @property
    def ordering(self):
        return self.get_ordering()

    def get_ordering(self):
        return self.default_ordering


class BaseCreateAPIView(mixins.CreateModelMixin,
                    BaseGenericAPIView):
    """
    Concrete view for creating a model instance.
    """
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BaseListAPIView(mixins.ListModelMixin,
                  BaseGenericAPIView):
    """
    Concrete view for listing a queryset.
    """
    #  默认需要分页,防止数据过大
    is_paginated = True

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # 默认需要分页,防止数据过大
        if self.is_paginated:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        count = len(data)
        # return HttpResponse('forbidden',status=403)
        # 如果抛出drf的异常，drf是try...exception 处理的，可以返回响应
        # 如果语法错误等异常，django core handler处理
        return Response(OrderedDict([
            ('count', count),
            ('data', data)
        ]))


class BaseRetrieveAPIView(mixins.RetrieveModelMixin,
                      BaseGenericAPIView):
    """
    Concrete view for retrieving a model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class BaseDestroyAPIView(mixins.DestroyModelMixin,
                     BaseGenericAPIView):
    """
    Concrete view for deleting a model instance.
    """
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class BaseUpdateAPIView(mixins.UpdateModelMixin,
                    BaseGenericAPIView):
    """
    Concrete view for updating a model instance.
    """
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class BaseListCreateAPIView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        BaseGenericAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BaseRetrieveUpdateAPIView(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            BaseGenericAPIView):
    """
    Concrete view for retrieving, updating a model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class BaseRetrieveDestroyAPIView(mixins.RetrieveModelMixin,
                             mixins.DestroyModelMixin,
                             BaseGenericAPIView):
    """
    Concrete view for retrieving or deleting a model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class BaseRetrieveUpdateDestroyAPIView(mixins.RetrieveModelMixin,
                                   mixins.UpdateModelMixin,
                                   mixins.DestroyModelMixin,
                                   GenericAPIView):
    """
    Concrete view for retrieving, updating or deleting a model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
