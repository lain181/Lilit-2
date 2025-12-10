from django.urls import path

from comments.views import CreateReply

urlpatterns = [
    path('reply/<int:id>', CreateReply.as_view(), name = 'reply'),
]
