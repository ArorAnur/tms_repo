from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from TMS_system.serializers.auth_serializers import MyTokenObtainPairSerializer
from TMS_system.serializers.auth_serializers import MyTokenRefreshSerializer

class MyTokenObtainPairView(TokenObtainPairView):

    serializer_class = MyTokenObtainPairSerializer

class MyTokenRefreshView(TokenRefreshView):

    serializer_class = MyTokenRefreshSerializer
