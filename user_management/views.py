from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from django.contrib.auth.models import Permission
from rest_framework.exceptions import APIException
from rest_framework.response import Response


class UserPermissions(APIView):

    def get(self, request, user_id):
        """
        This API returns all the permissions of a user
        """
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise APIException('Not a valid user id')
        return Response({'permissions': user.get_all_permissions()})


class CheckPermissions(APIView):

    def get(self, request):
        """
        This is API returns the access status of a specific user
        """
        user_id = request.GET.get('user_id')
        permission_id = request.GET.get('permission_id')
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise APIException('Not a valid user id')
        permission = Permission.objects.filter(id=permission_id).first()
        if not permission:
            raise APIException('Not a valid permission')
        return Response({'access_allowed': True if user.has_perm(permission.name) else False})


class ModifyPermission(APIView):

    def post(self, request, group_id):
        """
        This API accepts x-www-form-urlencoded only
        """
        permission_ids = request.POST.getlist('permissions')
        group = Group.objects.filter(id=group_id).first()
        if not group:
            raise APIException('Not a valid group id')
        permissions = list(Permission.objects.filter(id__in=permission_ids))
        if not permissions:
            raise APIException('Permissions not found')
        # Clearing all permissions
        group.permissions.clear()
        # Adding new permissions
        group.permissions.add(*permissions)
        return Response({'status': 'Permissions successfully modified'})


class DeletePermission(APIView):

    def delete(self, request, permission_id):
        """
        This API deletes a specific permission
        """
        permission = Permission.objects.filter(id=permission_id).first()
        if not permission:
            raise APIException('Not a valid permission')
        # Not sure if we really want to delete a permission or clearing it for all user
        # So clearing it as a safer option
        # Clearing user permissions
        permission.user_set.clear()
        # Clearing group permission
        permission.group_set.clear()
        return Response({'status': 'Permission deleted'})
