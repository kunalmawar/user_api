from django.urls import re_path
from user_management.views import UserPermissions, CheckPermissions, ModifyPermission, DeletePermission


urlpatterns = [
    re_path(r'^user/(?P<user_id>\d+)', UserPermissions.as_view(), name='user-perms'),
    re_path(r'^checkpermission/', CheckPermissions.as_view(), name='check-perms'),
    re_path(r'^roles/(?P<group_id>\d+)', ModifyPermission.as_view(), name='modify-perms'),
    re_path(r'^permissions/(?P<permission_id>\d+)', DeletePermission.as_view(), name='delete-perm'),
]