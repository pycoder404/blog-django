from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateComment.as_view(), name='comment-create'),
]
