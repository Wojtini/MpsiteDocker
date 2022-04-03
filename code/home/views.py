import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewUserForm, EditProfileForm, EditUserForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.core.exceptions import ObjectDoesNotExist
from .models import Profile, Quote
from movierating.models import Review
from django.contrib.auth.models import Permission


@login_required
def index(request):
    return render(request, "home.html", context={"perm": get_user_permissions(request.user)})

@login_required
def servers_monitor(request):
    return render(request, "servers.html", {})

@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        quotes = Quote.objects.filter(user=user)
    except ObjectDoesNotExist:
        return render(request, "error.html")
    return render(request, "profile.html",
                  context={
                      "profile": profile,
                      "quotes": quotes,
                  })

@login_required
def edit_profile(request):
    instance = get_object_or_404(Profile, user=request.user)
    form = EditProfileForm(instance=instance)

    if request.POST:
        form = EditProfileForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("/editprofile")

    return render(request, "editprofile.html",
                  context={
                      'form': form,
                    })

@login_required
def edit_user(request):
    user_instance = get_object_or_404(User, id=request.user.id)
    user_form = EditUserForm(request.POST or None, instance=user_instance)
    if user_form.is_valid():
        user_form.save()
        return redirect("/edituser")

    return render(request, "editprofile.html",
                  context={
                      'form': user_form
                  })

@login_required
def personnel(request):
    all_users = User.objects.values()
    for user in all_users:
        quotes = Quote.objects.filter(user=user['id'])
        if len(quotes) == 0:
            user['quote'] = "No quotes"
        else:
            quote = random.choice(quotes)
            user['quote'] = quote.quote_text
        all_reviews = Review.objects.select_related().filter(user=user['id'])
        user['reviews_count'] = len(all_reviews)
        user['profile'] = Profile.objects.get(user=user['id'])
    return render(request, "personnel.html",
                  context={
                      "all_users_blocks": all_users,
                  })

def register_request(request):
    msg = ''
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            #messages.success(request, "Registration successful.")
            return redirect("/")
        #messages.error(request, "Unsuccessful registration. Invalid information.")
        msg = "Unsuccessful registration"
    form = NewUserForm()
    return render(request=request, template_name="register.html",
                  context={
                      "register_form": form,
                      "msg": msg,
                  })


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")


def get_user_permissions(user):
    if user.is_superuser:
        return Permission.objects.all()
    return user.user_permissions.all() | Permission.objects.filter(group__user=user)