"""MyBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# from article.views import ArticleViewSet
from article.views import TagViewSet
from article.views import CategoryViewSet

router = DefaultRouter()
router.register(r'api/tag', TagViewSet, basename='tag')
router.register(r'api/category', CategoryViewSet, basename='category')


urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('api/article/', include('article.urls')),
    path('api/comment/', include('comment.urls')),
    path('api/accounts/', include('allauth.urls')),

]
urlpatterns += router.urls
