from django.urls import path

from counsels.views import CounselListCreateView, CounselDetailView

app_name = 'counsels'
urlpatterns = [
    path('',CounselListCreateView.as_view(), name='list'),
    path('<int:pk>/',CounselDetailView.as_view(), name='detail'),
]