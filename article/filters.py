from django_filters import rest_framework as filters

class IsAdminFitlerBackend(filters.DjangoFilterBackend):
    """
    filter only admin
    """

    def filter_queryset(self, request, queryset, view):
        user = request.user
        if hasattr(user,'roles') and 'admin' in user.roles.split(","):
            return  queryset
        else:
            return queryset.filter(status='published')