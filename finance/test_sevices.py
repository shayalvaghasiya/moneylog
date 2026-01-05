from django.test import TestCase
from django.utils import timezone

from django.contrib.auth import get_user_model
from finance.models import Account, Category, Transaction
from finance.services import get_filtered_transactions


class TransactionServiceTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.account = Account.objects.create(user=self.user, name="Cash", account_type="cash", opening_balance=0)
        self.food = Category.objects.create(user=self.user, name="Food", category_type="expense")
        self.salary = Category.objects.create(user=self.user, name="Salary", category_type="income")

        Transaction.objects.create(user=self.user, account=self.account, category=self.food, amount=100, transaction_type="expense", occurred_at=timezone.now())
        Transaction.objects.create(user=self.user, account=self.account, category=self.salary, amount=1000, transaction_type="income", occurred_at=timezone.now())

    def test_filter_by_category(self):
        params = {"category": self.food.id}
        transactions = get_filtered_transactions(self.user, params)

        self.assertEqual(transactions.count(), 1)
        self.assertEqual(transactions.first().category, self.food)

    
    def test_filter_by_date(self):
        today = timezone.now().date().isoformat()
        params = {"from": today, "to": today}

        transactions = get_filtered_transactions(self.user, params)
        self.assertEqual(transactions.count(), 2)
