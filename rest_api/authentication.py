from rest_framework import permissions

        
class RequestPermission(permissions.BasePermission):
    message = 'You do not have the right permission to access this data'

    def has_permission(self, request, view, method, permissions_required):
        if request.method == method or method == "ANY":
            for permission_str in permissions_required:
                if not getattr(request.user, permission_str):
                    return False
        return True


class HasPermission(RequestPermission):
    def has_permission(self, request, view):
      return super(HasPermission, self).has_permission(request, view, "ANY", view.permissions_required)


class HasDeletePermission(RequestPermission):
    def has_permission(self, request, view):
      return super(HasDeletePermission, self).has_permission(request, view, "DELETE", view.delete_permissions_required)


class HasGetPermission(RequestPermission):
    def has_permission(self, request, view):
      return super(HasGetPermission, self).has_permission(request, view, "GET", view.get_permissions_required)


class HasPostPermission(RequestPermission):
    def has_permission(self, request, view):
      return super(HasPostPermission, self).has_permission(request, view, "POST", view.post_permissions_required)


class HasPutPermission(RequestPermission):
    def has_permission(self, request, view):
      return super(HasPutPermission, self).has_permission(request, view, "PUT", view.put_permissions_required)