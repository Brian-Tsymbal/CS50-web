
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("UserProfile/<int:user_id>", views.profile, name="UserProfile"),
    path("following", views.following, name="following"),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),


    path("AllFollowers", views.AllFollowers, name="AllFollowers"),
    path("UserProfile/AllFollowers/<int:follower_id>",
         views.Follower, name="Follower"),

    path("New", views.newpost, name="New"),
    path("CreatePost", views.CreateNewPost, name="create"),
    path("AllPosts", views.AllPosts, name="AllPosts"),
    path("AllPosts/<int:post_id>", views.post, name="posts")
]
