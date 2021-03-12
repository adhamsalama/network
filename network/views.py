from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from .models import User, UserFollowing, Post
from .utils import paginate

login_required = login_required(login_url="login")


def index(request):
    return all_posts(request)
    #return render(request, "network/index.html")

@login_required
def create_post(request):
    if request.method == "GET":
        return render(request, "network/create_post.html")
    text = request.POST["text"]
    post = Post(user=request.user, text=text)
    post.save()
    messages.info(request, 'Post created successfully.')
    return HttpResponseRedirect(reverse("index"))

def all_posts(request):
    posts = Post.objects.order_by("-date")
    num = request.GET.get("page", 1)
    posts_paginator = paginate(posts, num)
    return render(request, "network/all_posts.html", 
                    {"paginator": posts_paginator["paginator"], "page_obj": posts_paginator["page_obj"], "posts": posts_paginator["posts"]})

@login_required
def following_posts(request):
    user = User.objects.get(username=request.user.username)
    followed_users = user.following.all()
    posts = []
    for followed_user in followed_users:
        user_posts = Post.objects.filter(user=followed_user.followed_user).order_by("-date")
        for user_post in user_posts:
            posts.append(user_post)
    posts.sort(key=lambda x: x.date, reverse=True)
    num = request.GET.get("page", 1)
    posts_paginator = paginate(posts, num)
    print(posts_paginator)
    return render(request, "network/following.html", 
                    {"paginator": posts_paginator["paginator"], "page_obj": posts_paginator["page_obj"], "posts": posts_paginator["posts"]})

def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        messages.warning(request, "User doesn't exist.")
        return HttpResponseRedirect(reverse("index"))
    posts = Post.objects.filter(user=user).order_by("-date")
    num = request.GET.get("page", 1)
    posts_paginator = paginate(posts, num)
    if request.user.is_authenticated:
        logged_user_follows_this_profile = bool(user.followers.filter(user=request.user))
    else:
        logged_user_follows_this_profile = False
    return render(request, "network/profile.html", 
                    {"profile_user": user,
                    "followers": user.followers.count(),
                    "following": user.following.count(),
                    "logged_user_follows_this_profile": logged_user_follows_this_profile,
                    "paginator": posts_paginator["paginator"], 
                    "page_obj": posts_paginator["page_obj"],
                    "posts": posts_paginator["posts"]})


@login_required
@require_http_methods(["POST"])
def follow_unfollow(request):
    data = json.loads(request.body)
    #return JsonResponse({"message": "Gotcha baby."}, status=201)
    followed_user_id = data["followed_user_id"]
    action = data["action"]
    if action == "follow":
        followed_user = User.objects.get(id=followed_user_id)
        try:
            user_follow = UserFollowing(user=request.user, followed_user=followed_user)
            user_follow.save()
        except:
            return JsonResponse({"message": "User already followed."}, status=400)
        return JsonResponse({"message": "User followed successfully"}, status=201) 
    else:
        followed_user = User.objects.get(id=data["followed_user_id"])
        user_follow = UserFollowing.objects.get(user=request.user, followed_user=followed_user)
        user_follow.delete()
        return JsonResponse({"message": "User unfollowed successfully."}, status=201)

@login_required
@require_http_methods(["POST"])
def like_unlike(request):
    data = json.loads(request.body)
    post = Post.objects.get(id=data["post_id"])
    print(post)
    if data["action"] == "like":
        post.likes.add(request.user)
        return JsonResponse({"message": "Post liked successfully."}, status=201)
    else:
        print(post.likes.all())
        post.likes.remove(request.user)
        return JsonResponse({"message": "Post unliked successfully."}, status=201)

@login_required
@require_http_methods(["POST"])
def edit_post(request):
    data = json.loads(request.body)
    post = Post.objects.get(id=data["post_id"])
    post.text = data["new_text"]
    post.save()
    return JsonResponse({"message": "Post edited successfully."}, status=201)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
