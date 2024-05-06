from website.models import ContactUs, Status
from django.contrib import messages


class ContaxtMixin:
    def dispache(self, request, *args, **kwargs):
        contact = ContactUs.objects.get(id=self.kwargs.get("pk"), user=self.request.user)
        if not contact.status == Status.closed.value:
            pass
        else:
            return messages.error(
                request, "تیکت فعلی بسته شده است و دیگر قابلیت ارسال پیام وجود ندارد"
            )
        return super().dispatch(request, *args, **kwargs)
