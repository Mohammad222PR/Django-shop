from django.contrib.auth.mixins import UserPassesTestMixin

from accounts.models import UserType


class HasAdminAccessPermission(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated:
            return (
                self.request.user.type == UserType.superuser.value
                or self.request.user.type == UserType.admin.value
            )
        return False
