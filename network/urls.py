
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post", views.create_post, name="create_post"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("all_posts", views.all_posts, name="all_posts"),
    path("following", views.following_posts, name="following"),
    path("follow_unfollow", views.follow_unfollow, name="follow_unfollow"),
    path("like_unlike", views.like_unlike, name="like_unlike"),
    path("edit_post", views.edit_post, name="edit_post")
]
