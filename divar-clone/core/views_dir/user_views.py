from django.shortcuts import get_object_or_404, render, redirect
from core.models import Item
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from core.forms import UserCreateForm, UserLoginForm, UserUpdateForm
from django.contrib import messages


def user_register_view(request):
    form = UserCreateForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.add_message(
                request, messages.SUCCESS, "User was created successfully"
            )
            return redirect("core:index")
        else:
            messages.add_message(request, messages.ERROR, "Invalid Inputs.")
            return redirect("core:user_register")
    if request.user.is_authenticated:
        return redirect("core:user_details", request.user.pk)
    context = {"form": form, "type": "register"}
    return render(request, "user/user_create_update.html", context=context)


def user_list_view(request):
    user_list = User.objects.all()
    context = {"user_list": user_list}
    return render(request, "user/user_list.html", context=context)


def user_details_view(request, user_id: int):
    user = get_object_or_404(User, pk=user_id)
    context = {"user": user}
    return render(request, "user/user_details.html", context=context)


def user_login_view(request):
    if request.user.is_authenticated:
        return redirect("core:user_details", request.user.pk)

    form = UserLoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            # username = form.cleaned_data["username"]
            # password = form.cleaned_data["password"]
            # user = authenticate(username=username, password=password)
            user = authenticate(**form.cleaned_data)
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, "You have logged in.")
                return redirect("core:index")
            else:
                messages.add_message(request, messages.ERROR, "Invalid Credentials.")
    context = {"form": form}
    return render(request, "user/user_login.html", context=context)


def user_update_view(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, "You have to log in first.")
        return redirect("core:user_login")

    form = UserUpdateForm(request.POST or None)
    if request.method == "POST":
        user = get_object_or_404(User, pk=request.user.pk)
        if form.is_valid():
            new_data = {
                "first_name": form.cleaned_data.get("first_name"),
                "last_name": form.cleaned_data.get("last_name"),
                "username": form.cleaned_data.get("username"),
                "email": form.cleaned_data.get("email"),
            }
            password = form.cleaned_data.get("password")
            for key, val in new_data.items():
                if val:
                    print(f"{key}: {val} was eddited")
                    setattr(user, key, val)
            if password:
                user.set_password(password)
            user.save()
            logout(request)
            login(request, user)
            messages.add_message(
                request, messages.SUCCESS, "Updated user data successfu<lly."
            )
            return redirect("core:user_details", request.user.pk)
        else:
            messages.add_message(request, messages.ERROR, "Invalid inputs!")
    context = {"form": form, "type": "update"}
    return render(request, "user/user_create_update.html", context=context)


def user_logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.add_message(request, messages.INFO, "You have been logged out.")
        return redirect("core:index")
    return render(request, "user/user_logout.html")


def user_item_list_view(request, user_id: int):
    item_list = Item.objects.all().filter(user__pk=user_id)
    context = {
        "item_list": item_list,
    }
    messages.add_message(
        request, messages.INFO, f"Showing items owned by: {request.user.username}"
    )
    return render(request, "index.html", context=context)
