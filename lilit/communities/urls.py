from django.urls import path

from communities.views import CreateCommunity

urlpatterns = [
    path('create/', CreateCommunity.as_view(), name = 'create_community'),
]