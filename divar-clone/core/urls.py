from django.urls import path, include
import core.views as views

app_name = "core"

urlpatterns = [
    path("", views.index_view, name="index"),
    path("users/", include("core.urls_dir.user_urls")),
    path("items/", include("core.urls_dir.item_urls")),
]
