from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.Creating_listing, name="create"),
    path("categories", views.Categories, name="categories"),
    path("Watchlist", views.WatchlistPage, name="Watchlist"),
    path("Biding/<item>", views.Biding, name="Biding"),
    path("<str:name>", views.GeneralView, name="listing")
]
