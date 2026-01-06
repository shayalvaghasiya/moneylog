from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Account, Transaction, Category
from .forms import TransactionForm
from .serializers import TransactionSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from rest_framework.pagination import PageNumberPagination



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


@api_view(["GET", "POST"])
def trasaction_list_api(request):
    user = request.user

    if request.method == "GET":
        transactions = get_filtered_transactions(user, request.GET)
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(transactions, request)
        serializer = TransactionSerializer(transactions, many=True)

        return paginator.get_paginated_response(serializer.data)

    if request.method == "POST":
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save(user=user)
            return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated, IsOwner])
def transaction_detail_api(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)

    # Object-level permission check happens here
    if request.method == "GET":
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = TransactionSerializer(
            transaction,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == "DELETE":
        transaction.delete()
        return Response(status=204)
