from django.urls import path
from dashboard.customer.views import profiles as views


urlpatterns = [
    path("security-edit/", views.CustomerSecurityEditView.as_view(), name="security-edit"),
    path("profile-edit/", views.CustomerProfileEditView.as_view(), name="profile-edit"),
    path(
        "profile-edit/delete-avatar/",
        views.CustomerProfileDeleteAvatarView.as_view(),
        name="profile-delete-avatar",
    ),
]
