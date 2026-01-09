from django.urls import path
from .views import transaction_detail_api, trasaction_list_api, dashboard_api

urlpatterns = [
    path("api/dashboard/", dashboard_api, name="dashboard_api"),
    path("api/transactions/", trasaction_list_api, name="transaction_list_api"),    
    path("api/transactions/<int:pk>/", transaction_detail_api, name="transaction_detail_api")
]


