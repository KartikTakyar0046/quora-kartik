from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
import json
from posts.models import Question
def homepage(request):
    context={}
    return render(request,'home.html',context)

def home(request):
    return render(request,'base.html')
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')
@login_required
def account_settings(request):
    profile_user=request.user.profile
    logged_in_user=request.user
    following=Follow.objects.filter(following=logged_in_user)

    followers=Follow.objects.filter(follower=logged_in_user)
    form=AccountSettings(instance=profile_user)
    questions=Question.objects.filter(author=logged_in_user)
    if request.method == 'POST':
        form = AccountSettings(request.POST,request.FILES,instance=profile_user)
        if form.is_valid():
            form.save()
    context={'form':form,'logged_in_user':logged_in_user,'following':following,'followers':followers,'questions':questions}
    return render(request,'profile.html',context)


def profilevisit(request,username):
    logged_user=request.user
    logged_profile=logged_user.profile
    user_visit=User.objects.get(username=username)
    profile_user=user_visit.profile
    if logged_user==user_visit:
        return redirect('profile')
    try:
        test = Follow.objects.get(follower=user_visit,following=logged_user)
    except Follow.DoesNotExist:
        test = None
    is_follow=False
    if test is not None:
        is_follow=True
    context={'user_visit':user_visit,'profile_user':profile_user,'is_follow':is_follow}
    return render(request,'profilevisit.html',context)


def following(request):
    logged_in_user=request.user
    questions=Question.objects.filter(author=logged_in_user)
    following=Follow.objects.filter(following=logged_in_user)
    followers=Follow.objects.filter(follower=logged_in_user)
    all_follow=Follow.objects.all()
    context={'following':following,'followers':followers,'all_follow':all_follow,
    'questions':questions}
    return render(request,'following.html',context)



