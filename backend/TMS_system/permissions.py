# permissions/scope_permissions.py
from rest_framework.permissions import BasePermission

class HasRequiredScope(BasePermission):
    def has_permission(self, request, view):
        token = request.auth
        if not token or 'scopes' not in token:
            return False
        
        required_scope = getattr(view, 'required_scope', None)
        if not required_scope:
            return False
            
        return required_scope in token['scopes']