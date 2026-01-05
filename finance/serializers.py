from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)
    account = serializers.CharField(source="account.name", read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id", 
            "transaction_type",
            "amount", 
            "category",
            "category_name",
            "account",
            "account_name",
            "occurred_at",
            "note",
        ]