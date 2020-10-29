from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.db import IntegrityError

from django import forms
from django.core.paginator import Paginator


from .models import User, Post, Like, Follow


class PostForm(forms.Form):
    post = forms.CharField(
        initial="Share with your friends!!", widget=forms.Textarea)


class followform(forms.Form):
    follow = forms.BooleanField(required=False)


def index(request):
    if request.user.is_authenticated:
        posts = Post.objects.order_by("-timestamp").all()
        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        if len(Like.objects.all()) > 0:
            return render(request, "network/index.html", {
                "AllPosts": posts,
                "active_user": request.user,
                "liked": Like.objects.filter(user=request.user)
            })
        else:
            return render(request, "network/index.html", {
                "AllPosts": posts,
                "active_user": request.user,
            })
    else:
        return render(request, "network/index.html", {
            "AllPosts": Post.objects.order_by("-timestamp").all(),
            "active_user": request.user,
        })


def profile(request, user_id):
    if request.method == 'POST':
        form = followform(request.POST)
        if form.is_valid:
            item = User.objects.get(pk=user_id)
            connection = Follow(user=request.user, following=item)
            connection.save()
        return HttpResponseRedirect(reverse("UserProfile", args=[user_id]))
    else:
        posts = Post.objects.filter(user=user_id).order_by("-timestamp")
        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        return render(request, "network/profile.html", {
            "User": User.objects.get(pk=user_id),
            "AllPosts": posts,
            "followers": len(Follow.objects.filter(user=user_id)),
            "following": len(Follow.objects.filter(following=user_id)),
            "unfollow": Follow.objects.filter(user=request.user, following=user_id),
            "form": followform(),
            "active_user": request.user
        })


@login_required
def following(request):
    listA = []
    listB = []
    listC = []
    fltr = Follow.objects.filter(user=request.user)
    posts = Post.objects.order_by("-timestamp").all()
    for item in fltr:
        listB.append(item.following)
    for entry in posts:
        listA.append(entry.user)
    for post in posts:
        if post.user in listA and post.user in listB:
            listC.append(post)
    print(listA)
    print(listB)
    print(listC)
    posts = listC
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, "network/following.html", {
        "AllPosts": posts
    })


@login_required
def AllFollowers(request):
    # Filter emails returned based on mailbox
    follower = Follow.objects.filter(user=request.user)
    # Return emails in reverse chronologial order
    following = follower.order_by('id')
    return JsonResponse([follower.serialize() for follower in following], safe=False)


@csrf_exempt
@login_required
def Follower(request, follower_id):

    # Query for requested email
    try:
        follower = Follow.objects.get(user=request.user, following=follower_id)
    except Follow.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse(follower.serialize())

    # Update whether email is read or should be archived
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("true") is not None:
            follower.read = data["true"]
            follower.save
            if follower.read == False:
                follower.delete()
        return HttpResponse(status=204)

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


@ login_required
def newpost(request):
    return render(request, "network/newpost.html", {
        "form": PostForm()
    })


@ login_required
def CreateNewPost(request):
    forms = PostForm(request.POST)
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    else:
        if forms.is_valid():
            post = forms.cleaned_data['post']
            Save = Post(user=request.user, body=post)
            Save.save()
            return HttpResponseRedirect(reverse("index"))


@ csrf_exempt
@ login_required
def AllPosts(request):
    # Filter emails returned based on mailbox
    post = Post.objects.all()
    # Return emails in reverse chronologial order
    posts = post.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)


@ csrf_exempt
@ login_required
def post(request, post_id):    # Query for requested email
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update whether email is read or should be archived
    elif request.method == "PUT":
        post = Post.objects.get(id=post_id)
        data = json.loads(request.body)
        if data.get("likes") is not None:
            x1 = int(data["likes"])
            if x1 > post.likes:
                post = Post.objects.get(pk=post_id)
                like = Like(user=request.user, item=post)
                like.save()
                post.likes = post.likes + 1
            else:
                item = Like.objects.get(user=request.user, item=post_id)
                if item:
                    item.delete()
                    post.likes = post.likes - 1

        if data.get("body") is not None:
            post.body = str(data["body"])
        post.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


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
