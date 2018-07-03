# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import User, Friend
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request, 'login/index.html')


def register(request):
    result = User.objects.validate_registration(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    # Creates a friend object on registration
    current_user = User.objects.get(id=request.session['user_id'])
    Friend.objects.create(current_user=current_user)
    messages.success(request, "Successfully registered!")
    return HttpResponseRedirect(reverse("login:home"))


def login(request):
    result = User.objects.validate_login(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Successfully logged in!")
    return HttpResponseRedirect(reverse("login:home"))


def logout(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')


def show(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')

    user = User.objects.get(id=user_id)
    context = {
       'user': user,
    }
    return render(request, 'login/show.html', context)


def home(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        current_user = User.objects.get(id=request.session['user_id'])
        others = User.objects.exclude(id=request.session['user_id'])
        friend = Friend.objects.get(current_user=current_user)
        friends = friend.users.all()
        context = {
            'user': current_user,
            'others': others,
            'friends': friends
        }
        return render(request, 'home/home.html', context)


def add_friend(request, friend_id):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        friend = User.objects.get(id=friend_id)
        current_user = User.objects.get(id=request.session['user_id'])
        Friend.add_friend(current_user, friend)
        return redirect('login:home')


def lose_friend(request, friend_id):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        friend = User.objects.get(id=friend_id)
        current_user = User.objects.get(id=request.session['user_id'])
        Friend.lose_friend(current_user, friend)
        return redirect('login:home')


