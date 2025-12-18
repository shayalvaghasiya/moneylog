from django.db import models
from django.conf import settings


# Account

# pre-defined account types 
class AccountType(models.TextChoices):
    BANK = "bank", "Bank"
    CASH = "cash", "Cash"
    CREDIT_CARD = "credit card", "Credit Card"
    WALLET = "wallet", "Wallet"

class Account(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="accounts")
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=AccountType.choices)
    opening_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # avoid duplicate account for same user
        constraints = [
            models.UniqueConstraint(fields=["user", "name"], name="unique_account_name_per_user")]

    def __str__(self):
        return f"{self.name} ({self.account_type})"


# Category 

class CategoryType(models.TextChoices):
    INCOME = "income", "Income"
    EXPENSE = "expense", "Expense"

class Category(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=10, choices=CategoryType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "name", "category_type"], name="unique_category_name_per_user_type")]

    def __str__(self):
        return f"{self.name} ({self.category_type})"
    


# Transaction

class TransactionType(models.TextChoices):
    INCOME = "income", "Income"
    EXPENSE = "expense", "Expense"

class Transaction(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="transactions")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="transactions")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TransactionType.choices)
    occured_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)

    def clean(self):
        if self.amount <=0:
            raise ValueError("Transaction amount must be greater than zero")
        
        if self.transaction_type != self.category.category_type:
            raise ValueError("Transaction type must match the category type")
    
    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"
    

# Budget

class BudgetPeriod(models.TextChoices):
    MONTHLY = "monthly", "Monthly"

class Budget(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="budgets")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="budgets")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    period = models.CharField(max_length=10, choices=BudgetPeriod.choices, default=BudgetPeriod.MONTHLY)
    start_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)


    def clean(self):
        if self.amount <=0:
            raise ValueError("Budget amount must be positive")
        
        if self.category.category_type != CategoryType.EXPENSE:
            raise ValueError("Budget can only be set for expense categories")
        
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "category", "period", "start_date"], name="unique_budget_per_user_category_period_start_date")]

    def __str__(self):
        return f"{self.category.name} - {self.amount} per {self.period}"
    
    
        