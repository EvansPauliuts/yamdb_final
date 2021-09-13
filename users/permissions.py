from rest_framework import permissions


class IsModeratorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user and request.user.is_moderator)


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user and request.user.is_admin)


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user and request.user.is_user)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return ((request.method in permissions.SAFE_METHODS)
                or request.user.is_authenticated and request.user.is_admin)


class ReviewCommentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return ((request.method in permissions.SAFE_METHODS)
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return ((request.method in permissions.SAFE_METHODS)
                or obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin)
