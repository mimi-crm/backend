from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("", views.UserCreateView.as_view(), name="user_list_create"),
    path("info/", views.UserRetrieveUpdateDestroyAPIView.as_view(), name="info"),
]
