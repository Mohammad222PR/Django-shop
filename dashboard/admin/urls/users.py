from django.urls import path
from dashboard.admin.views import users as views


urlpatterns = [
    path("user/list/", views.AdminUsersListView.as_view(), name="users-list"),
    path(
        "user/update/<int:pk>/",
        views.AdminUsersUpdateView.as_view(),
        name="users-update",
    ),
    path(
        "user/delete/<int:pk>/",
        views.AdminUsersDeleteView.as_view(),
        name="users-delete",
    ),
]
