from django import forms

from shop.models import Product, ProductImage


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "category",
            "title",
            "slug",
            "image",
            "description",
            "brief_description",
            "stock",
            "status",
            "price",
            "discount_percent",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs["class"] = "form-control"
        self.fields["slug"].widget.attrs["class"] = "form-control"
        self.fields["category"].widget.attrs["class"] = "form-control"
        self.fields["image"].widget.attrs["class"] = "form-control"
        self.fields["image"].widget.attrs[
            "accept"
        ] = "image/png, image/jpg, image/jfif, image/jpeg"
        self.fields["brief_description"].widget.attrs["class"] = "form-control"
        self.fields["description"].widget.attrs["class"] = "ckeditor"
        self.fields["stock"].widget.attrs["class"] = "form-control"
        self.fields["stock"].widget.attrs["type"] = "number"
        self.fields["status"].widget.attrs["class"] = "form-select"
        self.fields["price"].widget.attrs["class"] = "form-control"
        self.fields["discount_percent"].widget.attrs["class"] = "form-control"


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ("file",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["file"].widget.attrs["class"] = "form-control"
        self.fields["file"].widget.attrs["accept"] = "image/png, image/jpg, image/jpeg"


class ChangeProductDataForm(forms.Form):
    CHANGE_CHOICES = [
        ("increase", "افزایش قیمت"),
        ("decrease", "کاهش قیمت"),
        ("published", "انتشار"),
        ("draft", "ذخیره"),
        ("delete", "حذف"),
    ]

    change_type = forms.ChoiceField(choices=CHANGE_CHOICES, label="نوع تغییر")
    percent = forms.DecimalField(label="مقدار", min_value=0)
    selected_products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="محصولات انتخاب شده",
    )
