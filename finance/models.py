from django.db import models
from django.conf import settings

# pre-defined account types 
class AccountType(models.TextChoices):
    BANK = "bank", "Bank"
    CASH = "cash", "Cash"
    CREDIT_CARD = "credit card", "Credit Card"
    WALLET = "wallet", "Wallet"


# Account
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
