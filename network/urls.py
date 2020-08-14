from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:user_id>", views.profile, name="profile"),

    # API Routes
    path("new_post", views.new_post, name="new_post"),
    path("get_posts/<str:post_filter>", views.get_posts, name="get_posts"),
    path("get_posts/<int:post_filter>", views.get_posts, name="get_posts"),
]
