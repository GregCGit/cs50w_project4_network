from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("change_follow", views.change_follow, name="change_follow"),
    path("change_like", views.change_like, name="change_like"),
    path("new_post", views.new_post, name="new_post"),
    path("update_post", views.update_post, name="update_post")
]
