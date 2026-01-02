from django.urls import path
from .views import dashboard, add_transaction

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("add/", add_transaction, name="add_transaction"),
]


