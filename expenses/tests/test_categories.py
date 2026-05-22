import pytest


@pytest.mark.django_db
class TestCategoryEndpoints:

    def test_unauthenticated_request_returns_401(self, api_client):
        response = api_client.get('/api/categories/')
        assert response.status_code == 401

    def test_authenticated_user_can_list_own_categories(
        self, auth_client_one, category_one
    ):
        response = auth_client_one.get('/api/categories/')
        assert response.status_code == 200
        assert response.data['count'] == 1
        assert response.data['results'][0]['name'] == 'Groceries'

    def test_user_cannot_see_other_users_categories(
        self, auth_client_one, category_two
    ):
        response = auth_client_one.get('/api/categories/')
        assert response.status_code == 200
        assert response.data['count'] == 0

    def test_create_category_sets_user_automatically(
        self, auth_client_one, user_one
    ):
        payload = {
            'name': 'Hobbies',
            'color': '#9b59b6',
            'icon': 'football'
        }
        response = auth_client_one.post('/api/categories/', payload)
        assert response.status_code == 201
        assert response.data['name'] == 'Hobbies'

    def test_user_cannot_delete_other_users_category(
        self, auth_client_one, category_two
    ):
        response = auth_client_one.delete(
            f'/api/categories/{category_two.id}/'
        )
        assert response.status_code == 404

    def test_duplicate_category_name_returns_400(
        self, auth_client_one, category_one
    ):
        payload = {
            'name': 'Groceries',
            'color': '#ffffff',
        }
        response = auth_client_one.post('/api/categories/', payload)
        assert response.status_code == 400