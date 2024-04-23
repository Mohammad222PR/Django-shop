from django.urls import path, re_path
from . import views

app_name = "review"

urlpatterns = [
    re_path(
        r"reviews/submit/",
        views.SubmitReviewView.as_view(),
        name="submit-review",
    )
]
