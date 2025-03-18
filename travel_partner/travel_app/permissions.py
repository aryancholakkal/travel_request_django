from rest_framework.permissions import BasePermission
 
class IsManager(BasePermission):
   
    def has_permission(self, request, view):
            if(request.user.id)==None:
                 return None
            user = hasattr(request.user,'manager')
            return user,request.user.id
 
class IsEmployee(BasePermission):
     
    def has_permission(self, request, view):
        user = hasattr(request.user,'employee')
        return user
   
class IsAdmin(BasePermission):
     
    def has_permission(self, request, view):
        user = hasattr(request.user,'admin')
        return user
 