from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("following/<int:user_id>", views.following, name="following"),

    # API Routes
    path("new_post", views.new_post, name="new_post"),
    path("get_posts", views.get_posts, name="get_posts"),
    path("change_follow", views.change_follow, name="change_follow"),
]
