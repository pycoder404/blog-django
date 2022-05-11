class BaseException(Exception):
    def __init__(self, message='服务内部错误，请联系管理员.', code=1, status=200):
        self.message = message
        self.code = code
        self.status = status

    def __str__(self):
        return str(self.message)


"""
Global Django exception and warning classes.
"""


class FieldDoesNotExist(BaseException):
    """The requested model field does not exist"""
    pass


class AppRegistryNotReady(BaseException):
    """The django.apps registry is not populated yet"""
    pass


class ObjectDoesNotExist(BaseException):
    """The requested object does not exist"""
    silent_variable_failure = True


class MultipleObjectsReturned(BaseException):
    """The query returned multiple objects when only one was expected."""
    pass


class PermissionDenied(BaseException):
    """The user did not have permission to do that"""
    pass


class ViewDoesNotExist(BaseException):
    """The requested view does not exist"""
    pass


class MiddlewareNotUsed(BaseException):
    """This middleware is not used in this server configuration"""
    pass


class ImproperlyConfigured(BaseException):
    """Django is somehow improperly configured"""
    pass


class FieldError(BaseException):
    """Some kind of problem with a model field."""
    pass


class EmptyResultSet(BaseException):
    """A database query predicate is impossible."""
    pass
