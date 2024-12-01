from django.urls import path

from oauth import views

app_name = 'oauth'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('refresh/', views.TokenRefreshView.as_view(), name='refresh'),
]