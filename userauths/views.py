from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from userauths.forms import UserRegisterForm
from userauths.models import User


def register_user(request):
    if request.method == "POST":
        print(request.POST)
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            print("valid")
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"{username} created")
            new_user = authenticate(
                username=form.cleaned_data["email"],
                password=form.cleaned_data["password1"],
            )
            login(request, new_user)
            return redirect("userauths:login")
    form = UserRegisterForm()
    context = {"form": form}
    return render(request, "userauths/register.html", context)


def login_user(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("payment:index")
            else:
                messages.warning(request, "Invalid username or password")
                return redirect("payment:login")
        except:
            messages.warning(request, "User does not exist")
            return render(request, "userauths/login.html")
    return render(request, "userauths/login.html")


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("userauths:login")
