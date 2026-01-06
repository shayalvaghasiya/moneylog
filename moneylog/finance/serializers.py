from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    account_name = serializers.SerializerMethodField()

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
    
    def get_category_name(self, obj):
        return obj.category.name
    
    def get_account_name(self, obj):
        return obj.account.name