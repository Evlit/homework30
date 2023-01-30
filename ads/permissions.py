from rest_framework import permissions

from ads.models import User


class AdUpdateDeletePermission(permissions.BasePermission):
    message = 'Update or Delete ads only for owner or admin/moderator users.'

    def has_object_permission(self, request, view, obj):
        if request.user != obj.author and request.user.role == User.MEMBER:
            return False
        return True


class SelectionChangePermission(permissions.BasePermission):
    message = 'Change selections only for authorization owners.'

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False
