import pytest
from datetime import date
from expenses.models import Expense


@pytest.mark.django_db
class TestSummaryEndpoint:

    def test_summary_returns_correct_total(
        self, auth_client_one, user_one, category_one
    ):
        Expense.objects.create(
            user=user_one, category=category_one,
            amount='100.00', date=date.today()
        )
        Expense.objects.create(
            user=user_one, category=category_one,
            amount='50.00', date=date.today()
        )
        response = auth_client_one.get('/api/expenses/summary/')
        assert response.status_code == 200
        assert str(response.data['total']) == '150.00'
        assert response.data['expense_count'] == 2

    def test_summary_only_includes_current_users_data(
        self, auth_client_one, expense_two
    ):
        response = auth_client_one.get('/api/expenses/summary/')
        assert response.status_code == 200
        assert response.data['expense_count'] == 0

    def test_summary_returns_zeros_when_no_expenses(
        self, auth_client_one
    ):
        response = auth_client_one.get('/api/expenses/summary/')
        assert response.status_code == 200
        assert response.data['expense_count'] == 0


@pytest.mark.django_db
class TestByCategoryEndpoint:

    def test_by_category_returns_correct_breakdown(
        self, auth_client_one, user_one, category_one
    ):
        Expense.objects.create(
            user=user_one, category=category_one,
            amount='100.00', date=date.today()
        )
        response = auth_client_one.get('/api/expenses/by-category/')
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['category_name'] == 'Groceries'
        assert str(response.data[0]['total']) == '100.00'
        assert response.data[0]['percentage'] == 100.0

    def test_by_category_excludes_other_users_data(
        self, auth_client_one, expense_two
    ):
        response = auth_client_one.get('/api/expenses/by-category/')
        assert response.status_code == 200
        assert len(response.data) == 0