from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction, Category
from .forms import TransactionForm
from django.core.paginator import Paginator
from datetime import datetime

from .services import (
    get_account_balance, 
    get_total_balance_for_user, 
    get_monthly_spend_by_category, 
    get_monthly_budget_report,
    get_filtered_transactions,
)

@login_required
def dashboard(request):
    user = request.user

    accounts = Account.objects.filter(user=user)
    account_balances = []
    for account in accounts:
        account_balances.append({
            "name": account.name,
            "balance": get_account_balance(account)
        })
    
    transactions_qs = get_filtered_transactions(user, request.GET)
    paginator = Paginator(transactions_qs, 10)
    page_number = request.GET.get("page")
    transactions = paginator.get_page(page_number)

    context = {
        "total_balance": get_total_balance_for_user(user),
        "accounts": account_balances,
        "monthly_spend": get_monthly_spend_by_category(user),
        "budget_report": get_monthly_budget_report(user),
        "transactions": transactions,
        "categories": Category.objects.filter(user=user, category_type="expense"),
    }

    return render(request, "finance/dashboard.html", context)


@login_required
def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect("dashboard")
    else:
        form = TransactionForm()

    return render(request, "finance/add_transaction.html", {"form": form})
           

@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(
        Transaction, pk=pk, user=request.user
    )

    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = TransactionForm(instance=transaction)
    
    return render(request, "finance/edit_transaction.html", {"form": form})


@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(
        Transaction, pk=pk, user=request.user
    )
    
    if request.method == "POST":
        transaction.delete()
        return redirect("dashboard")
    
    return render(request, "finance/delete_transaction.html", {"transaction": transaction})