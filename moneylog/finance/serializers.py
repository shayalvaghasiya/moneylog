from rest_framework import serializers
from .models import Transaction, Account, Category, Budget

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "name", "account_type", "opening_balance", "created_at"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "category_type", "created_at"]

class BudgetSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Budget
        fields = ["id", "category", "category_name", "amount", "period", "start_date", "created_at"]

    def get_category_name(self, obj):
        return obj.category.name

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