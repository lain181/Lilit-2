from django.urls import path

from posts.views import FeedBase, PostDetail

urlpatterns = [
    path('', FeedBase.as_view(), name='feed'),
    path('post/<slug:slug>', PostDetail.as_view(), name='post')
]
