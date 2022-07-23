from django.shortcuts import get_object_or_404, render, redirect 
from core.models import Item 
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User


def index_view(request, message=None):
    item_list = Item.objects.all()
    context = {
        'item_list': item_list,
        'message': message
    }
    return render(request, 'index.html', context=context)


def user_register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_conf = request.POST.get('password_conf')
        if password != password_conf:
            return render(request, 'user_register.html')
        try:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
        except:
            print('something went wrong')
        return redirect('core:index')
    if request.user.is_authenticated:
        return redirect('core:user_details', request.user.pk)
    return render(request, 'user_register.html')

def user_list_view(request):
    user_list = User.objects.all()
    context = {
        'user_list': user_list
    }
    return render(request, 'user_list.html', context=context)

def user_details_view(request, user_id: int):
    if request.user.is_authenticated and request.user.pk == user_id:
        user = get_object_or_404(User, pk=user_id)
        return render(request, 'user_details.html')
    return redirect('core:index')
    
def user_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return redirect('core:user_login')
        # user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('core:index')
    if request.user.is_authenticated:
        return redirect('core:user_details', request.user.pk)
    return render(request, 'user_login.html')

def user_logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('core:index')
    return render(request, 'user_logout.html')

def item_list_view(request):
    item_list = Item.objects.all()
    if request.method == 'POST':
        item_list = Item.objects.filter(name__icontains=request.POST.get('q'))
    
    context = {
        'item_list': item_list
    }

    return render(request, 'index.html', context=context)

def item_create_view(request):
    is_user_auth = request.user.is_authenticated
    if request.method == 'POST' and is_user_auth:
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        user = request.user
        try:
            item = Item.objects.create(
                name=name, description=description, price=price, user=user
            )
        except Exception as e:
            print(e)
            print('\nsomething went wrong!\n')
        return redirect("core:index")
    if is_user_auth:
        return render(request, 'item_create.html')
    return redirect('core:user_login')

def item_details_view(request, item_id: int):
    item = get_object_or_404(Item, pk=item_id)
    context = {
        'item': item
    }
    return render(request, 'item_details.html', context=context)

def item_delete_view(request, item_id: int):
    if request.method == 'POST':
        if request.user.is_authenticated:
            item = get_object_or_404(Item, pk=item_id)
            if request.user == item.user:
                item.delete()
                return redirect('core:index')

    item = get_object_or_404(Item, pk=item_id)
    context = {'item': item}
    return render(request, 'item_delete.html', context=context)

def item_buy_view(request, item_id: int):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        res = api_pay(item.price)
        if res:
            item.delete()
            return redirect('core:index')
    return render(request, 'item_buy.html', {'item': item})

def user_item_list_view(request):
    item_list = Item.objects.all().filter(user=request.user)
    context = {
        'item_list': item_list,
    }
    return render(request, 'index.html', context=context)

    
def api_pay(item_price):
    return True