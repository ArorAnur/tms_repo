from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class DashboardDataView(APIView):
  
    permission_classes = [IsAuthenticated]

    def get(self, request):
    
        content = {
            'message': f'Authenticated successfully! Welcome to the dashboard, {request.user.username}.',
            'status': 'Secure data fetched.'
        }
        return Response(content)