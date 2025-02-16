from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages


def user_login(request):
    # Get "next" from GET or POST, default to "/"
    next_url = request.GET.get("next") or request.POST.get("next") or "/"

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(next_url)
        else:
            messages.error(request, "Invalid credentials")

    # Pass the next URL to the template
    return render(request, "login.html", {"next": next_url})


def user_logout(request):
    logout(request)
    return redirect("login")
