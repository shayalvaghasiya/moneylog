from django.urls import path
from .views import (
    transaction_detail_api, 
    transaction_list_api, 
    dashboard_api, 
    register_api,
    account_list_api,
    account_detail_api,
    category_list_api,
    category_detail_api,
    budget_list_api,
    budget_detail_api
)

urlpatterns = [
    path("api/register/", register_api, name="register_api"),
    path("api/dashboard/", dashboard_api, name="dashboard_api"),
    path("api/transactions/", transaction_list_api, name="transaction_list_api"),    
    path("api/transactions/<int:pk>/", transaction_detail_api, name="transaction_detail_api"),
    path("api/accounts/", account_list_api, name="account_list_api"),
    path("api/accounts/<int:pk>/", account_detail_api, name="account_detail_api"),
    path("api/categories/", category_list_api, name="category_list_api"),
    path("api/categories/<int:pk>/", category_detail_api, name="category_detail_api"),
    path("api/budgets/", budget_list_api, name="budget_list_api"),
    path("api/budgets/<int:pk>/", budget_detail_api, name="budget_detail_api"),
]
