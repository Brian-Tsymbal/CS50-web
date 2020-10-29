

from django.urls import path
from django.urls import re_path

from . import views
from . import templates


urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.new_wiki, name="create"),
    path("random", views.random_search, name="name"),
    path('search', views.search_func, name="search"),
    path("update/<str:names>", views.update, name="update"),
    # this needs to be last
    path("<str:name>", views.visit, name="visit"),
]
