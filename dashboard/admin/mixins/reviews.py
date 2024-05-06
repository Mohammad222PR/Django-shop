from accounts.models import UserType
from django.http import Http404


class ReviewUpdateFormMixin:
    def dispache(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.user.type == UserType.admin.value:
                self.fields = ["status"]
            elif request.user.type == UserType.superuser.value:
                self.fields.append("description", "rate")
        else:
            raise Http404("You can't see this page")
        return super().dispatch(request, *args, **kwargs)
