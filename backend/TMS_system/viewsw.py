from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class DashboardDataView(APIView):
    # This enforces that a valid JWT token must be provided in the headers
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {
            'message': f'Authenticated successfully! Welcome to the dashboard, {request.user.username}.',
            'status': 'Secure data fetched.'
        }
        return Response(content)