from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrAdminForOrder(BasePermission):

    def has_permission(self, request, view):
        if request.method == "POST":
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated


    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        if obj.user == request.user:
            if request.method in SAFE_METHODS:
                return True

            if request.method in ["PATCH", "PUT"]:
                return obj.status == 1

        return False