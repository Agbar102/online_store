from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class IsAdminWithCustomMessage(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated and request.user.is_staff):
            raise PermissionDenied(detail="У вас недостаточно прав для доступа к этому ресурсу.")
        return True

