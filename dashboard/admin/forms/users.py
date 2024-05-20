from django import forms
from accounts.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User

        fields = [
            "email",
            "is_active",
            "is_verified",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add custom classes to fields
        self.fields["email"].widget.attrs[
            "class"
        ] = "form-control mx-3 Disabled text-center mb-3"
        self.fields["email"].disabled = True

        self.fields["is_active"].widget.attrs["class"] = "form-check-input mb-3"
        self.fields["is_verified"].widget.attrs["class"] = "form-check-input mb-3"


class ChangeUserDataForm(forms.Form):

    selected_user = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="کاربرای انتخاب شده",
    )
