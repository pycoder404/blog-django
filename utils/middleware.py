import json
from django.http import HttpResponse
from utils.exceptions import BaseException

from django.utils.deprecation import MiddlewareMixin


class UtilsExceptionMiddleware(MiddlewareMixin):

    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__(get_response)

    def process_exception(self, request, exception):
        """
        process_exception, 接收HttpRequest和Exception两个参数，在view抛出异常后开始调用，返回None或者HttpResponse对象
        返回值默认为None,如果返回一个HttpResponse对象,则直接返回上层的middleware进行response处理.
        :param request:
        :param exception:
        :return: None or HttpResponse object
        """

        if not isinstance(exception, BaseException):
            return None
        res = {
            "message": exception.message,
            "code": exception.code,
        }
        return HttpResponse(content=json.dumps(res), status=exception.status)
    #
    # def process_request(self, request):
    #     """
    #     process_request,在调用下一个middleware之前执行,接收的为HttpRequest实例为参数,在这里我们对request进行预先的统一处
    #     理,例如从cookie里面获取到session的sessionid信息,然后获取到正式的session.
    #     返回值默认为None,调用下面middleware的process_request,如果返回一个HttpResponse对象,则直接返回上层的middleware进行
    #     response处理,不再调用下面的middleware.
    #     :param request: HttpRequest对象
    #     :return: None or HttpResponse object
    #     """
    #     print("utils--> process_request")
    #     return None
    #
    #
    # def process_response(self, request, response):
    #     """
    #     process_response，由下级middleware返回response后调用，接收HttpRequest和HttpResponse两个参数，主要对response进行一些统一
    #     处理，例如对session进行更新和检查，然后返回一个HttpResponse对象，由上级的middleware进行在处理
    #     :param request: HttpRequest对象
    #     :param response: HttpResponse对象
    #     :return: HttpResponse object
    #     """
    #     print("utils--> process_response")
    #
    #     return response
    #
    # def process_view(self, request, view_func, view_args, view_kwargs):
    #     """
    #     process_view, 应该类似于urls中配置的view，在process_request 调用链 之后调用
    #     :param request: request实例
    #     :param view_func: django需要调用处理view的函数，真实的函数对象，而不是函数名
    #     :param view_args:
    #     :param view_kwargs:
    #     :return: None or HttpResponse object
    #     """
    #
    #     return None
