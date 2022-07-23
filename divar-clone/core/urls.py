from django.urls import path 
import core.views as views

app_name = 'core'

urlpatterns = [
    path('', views.index_view, name='index'),

    path('users/', views.user_list_view, name='user_list'),
    path('users/register', views.user_register_view, name='user_register'),
    path('users/login', views.user_login_view, name='user_login'),
    path('users/logout', views.user_logout_view, name='user_logout'),
    path('users/my-items', views.user_item_list_view, name='user_item_list'),
    path('users/<int:user_id>/', views.user_details_view, name='user_details'),

    path('items/', views.item_list_view, name='item_list'),
    path('items/create', views.item_create_view, name='item_create'),
    path('items/<int:item_id>/', views.item_details_view, name='item_details'),
    path('items/<int:item_id>/delete', views.item_delete_view, name='item_delete'),
]
