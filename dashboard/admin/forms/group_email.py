from django import forms

from group_email.models import GroupEmail, GroupEmailStatus


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
