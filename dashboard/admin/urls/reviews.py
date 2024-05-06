from django.urls import path
from dashboard.admin.views import reviews as views


urlpatterns = [
    path("reviews/list/", views.AdminReviewsListView.as_view(), name="reviews-list"),
    path(
        "revuews/update/<int:pk>/",
        views.AdminReviewsUpdateView.as_view(),
        name="reviews-update",
    ),
]
