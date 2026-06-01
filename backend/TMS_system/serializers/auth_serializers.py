from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

ADMIN_SCOPES = ['admin', 'read', 'write']
STAFF_SCOPES = ['read', 'write']
USER_SCOPES = ['read']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username

        if user.is_superuser:
            token['scopes'] = ADMIN_SCOPES
        elif user.is_staff:
            token['scopes'] = STAFF_SCOPES
        else:
            token['scopes'] = USER_SCOPES

        return token
    




class MyTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        # 1. Let SimpleJWT validate the refresh token and generate standard output
        data = super().validate(attrs)
        
        # 2. Get the user ID from the validated refresh token payload
        refresh = RefreshToken(attrs['refresh'])
        user_id = refresh.payload.get('user_id')
        
        try:
            user = User.objects.get(id=user_id)
            
            # 3. Dynamically re-evaluate scopes from the DB
            if user.is_superuser:
                current_scopes = ADMIN_SCOPES
            elif user.is_staff:
                current_scopes = STAFF_SCOPES
            else:
                current_scopes = USER_SCOPES
                
            # 4. Inject the fresh scopes directly into the response's access token
            # (SimpleJWT allows you to manipulate the token object on the fly here)
            access_token = refresh.access_token
            access_token['scopes'] = current_scopes
            
            # Update the string format in the final HTTP response data dictionary
            data['access'] = str(access_token)
            
        except User.DoesNotExist:
            pass

        return data