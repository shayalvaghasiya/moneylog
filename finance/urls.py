from django.urls import path
from .views import dashboard, add_transaction, edit_transaction


urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("add/", add_transaction, name="add_transaction"),
    path("edit/<int:pk>/", edit_transaction, name="edit_transaction"),
]


