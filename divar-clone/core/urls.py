from django.urls import path, include
from core.views_dir import general_views

app_name = "core"

urlpatterns = [
    path("", general_views.index_view, name="index"),
    path("users/", include("core.urls_dir.user_urls")),
    path("items/", include("core.urls_dir.item_urls")),
]
