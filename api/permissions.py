from typing import Type

from django.http.request import HttpRequest
from rest_framework.permissions import BasePermission

from .models import CustomUser

class IsGuestUser(BasePermission):
    def has_permission(self, request: HttpRequest, view: Type) -> bool:
        return request.user.is_guest

class IsRegisteredUser(BasePermission):
    def has_permission(self, request: HttpRequest, view: Type) -> bool:
        if request.user.is_authenticated and not request.user.is_guest:
            return True
        else:
            return False