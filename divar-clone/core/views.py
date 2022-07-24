from time import sleep
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from core.models import Item
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
import api.views as api
from core.forms import ItemCreateForm, UserCreateUpdateForm, UserLoginForm
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
    form = UserCreateUpdateForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            password_conf = form.cleaned_data["password_conf"]
            if password != password_conf:
                messages.add_message(request, messages.ERROR, "Passwords do not match.")
                return redirect("core:user_register")
            try:
                user = User.objects.create_user(  # type: ignore
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                )
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
    context = {"form": form}
    return render(request, "user_register.html", context=context)


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
    return HttpResponse("Updated! are hatman!")


def user_logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.add_message(request, messages.INFO, "You have been logged out.")
        return redirect("core:index")
    return render(request, "user_logout.html")


def item_create_view(request):
    if not request.user.is_authenticated:
        return redirect("core:user_login")

    form = ItemCreateForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data.get("description")
            image = form.cleaned_data.get("image")
            price = form.cleaned_data["price"]
            user = request.user
            try:
                item = Item.objects.create(
                    name=name,
                    description=description,
                    price=price,
                    user=user,
                    image=image,
                )
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
                return redirect("core:index")

    item = get_object_or_404(Item, pk=item_id)
    context = {"item": item}
    return render(request, "item_delete.html", context=context)


def item_buy_view(request, item_id: int):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == "POST":
        res = api.pay_for_item(item.price)
        if res.status_code == 200:
            item.delete()
            return redirect("core:index")
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
