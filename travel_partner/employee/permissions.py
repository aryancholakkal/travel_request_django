from rest_framework.permissions import BasePermission
 
class IsEmployee(BasePermission):
     
    def has_permission(self, request, view):
        user = hasattr(request.user,'employee')
        return user