from django.shortcuts import render
from core.models import Item
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
