from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('signup/', views.UserSignUpView.as_view(), name='signup'),
    path('info/', views.UserRetrieveUpdateDestroyAPIView.as_view(), name='info'),
]