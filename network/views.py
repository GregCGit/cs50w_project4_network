import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import Follow, Like, Post, User


def index(request):
    post_filter = request.GET.get('user', 'all')
    following_page = request.GET.get('flw', '0')
    ptitle = ""
    following = '0'
    followed_by = '0'
    am_following = 'Follow'
    
    if post_filter == 'all':
        posts = Post.objects.all()
        ptitle = 'All Posts'
    else:
        if following_page != '0':
            try:
                post_filter = Follow.objects.filter(user_id=post_filter).values_list('following', flat=True)
                print("Inside following", post_filter)
                ptitle = 'Following'
            except ObjectDoesNotExist:
                pass
        else:
            # For the profile page, get follow, followed_by, and me_follow
            ptitle = User.objects.get(id=post_filter)
            following = Follow.objects.filter(user_id=post_filter).count()
            followed_by = Follow.objects.filter(following=post_filter).count()
            if Follow.objects.filter(user_id=request.user.id, following=post_filter).count():
                am_following = "Unfollow"


        # Assume that we are passed a user
        posts = Post.objects.filter(user_id__in=post_filter)

    # Figure out likes - first, count up the number of likes per post
    fullpostlist = []
    posts = posts.order_by("-timestamp").all()
    for post in posts:
        like_dict = count_likes(post.id, request.user.id)
        fullpostlist.append({
            "id": post.id,
            "user": post.user.username,
            "user_id": post.user_id,
            "entry": post.entry,
            "timestamp": post.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "like":  like_dict['num_like'],
            "user_like": like_dict['user_like']
        })

    p = Paginator(fullpostlist, 10)
    ppg = p.page(request.GET.get('page', '1'))

    filter_value = request.GET.get('user', 'all')
    if filter_value != 'all':
        filter_value = int(filter_value)
    return render(request, 'network/index.html', {
        'flw': following_page,
        'ppg': ppg,
        'filter': filter_value,
        'ptitle': ptitle,
        "following": following,
        "followed_by": followed_by,
        'am_following': am_following
    })


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


def new_post(request):
    print("NP:", request.user.id)
    print("RE:", request.content_params)
    for key, value in request.POST.items():
        print(f'Key: {key}')
        print(f'Value: {value}')
    # Composing a new post must be via POST
    if request.method != "POST":
        # TBD update error condition
        return JsonResponse({"error": "POST request required."}, status=400)

    #  Add data checking here
    #data = json.loads(request.body)
    #user = User.objects.get(id=request.user.id)
    #entry = data.get("entry", "")

    if not request.POST["new_entry"]:
        # TBD needs to be changed for error condition
        return JsonResponse({"error": "Post cannot be empty."}, status=400)

    post = Post(
        user=User.objects.get(id=request.user.id),
        entry=request.POST["new_entry"]
    )
    post.save()
    return HttpResponseRedirect(reverse("index"))
    # return JsonResponse({"message": "Post logged successfully."}, status=201)


def count_likes(post_id, user_id):
    like_dict = {
        'num_like': 0,
        'user_like': 'Like'
        }
    try:
        # First, lets get the count
        like_dict['num_like'] = Like.objects.filter(post_id=post_id).count()
        # And then check to see if the user liked it
        try:
            Like.objects.get(post_id=post_id, user_id=user_id)
            like_dict['user_like'] = 'Unlike'
        except ObjectDoesNotExist:
            pass
    except ObjectDoesNotExist:
        pass
    return like_dict


@csrf_exempt
def change_follow(request):
    data = json.loads(request.body)
    try:
        follow_entry = Follow.objects.get(user_id=data['cur_user_id'], following_id=data['req_user_id'])
        follow_entry.delete()
    except Follow.DoesNotExist:
        follow_entry = Follow(
            user_id=data['cur_user_id'],
            following_id=data['req_user_id']
        )
        follow_entry.save()
    return HttpResponse(status=204)


@csrf_exempt
def change_like(request):
    data = json.loads(request.body)
    try:
        like_entry = Like.objects.get(user_id=data['cur_user_id'], post_id=data['post_id'])
        like_entry.delete()
    except ObjectDoesNotExist:
        like_entry = Like(
            user_id=data['cur_user_id'],
            post_id=data['post_id']
        )
        like_entry.save()
    return HttpResponse(status=204)


@csrf_exempt
def update_post(request):
    data = json.loads(request.body)
    Post.objects.filter(pk=data['id']).update(entry=data['entry'])
    return HttpResponse(status=204)
