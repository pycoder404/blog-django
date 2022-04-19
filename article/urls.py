from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.ArticleList.as_view(), name='article_list'),
    path('detail/<int:pk>/', views.ArticalDetail.as_view(), name='article_detail'),
]

