# views/user_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import UserRegisterSerializer

class RegisterUserView(APIView):
    # Public endpoint allowing unauthenticated users to create an account
    permission_classes = [] 

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save() triggers our Service Layer underneath
            serializer.save()
            return Response({
                "message": "User registered successfully.",
                "user": {
                    "username": serializer.validated_data['username'],
                    "email": serializer.validated_data['email']
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
