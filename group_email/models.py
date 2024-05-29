from django.db import models
from accounts.models import User
from django.utils.translation import gettext_lazy as _
# Create your models here.

class GroupEmailStatus(models.IntegerChoices):
    published = 1, _("منتشر شده")
    draft = 2, _("ذخیره")
    cancelled = 3, _("لغو شده")

class GroupEmail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group email")
    subject = models.CharField(max_length=100, verbose_name=_("subject"))
    from_email = models.EmailField(verbose_name=_("email"))
    to_email = models.TextField(max_length=10000, verbose_name=_("to email"))
    content = models.TextField(verbose_name="content")
    status = models.IntegerField(default=GroupEmailStatus.draft.value, choices=GroupEmailStatus.choices, verbose_name=_("Status"))
    created_date = models.DateField(auto_now_add=True, verbose_name=_("created date"))
    time_published = models.DateTimeField(verbose_name=_("time published"))

    def __str__(self) -> str:
        return self.subject
    
    def to_email_split(self):
        return self.to_email.split(',')
    
