from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAdminUser):
    # class IsAdminUser(BasePermission):
    #     """
    #     Allows access only to admin users.
    #     """
    #
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # Check permissions for read-only request
            # NOTE: "SAFE_METHODS" is "GET" request
            return True
        else:
            return bool(request.user and request.user.is_staff)
    #
    # here if the user is admin then it will return true and if not then it will return false.
    #
    # Custom permissions:
    # To implement a custom permission, override BasePermission and implement either, or both, of the following methods:
    #
    # .has_permission(self, request, view)
    # here we are just generally checking if the user has the permissions to read or anything else.
    #
    # .has_object_permission(self, request, view, obj)
    # when we use this ".has_object_permission(self, request, view, obj", we are specifically checking and testing a
    # particular object.
    #
    # The methods should return True if the request should be granted access, and False otherwise.

    # def has_permission(self, request, view):
    #     # here what we want to do is if the user is admin then we need to return true and if the user is not an admin
    #     # then we need to return false.
    #     admin_permission = bool(request.user and request.user.is_staff)
    #     # if the both conditions, "request.user" and "request.user.is_staff" are true. We have a logged in user,
    #     # which is staff
    #     # if "request.user" is true and "request.user.is_staff" is false we have a normal user logged in.
    #     # and if both "request.user" and "request.user.is_staff" in not true then no user is logged in.
    #     # So, if we going to get a true we have a permission about admin.
    #     return request.method == "GET" or admin_permission
    #     # this is only about admin otherwise we are going to check out which permission they are trying to access.
    #     # so, i am testing there method, here insted of using "GET", i am testing, if the request "GET" or they have the
    #     # admin permission.


class IsReviewUserOrReadOnly(permissions.BasePermission):
    # if the user is review owner then we are going to give the permission to edit otherwise it is going to be read only

    def has_object_permission(self, request, view, obj):
        # I am using this "has_object_permission", because we are granting permission for an individual object.

        if request.method in permissions.SAFE_METHODS:
            # Check permissions for read-only request
            # NOTE: "SAFE_METHODS" is "GET" request
            return True
        else:
            # Check permissions for write request
            # if the request is not "GET" it means it can be "POST", "PUT", "PATCH", "DELETE"
            return obj.review_user == request.user or request.user.is_staff
            # here i am checking if the user is equal to the review author
            # i.e. i am comparing "obj.review_user": the person who have written the review
            # with "request.user": the current logged in user.
            # this will return true if the user is same or if the user is admin.
