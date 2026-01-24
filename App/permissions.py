from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        # admin can do everything
        if request.user.is_staff or request.user.is_superuser:
            return True

        # user can only touch their own post
        return obj.user == request.user


