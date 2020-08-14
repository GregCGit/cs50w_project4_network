import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import Like, Post, User


def index(request):
    return render(request, "network/index.html")


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


@csrf_exempt
@login_required
def new_post(request):
    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    #  Add data checking here
    data = json.loads(request.body)
    user = User.objects.get(id=request.user.id)
    entry = data.get("entry", "")

    if not entry:
        return JsonResponse({"error": "Post cannot be empty."}, status=400)

    post = Post(
        user=user,
        entry=entry
    )
    post.save()
    return JsonResponse({"message": "Post logged successfully."}, status=201)

def count_likes(post_id, user_id):
    like_dict = {
        'num_like': 0,
        'user_like': 0
        }
    try:
        # First, lets get the count
        like_dict['num_like'] = Like.objects.filter(post_id=post_id).count()
        print("Likes", post_id, like_dict['num_like'])
        # And then check to see if the user liked it
        try:
            like_dict['user_like'] = Like.objects.filter(post_id=post_id, user_id=user_id).count()
        except ObjectDoesNotExist:
            pass
        #comment_post = []
        #for item in comment_pre:
        #    temp = [User.objects.only('username').get(id=item.user_id).username, item.comment]
        #    comment_post.append(temp)
    except ObjectDoesNotExist:
        pass
    return like_dict

def get_posts(request, post_filter):
    #print("User name here", user)
    #print("User name here", user.id)
    print("User name here", request.user.id)

    print("Filter", post_filter)

    if post_filter == 'all':
        posts = Post.objects.all()
    
    # Figure out likes - first, count up the number of likes per post
    fullpostlist = []
    posts = posts.order_by("-timestamp").all()
    for post in posts:
        print("Post-ie", post)
        like_dict = count_likes(post.id, request.user.id)
        fullpostlist.append( {
            "id": post.id,
            "user": post.user.username,
            "entry": post.entry,
            "timestamp": post.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "like":  like_dict['num_like'],
            "user_like": like_dict['user_like']
        })

    # Determine if the current user liked the post
    # Probably need to rewrite serialize
    #fullpostlist = json.dumps(fullpostlist)
    print("Posts", fullpostlist)
    return JsonResponse(fullpostlist, safe=False)
    #return JsonResponse([post.serialize() for post in posts], safe=False)
    #return JsonResponse({"message": "Sure, we got here."}, status=201)
