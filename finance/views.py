from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Account
from .services import (
    get_account_balance, 
    get_total_balance_for_user, 
    get_monthly_spend_by_category, 
    get_monthly_budget_report,
)

def dashboard(request):
    user = request.user

    accounts = Account.objects.filter(user=user)
    account_balances = []
    for account in accounts:
        account_balances.append({
            "name": account.name,
            "balance": get_account_balance(account)
        })
    
    context = {
        "total_balance": get_total_balance_for_user(user),
        "accounts": account_balances,
        "monthly_spend": get_monthly_spend_by_category(user),
        "budget_report": get_monthly_budget_report(user),
    }

    return render(request, "finance/dashboard.html", context)