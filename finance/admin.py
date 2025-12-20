from django.contrib import admin
from .models import Account, Category, Transaction, Budget

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("name", "account_type", "opening_balance", "user", "created_at")
    list_filter = ("account_type", )
    search_fields = ("name", )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category_type", "user", "created_at")
    list_filter = ("category_type", )
    search_fields = ("name", )

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("transaction_type", "amount", "category", "account", "user", "occurred_at",)
    list_filter = ("transaction_type", "category", "account", )
    search_fields = ("note", )
    date_hierarchy = "occurred_at"

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("category", "amount", "period", "start_date", "user",)
    list_filter = ("period", )
    