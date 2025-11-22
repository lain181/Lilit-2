from django.urls import path

from posts.views import test1

urlpatterns = [
    path('', test1),

]
