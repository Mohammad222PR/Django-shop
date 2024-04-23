from django import forms
from shop.models import Product, ProductStatus
from review.models import Review


class SubmitReviewForm(forms.ModelForm):
    class Meta:
        models = Review
        fields = ["product", "review", "description"]

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')

        try:
            Product.objects.get(id=product.id, status=ProductStatus.published.value)
        except Product.DoesNotExist:
            raise forms.ValidationError("این محصول وجود ندارد")

        return cleaned_data
