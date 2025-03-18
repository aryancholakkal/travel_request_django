from rest_framework.permissions import BasePermission
    
class IsAdmin(BasePermission):
     
    def has_permission(self, request, view):
        user = hasattr(request.user,'admin')
        return user
 