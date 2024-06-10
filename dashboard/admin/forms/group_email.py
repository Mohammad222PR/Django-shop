from django import forms
from django.utils import timezone
from group_email.models import GroupEmail, GroupEmailStatus
from django.core.exceptions import ValidationError

class ChangeGroupEmailDataForm(forms.Form):
    CHANGE_CHOICES = [
        ("published", "انتشار"),
        ("draft", "ذخیره"),
        ("cancelled", "لغو"),
    ]

    change_type = forms.ChoiceField(choices=CHANGE_CHOICES, label="نوع تغییر")
    selected_products = forms.ModelMultipleChoiceField(
        queryset=GroupEmail.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="ایمیل های انتخاب شده",
    )


class GroupEmailStartForm(forms.ModelForm):
    time_published =  forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"class": "form-control", "type": "datetime-local"}
        )
    )
    class Meta:
        model = GroupEmail
        fields = ["subject", "from_email", "time_published", "content"]


    # def clean_time_published(self):
    #     time_published = self.cleaned_data["time_published"]


    #     if time_published <= timezone.now():
    #         return ValidationError("تاریخ انتشار نمی تواند برای قبل از تاریخ امروز باشد")
    #     return time_published
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subject"].widget.attrs["class"] = "form-control"
        self.fields["from_email"].widget.attrs["class"] = "form-control"
 

        self.fields["content"].widget.attrs["class"] = "ckeditor"

