from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        'message': 'Expense Tracker API',
        'version': '1.0',
        'status': 'online',
        'endpoints': {
            'auth': {
                'register': '/auth/registration/',
                'login': '/auth/login/',
                'logout': '/auth/logout/',
                'user': '/auth/user/',
                'google': '/auth/google/',
            },
            'categories': {
                'list_create': '/api/categories/',
                'detail': '/api/categories/{id}/',
            },
            'expenses': {
                'list_create': '/api/expenses/',
                'detail': '/api/expenses/{id}/',
                'summary': '/api/expenses/summary/',
                'by_category': '/api/expenses/by-category/',
            },
        },
        'authentication': 'Token based — include header: Authorization: Token <your_token>',
        'note': 'All /api/ endpoints require authentication except /auth/ endpoints.',
    })