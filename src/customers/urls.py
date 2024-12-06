from customers.views import (CustomerDetailView, CustomerListCreateView,
                             CustomerSecurityEditView)
from django.urls import path

app_name = "customers"
urlpatterns = [
    path("", CustomerListCreateView.as_view(), name="customers"),
    path("<int:pk>/", CustomerDetailView.as_view(), name="customer-detail"),
    path(
        "<int:pk>/security/",
        CustomerSecurityEditView.as_view(),
        name="customer-security-edit",
    ),
]
