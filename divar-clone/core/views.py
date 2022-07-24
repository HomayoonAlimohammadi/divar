from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from core.models import Item
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
import api.views as api
from core.forms import ItemCreateForm, UserCreateForm, UserLoginForm, UserUpdateForm
from django.contrib import messages


def index_view(request, q=None):
    item_list = Item.objects.all()
    if request.method == "POST":
        q = request.POST.get("q")
        messages.add_message(
            request, messages.INFO, f"Showing search results containing: {q}"
        )
        item_list = Item.objects.filter(name__icontains=q)
    context = {
        "item_list": item_list,
    }
    return render(request, "index.html", context=context)


def user_register_view(request):
    form = UserCreateForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            password = form.cleaned_data["password"]
            password_conf = form.cleaned_data["password_conf"]
            if password != password_conf:
                messages.add_message(request, messages.ERROR, "Passwords do not match.")
                return redirect("core:user_register")
            try:
                user = form.save()
                login(request, user)
                messages.add_message(
                    request, messages.SUCCESS, "User was created successfully"
                )
            except Exception as e:
                messages.add_message(request, messages.ERROR, "Something went wrong...")
                print(e)
            return redirect("core:index")
    if request.user.is_authenticated:
        return redirect("core:user_details", request.user.pk)
    context = {"form": form, "type": "register"}
    return render(request, "user_create_update.html", context=context)


def user_list_view(request):
    user_list = User.objects.all()
    context = {"user_list": user_list}
    return render(request, "user_list.html", context=context)


def user_details_view(request, user_id: int):
    user = get_object_or_404(User, pk=user_id)
    context = {"user": user}
    return render(request, "user_details.html", context=context)


def user_login_view(request):
    if request.user.is_authenticated:
        return redirect("core:user_details", request.user.pk)

    form = UserLoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, "You have logged in.")
                return redirect("core:index")
            else:
                messages.add_message(request, messages.ERROR, "Invalid Credentials.")
    context = {"form": form}
    return render(request, "user_login.html", context=context)


def user_update_view(request):
    form = UserUpdateForm(request.POST or None)
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, "You have to log in first.")
        return redirect("core:user_login")
    if request.method == "POST":
        print("request method was post!")
        user = get_object_or_404(User, pk=request.user.pk)
        if form.is_valid():
            print("form is valid")
            new_data = {
                "first_name": form.cleaned_data.get("first_name"),
                "last_name": form.cleaned_data.get("last_name"),
                "username": form.cleaned_data.get("username"),
                "email": form.cleaned_data.get("email"),
            }
            password = form.cleaned_data.get("password")
            password_conf = form.cleaned_data.get("password_conf")
            if password != password_conf:
                messages.add_message(request, messages.ERROR, "Passwords do not match.")
            else:
                try:
                    for key, val in new_data.items():
                        print(f"this is now {key}: {val}, {type(val)}, {repr(val)}")
                        if val:
                            print(f"{key}: {val} was eddited")
                            setattr(user, key, val)
                    if password:
                        user.set_password(password)
                    user.save()
                    print("user was updated")
                    messages.add_message(
                        request, messages.SUCCESS, "Updated user data successfully."
                    )
                    logout(request)
                    login(request, user)
                except Exception as e:
                    messages.add_message(request, messages.ERROR, str(e))
                return redirect("core:user_details", request.user.pk)
        else:
            messages.add_message(request, messages.ERROR, "Form was not valid!")
    context = {"form": form, "type": "update"}
    return render(request, "user_create_update.html", context=context)


def user_logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.add_message(request, messages.INFO, "You have been logged out.")
        return redirect("core:index")
    return render(request, "user_logout.html")


def item_create_view(request):
    if not request.user.is_authenticated:
        return redirect("core:user_login")

    form = ItemCreateForm(request.POST, request.FILES or None)
    if request.method == "POST":
        print(request.FILES)
        if form.is_valid():
            try:
                print(form.cleaned_data)
                item = Item(**form.cleaned_data)
                item.user = request.user
                item.save()
                messages.add_message(request, messages.SUCCESS, "Item was Created.")
            except Exception as e:
                messages.add_message(request, messages.ERROR, "Something went wrong...")
                print(e)
            return redirect("core:index")
    context = {"form": form}
    return render(request, "item_create.html", context=context)


def item_details_view(request, item_id: int):
    item = get_object_or_404(Item, pk=item_id)
    context = {"item": item}
    return render(request, "item_details.html", context=context)


def item_delete_view(request, item_id: int):
    if request.method == "POST":
        if request.user.is_authenticated:
            item = get_object_or_404(Item, pk=item_id)
            if request.user == item.user:
                item.delete()
                messages.add_message(
                    request, messages.SUCCESS, "Item was deleted successfully."
                )
                return redirect("core:index")
            else:
                messages.add_message(
                    request, messages.ERROR, "You can only delete your own items!"
                )
        else:
            messages.add_message(request, messages.ERROR, "You have to login first.")
            return redirect("core:user_login")

    item = get_object_or_404(Item, pk=item_id)
    context = {"item": item}
    return render(request, "item_delete.html", context=context)


def item_buy_view(request, item_id: int):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == "POST":
        res = api.pay_for_item(item.price)
        if res.status_code == 200:
            item.delete()
            messages.add_message(
                request, messages.SUCCESS, "Item was bought successfully!"
            )
            return redirect("core:index")
        else:
            messages.add_message(request, messages.ERROR, "Something went wrong!")
    return render(request, "item_buy.html", {"item": item})


def user_item_list_view(request, user_id: int):
    item_list = Item.objects.all().filter(user__pk=user_id)
    context = {
        "item_list": item_list,
    }
    messages.add_message(
        request, messages.INFO, f"Showing items owned by: {request.user.username}"
    )
    return render(request, "index.html", context=context)
