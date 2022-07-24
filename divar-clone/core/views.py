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
            request, messages.INFO, f"Showing search results containing: `{q}`"
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
    return render(request, "user_login.html", context=context)


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
                request, messages.SUCCESS, "Updated user data successfully."
            )
            return redirect("core:user_details", request.user.pk)
        else:
            messages.add_message(request, messages.ERROR, "Invalid inputs!")
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
            print(form.cleaned_data)
            item = Item(**form.cleaned_data)
            item.user = request.user
            item.save()
            messages.add_message(request, messages.SUCCESS, "Item was Created.")
            return redirect("core:index")
        else:
            messages.add_message(
                request, messages.ERROR, "Invalid inputs for the Item."
            )
    context = {"form": form}
    return render(request, "item_create.html", context=context)


def item_details_view(request, item_id: int):
    item = get_object_or_404(Item, pk=item_id)
    context = {"item": item}
    return render(request, "item_details.html", context=context)


def item_delete_view(request, item_id: int):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, "You should login first.")
        return redirect("core:user_login")

    item = get_object_or_404(Item, pk=item_id)
    if request.user != item.user:
        messages.add_message(
            request, messages.ERROR, "You can only delete items you own."
        )
        return redirect("core:index")

    if request.method == "POST":
        item.delete()
        messages.add_message(
            request, messages.SUCCESS, "Item was deleted successfully."
        )
        return redirect("core:index")
    context = {"item": item}
    return render(request, "item_delete.html", context=context)


def item_buy_view(request, item_id: int):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == "POST":
        res = api.pay_for_item(item.price)
        if res.status_code != 200:
            messages.add_message(request, messages.ERROR, "Something went wrong!")
            return redirect("core:item_buy", {"item_id", item_id})
        item.delete()
        messages.add_message(request, messages.SUCCESS, "Item was bought successfully!")
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
