from django.db.models import Sum 
from django.utils import timezone

from .models import Account, Transaction, Budget

# services for views (some common logics, tasks)

def get_account_balance(account):
    
    income = (Transaction.objects.filter(account=account, transaction_type="income").aggregate(total=Sum("amount"))["total"] or 0)
    expense = (Transaction.objects.filter(account=account, transaction_type="expense").aggregate(total=Sum("amount"))["total"] or 0)

    return account.opening_balance + income - expense


def get_total_balance_for_user(user):

    total_opening = Account.objects.filter(user=user).aggregate(total=Sum("opening_balance"))["total"] or 0
    income = Transaction.objects.filter(user=user, transaction_type="income").aggregate(total=Sum("amount"))["total"] or 0
    expense = Transaction.objects.filter(user=user, transaction_type="expense").aggregate(total=Sum("amount"))["total"] or 0

    return total_opening + income - expense


def get_monthly_spend_by_category(user, date=None):

    if date is None:
        date = timezone.now()
    
    start_of_month = date.replace(day=1, hour=0, minute=0, second=0)

    return (Transaction.objects.filter(user=user, transaction_type="expense", occurred_at__gte=start_of_month).values("category__name").annotate(total=Sum("amount")).order_by("-total"))


def get_monthly_budget_report(user, date=None):
    if date is None:
        date = timezone.now()

    start_of_month = date.replace(day=1, hour=0, minute=0, second=0)
    budgets = Budget.objects.filter(user=user, period="monthly", start_date__lte=date.date())

    report = []
    for budget in budgets:
        spent = (Transaction.objects.filter(user=user, category=budget.category, transaction_type="expense", occurred_at__gte=start_of_month).aggregate(total=Sum("amount"))["total"] or 0)
        report.append({
            "category": budget.category.name,
            "budget": budget.amount,
            "spent": spent,
            "remaining": budget.amount - spent
        })

    return report


    
