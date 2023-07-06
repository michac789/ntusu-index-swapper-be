from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_superuser
        )


class IsSelfOrReadOnly(BasePermission):
    def has_object_permission(self, request, _, obj):
        return bool(
            request.method == 'GET' or
            request.user == obj
        )
