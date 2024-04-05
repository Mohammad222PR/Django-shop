from django.urls import path
from dashboard.admin.views import profiles as views


urlpatterns = [
    path("security-edit/", views.AdminSecurityEditView.as_view(), name="security-edit"),
    path("profile-edit/", views.AdminProfileEditView.as_view(), name="profile-edit"),
    path(
        "profile-edit/delete-avatar/",
        views.AdminProfileDeleteAvatarView.as_view(),
        name="profile-delete-avatar",
    ),
]
