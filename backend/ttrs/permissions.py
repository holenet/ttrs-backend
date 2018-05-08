from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions

from .models import Student


class IsStudentOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            Student.objects.get_by_natural_key(request.user.username)
        except ObjectDoesNotExist:
            return False
        return True


class IsOtherStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            print(Student.objects.get_by_natural_key(request.user.username))
        except ObjectDoesNotExist:
            return False
        return True

    def has_object_permission(self, request, view, evaluation):
        print(request.user.username)
        print(evaluation.author.username)
        return request.user.username != evaluation.author.username
