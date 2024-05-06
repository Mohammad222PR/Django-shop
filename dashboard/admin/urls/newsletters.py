from django.urls import path
from dashboard.admin.views import newsletters as views


urlpatterns = [
    path(
        "newletters/list/",
        views.AdminNewslettersListView.as_view(),
        name="newsletters-list",
    ),
    path(
        "newletters/delete/<int:pk>/",
        views.AdminNewslettersDeleteView.as_view(),
        name="newsletters-delete",
    ),
]
