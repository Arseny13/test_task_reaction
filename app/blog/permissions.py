from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsReadOnly(BasePermission):
    """Перминш для изменение моделей только cоздателям или админу."""

    def has_permission(self, request, view):
        """GET-запрос не требует авторизации."""
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Пользователь User не может редактировать(удлять) чужой объект."""
        return (
            request.method in SAFE_METHODS
            or obj.user == request.user
            or request.user.is_admin
        )
