from django.shortcuts import get_object_or_404, render, redirect
from core.models import Item
import api.views as api
from core.forms import ItemCreateForm
from django.contrib import messages


def item_list_view(request):
    return redirect("core:index")


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
    return render(request, "item/item_create.html", context=context)


def item_details_view(request, item_id: int):
    item = get_object_or_404(Item, pk=item_id)
    context = {"item": item}
    return render(request, "item/item_details.html", context=context)


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
    return render(request, "item/item_delete.html", context=context)


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
    return render(request, "item/item_buy.html", {"item": item})
