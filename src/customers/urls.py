from customers.views import CustomerDetailView, CustomerListCreateView
from django.urls import path

app_name = "customers"
urlpatterns = [
    path("", CustomerListCreateView.as_view(), name="customers"),
    path("<int:pk>/", CustomerDetailView.as_view(), name="customer-detail"),
]
