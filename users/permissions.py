from typing import Any

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser


class IsUser(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> Any:
        return obj.pharmacist == request.user


class UserNew(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.id


class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsCustomer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user
