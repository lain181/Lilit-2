from django.urls import path

from posts.views import FeedBase, PostDetail, CreatePost, PostsByTheme

urlpatterns = [
    path('', FeedBase.as_view(), name='feed'),
    path('post/<slug:slug>', PostDetail.as_view(), name='post'),
    path('newpost/', CreatePost.as_view(), name = 'new_post'),
    path('theme/<slug:slug>', PostsByTheme.as_view(), name = 'posts_by_theme')

]
