from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from finance.models import Account, Category, Transaction

class TransactionAPITest(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass"
        )

        self.account = Account.objects.create(
            user=self.user,
            name="Cash",
            account_type="cash",
            opening_balance=0
        )

        self.category = Category.objects.create(
            user=self.user,
            name="Food",
            category_type="expense"
        )

        Transaction.objects.create(
            user=self.user,
            account=self.account,
            category=self.category,
            amount=100,
            transaction_type="expense",
            occurred_at=timezone.now()
        )

        self.url = reverse("transaction_list_api")

    def test_api_requires_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_get_transactions(self):
        self.client.login(username="testuser", password="testpass")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)

    
    def test_create_transaction(self):
        self.client.login(username="testuser", password="testpass")

        payload = {
            "transaction_type": "expense",
            "amount": "250.00",
            "category": self.category.id,
            "account": self.account.id,
            "occurred_at": timezone.now().isoformat(),
            "note": "Dinner",
        }

        response = self.client.post(
            self.url,
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 2)

