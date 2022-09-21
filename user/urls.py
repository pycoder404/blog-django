from django.urls import path
from . import views

# rest_framework_simplejwt中的baseview对authentication_class置空重写覆盖了rest_framework父类的 authentication_class
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('', views.index, name='index'),
    path('info/', views.UserInfo.as_view(), name='info'),
    path('logout/', views.index, name='logout'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/github/', views.GitHubLogin.as_view(), name='github_login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='refresh'),

]

