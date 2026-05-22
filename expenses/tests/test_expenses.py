import pytest
from datetime import date


@pytest.mark.django_db
class TestExpenseEndpoints:

    def test_unauthenticated_request_returns_401(self, api_client):
        response = api_client.get('/api/expenses/')
        assert response.status_code == 401

    def test_authenticated_user_can_list_own_expenses(
        self, auth_client_one, expense_one
    ):
        response = auth_client_one.get('/api/expenses/')
        assert response.status_code == 200
        assert response.data['count'] == 1
        assert response.data['results'][0]['description'] == 'Weekly groceries'

    def test_user_cannot_see_other_users_expenses(
        self, auth_client_one, expense_two
    ):
        response = auth_client_one.get('/api/expenses/')
        assert response.status_code == 200
        assert response.data['count'] == 0

    def test_create_expense_sets_user_automatically(
        self, auth_client_one, category_one
    ):
        payload = {
            'amount': '75.00',
            'description': 'Big shop',
            'date': str(date.today()),
            'category': category_one.id
        }
        response = auth_client_one.post('/api/expenses/', payload)
        assert response.status_code == 201
        assert response.data['amount'] == '75.00'
        assert response.data['category_name'] == 'Groceries'

    def test_user_cannot_edit_other_users_expense(
        self, auth_client_one, expense_two
    ):
        payload = {'amount': '999.00', 'date': str(date.today())}
        response = auth_client_one.patch(
            f'/api/expenses/{expense_two.id}/', payload
        )
        assert response.status_code == 404

    def test_user_cannot_delete_other_users_expense(
        self, auth_client_one, expense_two
    ):
        response = auth_client_one.delete(
            f'/api/expenses/{expense_two.id}/'
        )
        assert response.status_code == 404

    def test_filter_by_category(
        self, auth_client_one, expense_one, category_one
    ):
        response = auth_client_one.get(
            f'/api/expenses/?category={category_one.id}'
        )
        assert response.status_code == 200
        assert response.data['count'] == 1

    def test_filter_by_date_range(
        self, auth_client_one, expense_one
    ):
        today = str(date.today())
        response = auth_client_one.get(
            f'/api/expenses/?date_after={today}&date_before={today}'
        )
        assert response.status_code == 200
        assert response.data['count'] == 1