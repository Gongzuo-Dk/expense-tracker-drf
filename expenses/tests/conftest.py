import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from expenses.models import Category, Expense
from datetime import date

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_one(db):
    return User.objects.create_user(
        username='userone',
        email='userone@example.com',
        password='TestPass123!'
    )


@pytest.fixture
def user_two(db):
    return User.objects.create_user(
        username='usertwo',
        email='usertwo@example.com',
        password='TestPass123!'
    )


@pytest.fixture
def auth_client_one(api_client, user_one):
    api_client.force_authenticate(user=user_one)
    return api_client


@pytest.fixture
def auth_client_two(api_client, user_two):
    api_client.force_authenticate(user=user_two)
    return api_client


@pytest.fixture
def category_one(db, user_one):
    return Category.objects.create(
        user=user_one,
        name='Groceries',
        color='#2ecc71',
        icon='shopping-cart'
    )


@pytest.fixture
def category_two(db, user_two):
    return Category.objects.create(
        user=user_two,
        name='Transport',
        color='#3498db',
        icon='car'
    )


@pytest.fixture
def expense_one(db, user_one, category_one):
    return Expense.objects.create(
        user=user_one,
        category=category_one,
        amount='50.00',
        description='Weekly groceries',
        date=date.today()
    )


@pytest.fixture
def expense_two(db, user_two, category_two):
    return Expense.objects.create(
        user=user_two,
        category=category_two,
        amount='30.00',
        description='Bus pass',
        date=date.today()
    )