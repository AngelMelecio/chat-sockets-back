from django.urls import path
from chat.views import post_api_view

urlpatterns = [
    path('posts/', post_api_view, name='post_api')
]
