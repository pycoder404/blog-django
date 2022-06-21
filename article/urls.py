from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.ArticleList.as_view(), name='article-list'),
    path('detail/<int:id>/', views.ArticleDetail.as_view(), name='article-detail'),
    # path('detail/', views.ArticleDetail.as_view(), name='article_detail'),
    path('create/', views.CreateArticle.as_view(), name='article-create'),
    path('update/<int:id>/', views.UpdateArticle.as_view(), name='article-update'),
]

