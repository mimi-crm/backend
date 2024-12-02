from counsels.views import CounselDetailView, CounselListCreateView
from django.urls import path

app_name = "counsels"
urlpatterns = [
    path("", CounselListCreateView.as_view(), name="list"),
    path("<int:pk>/", CounselDetailView.as_view(), name="detail"),
]
