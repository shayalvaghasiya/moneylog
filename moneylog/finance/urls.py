from django.urls import path
from .views import transaction_detail_api, transaction_list_api, dashboard_api, register_api

urlpatterns = [
    path("api/register/", register_api, name="register_api"),
    path("api/dashboard/", dashboard_api, name="dashboard_api"),
    path("api/transactions/", transaction_list_api, name="transaction_list_api"),    
    path("api/transactions/<int:pk>/", transaction_detail_api, name="transaction_detail_api")
]
