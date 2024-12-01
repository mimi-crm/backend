

from django.urls import path

from customers.views import CustomerListCreateView, CustomerDetailView

app_name = 'customers'
urlpatterns = [
    path('',CustomerListCreateView.as_view(), name='customers'),
    path('<int:pk>/',CustomerDetailView.as_view(), name='customer-detail'),
]