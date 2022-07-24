from django.urls import path
from core import views


urlpatterns = [
    path("", views.index_view, name="index"),
    path("<int:item_id>/", views.item_details_view, name="item_details"),
    path("<int:item_id>/delete", views.item_delete_view, name="item_delete"),
    path("create", views.item_create_view, name="item_create"),
    path("buy/<int:item_id>", views.item_buy_view, name="item_buy"),
]
