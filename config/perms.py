from rest_framework.permissions import BasePermission


class ModeratorAllow(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Moderators').exists()


class ModeratorNotAllow(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Moderators').exists():
            return False
        return True


class IsObjectOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.creator


class ModeratorAndObjectCreatorAllow(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Moderators').exists() and request.method in ['GET', 'PUT', 'PATCH']:
            return True
        if request.user == obj.creator:
            return True
        return False