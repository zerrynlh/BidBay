from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:item>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("close/<int:item>", views.close_listing, name="close"),
    path("mylistings", views.mylistings, name="mylistings")
]
