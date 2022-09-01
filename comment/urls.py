from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.CommentList.as_view(), name='comment-list'),
    path('detail/<int:id>/', views.CommentDetail.as_view(), name='comment-detail'),
    path('create/', views.CommentCreate.as_view(), name='comment-create'),
]
