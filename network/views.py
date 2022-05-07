from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import json
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import PostForm
from .models import User, Post, Follower, Like


def index(request):
    disp_EditForm = 'none'
    myPostForm=  PostForm()
    post_list=Post.objects.all().order_by('-date')
    if request.method =='POST':
        myPostForm=PostForm(request.POST)
        if myPostForm.is_valid():
            myPostForm.instance.user=request.user
            myPostForm.instance.date=datetime.now()
            myPostForm.save()
            return redirect('index')

    post_list_paginator=retPaginatorList(request,post_list)
    return render(request, "network/index.html", {'PostForm':myPostForm,'post_list':post_list_paginator,'p':'p', "disp_EditForm":disp_EditForm})


def Find_no_of_follower(profile_user):
    following=Follower.objects.all().filter(user=profile_user)
    f_list=[]
    no_follower=0
    for item in following:
        f_list.append((item.user_follower))

    for us in f_list:
        if Follower.objects.all().filter(user=us,user_follower=profile_user):
            no_follower+= 1

    return no_follower


def view_profile(request, id):
    fol_unfol='follow'
    disp_EditForm='none'
    no_follower=0
    profile_user=User.objects.all().get(id=id)
    post_list=Post.objects.all().filter(user=profile_user)
    tot_following = Follower.objects.filter(user=profile_user).count()
    no_follower=Find_no_of_follower(profile_user)
    if profile_user== request.user:
        disp='none'
    else:
        disp='block'
        test_follow = Follower.objects.all().filter(user=request.user, user_follower=profile_user)
        if test_follow:
            fol_unfol = 'unfollow'
        else:
            fol_unfol = 'follow'
    post_list_paginator = retPaginatorList(request,post_list)
    return render(request,'network/profile.html',{'post_list':post_list_paginator
        ,'disp_follow':disp,
         'fol_unfol':fol_unfol,
        'profile_user':profile_user,
        'no_following':tot_following,
        'no_follower':no_follower,
        "disp_EditForm":disp_EditForm


          })

def follow_check(request,pro_id):
    prof_user=User.objects.all().get(id=pro_id)
    res=Follower.objects.filter(user=request.user,user_follower=prof_user)
    print(res)
    if res:
        res.delete()
    else:
        Follower.objects.create(
            user=request.user,
            user_follower=prof_user
        )
    return HttpResponseRedirect(reverse('view-profile', args=(pro_id,)))



def view_following_posts(request):
    my_posts=Post.objects.all().filter(user=None)
    following_list=Follower.objects.all().filter(user=request.user)
    print("following list",following_list)
    for item in following_list:
        my_posts|=Post.objects.all().filter(user=item.user_follower)

    my_posts=my_posts.order_by('-date')
    print('total following posts',my_posts)
    post_list_paginator = retPaginatorList(request,my_posts)
    return render (request,'network/following_posts.html',{'post_list':post_list_paginator})



@csrf_exempt
@login_required
def likePost(request,post_id):
    try:
        post = Post.objects.all().get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)
    if request.method == "GET":
        return JsonResponse(post.serialize())
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("like") is not None:
            res = Like.objects.filter(user=request.user, posts=post)
            print(res)
            if res:
                res.delete()
                post.likes = post.likes - 1
                btn_status='like'
            else:
                Like.objects.create(
                    user=request.user,
                    posts=post)
                post.likes = post.likes + 1
                btn_status='unlike'
        post.save()

        return HttpResponse({'btn_status':btn_status}, status=204)
    else:
        return JsonResponse({ "error": "GET or PUT request required."}, status=400)





@csrf_exempt
@login_required
def edit_post(request, id):
    # Get contents of email
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    body = data.get("body", "")
    print('post body is', body)
    try:
        post = Post.objects.all().get(id=id, user=request.user)
        post.post_body = body
        post.date = datetime.now()
        post.save()
        return JsonResponse({"message": "Email sent successfully."}, status=201)
    except Post.DoesNotExist:
        return JsonResponse({
            "error": f"post with id {id} does not exist."
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


def testPaginator(request):
    user_list=User.objects.all()
    page=request.GET.get('page')
    mypge=Paginator(user_list, 8)
    try:
        users = mypge.page(page)
    except PageNotAnInteger:
        users = mypge.page(1)
    except EmptyPage:
        users = mypge.page(mypge.num_pages)

    return render(request, 'network/paginator_test.html', {'users': users})

def retPaginatorList(request, queryList):
    page = request.GET.get('page')
    mypge = Paginator(queryList, 4)
    try:
        resultList = mypge.page(page)
    except PageNotAnInteger:
        resultList = mypge.page(1)
    except EmptyPage:
        resultList = mypge.page(mypge.num_pages)

    return  resultList
