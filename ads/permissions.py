from rest_framework import permissions


class IsAuthorOrAdmin(permissions.BasePermission):
    """
    Разрешает доступ автору объекта или админу.
    """

    def has_object_permission(self, request, view, obj):
        # Администратор может всё
        if request.user.is_authenticated and request.user.role == "admin":
            return True

        # Автор может изменять/удалять только свой объект
        return obj.author == request.user


# class IsAuthenticatedOrReadOnlyList(permissions.BasePermission):
#     """
#     Анонимные пользователи могут получать только список объявлений.
#     """
#     def has_permission(self, request, view):
#         if view.action == 'list' or request.method == "GET":
#             return True
#         return request.user and request.user.is_authenticated
