from rest_framework.permissions import BasePermission

class IsSuperUserOrReadOnly(BasePermission):
    """
    Custom permission to allow superusers to perform any action,
    and allow read-only access to others.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Check if the user is a superuser to allow other methods.
        return request.user and request.user.is_superuser
