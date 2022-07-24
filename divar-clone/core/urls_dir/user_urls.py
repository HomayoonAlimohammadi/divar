from django.urls import path
from core import views

urlpatterns = [
    path("", views.user_list_view, name="user_list"),
    path("register", views.user_register_view, name="user_register"),
    path("login", views.user_login_view, name="user_login"),
    path("logout", views.user_logout_view, name="user_logout"),
    path("update", views.user_update_view, name="user_update"),
    path("<int:user_id>/", views.user_details_view, name="user_details"),
    path("<int:user_id>/items", views.user_item_list_view, name="user_item_list"),
]
