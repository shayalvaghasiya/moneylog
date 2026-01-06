from django.urls import path
from .views import dashboard, add_transaction, edit_transaction, delete_transaction, transaction_detail_api
from .views import trasaction_list_api

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("add/", add_transaction, name="add_transaction"),
    path("edit/<int:pk>/", edit_transaction, name="edit_transaction"),
    path("delete/<int:pk>/", delete_transaction, name="delete_transaction"),
    path("api/transactions/", trasaction_list_api, name="transaction_list_api"),    
    path("api/transactions/<int:pk>/", transaction_detail_api, name="transaction_detail_api")
]


