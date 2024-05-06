from django import forms
from website.models import AnswerContacts
from website.models import ContactUs


class AnswerContactForm(forms.ModelForm):
    class Meta:
        model = AnswerContacts
        fields = ("message",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["message"].widget.attrs["class"] = "form-control"
