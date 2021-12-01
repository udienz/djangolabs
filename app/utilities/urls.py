from django.urls import path

from .views import get_home

urlpatterns = [
    path("", get_home, name="home"),
]
