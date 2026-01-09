from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Account, Transaction, Category
from .serializers import TransactionSerializer
from .permissions import IsOwner

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination

from .services import (
    get_account_balance, 
    get_total_balance_for_user, 
    get_monthly_spend_by_category, 
    get_monthly_budget_report,
    get_filtered_transactions,
)

@api_view(["POST"])
@permission_classes([AllowAny])
def register_api(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    User.objects.create_user(username=username, password=password)
    return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_api(request):
    user = request.user

    accounts = Account.objects.filter(user=user)
    account_balances = [
        {
            "name": account.name,
            "balance": get_account_balance(account),
        }
        for account in accounts
    ]
    
    data = {
        "total_balance": get_total_balance_for_user(user),
        "accounts": account_balances,
        "monthly_spend": get_monthly_spend_by_category(user),
        "budget_report": get_monthly_budget_report(user),
        "categories": Category.objects.filter(user=user, category_type="expense").values("id", "name"),
    }

    return Response(data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def trasaction_list_api(request):
    user = request.user

    if request.method == "GET":
        transactions = get_filtered_transactions(user, request.GET)
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(transactions, request)
        serializer = TransactionSerializer(page, many=True)

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
