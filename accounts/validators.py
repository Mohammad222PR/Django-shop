from django.core.exceptions import ValidationError
import re


def validate_iranian_cellphone_number(value):
    pattern = r"^09\d{8}$"
    if not re.match(pattern, value):
        raise ValidationError("یک شماره معتبر ایرانی وارد کنید.")
