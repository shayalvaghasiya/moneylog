from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")
    account = serializers.CharField(source="account.name")

    class Meta:
        model = Transaction
        fields = [
            "id", 
            "transaction_type",
            "amount", 
            "category",
            "account",
            "occurred_at",
            "note",
        ]